from django.shortcuts import render
from rest_framework.views import APIView
from .models import HelpLine,HelperCategory
from django.shortcuts import get_object_or_404
from register_helper.models import Helper
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import HelperCategorySerializer,HelplineSerializer
import json
from task_manager.models import Action,Assign,QandA
from task_manager.options import AssignStatusOptions,ActionStatusOptions
from django.utils import timezone
from registercall.models import CallRequest,Task
from registercall.options import TaskStatusOptions
from task_manager.helpers import HelperMethods
from ivr.models import Call_Forward
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.

class getHelplines(APIView):
    def post(self,request):
        helplines = HelpLine.objects.all()
        helplines = HelplineSerializer(helplines,many=True)
        return Response({"helplines": helplines.data}, status=200)
class getHelplineNumber(APIView):
    def post(self, request):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        helper = get_object_or_404(Helper, user=user)
        helpline_number = helper.helpline.helpline_number
        return Response({"helpline_number": "0"+helpline_number[2:]}, status=200)

class getHelplineCategories(APIView):
    def post(self,request):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        helper = get_object_or_404(Helper, user=user)
        helpline = helper.helpline
        helpline_categories = HelperCategory.objects.filter(helpline=helpline).exclude(name='Repeat')
        helpline_categories = HelperCategorySerializer(helpline_categories,many=True)
        return Response({"categories":helpline_categories.data},status=200)

class getHelperProfile(APIView):
    def post(self,request):
        username = request.data.get("username")
        user = get_object_or_404(User,username=username)
        helper = get_object_or_404(Helper,user=user)
        helper_cat = HelperCategorySerializer(helper.category.all(),many=True)
        data = {
            "first_name":user.first_name,
            "last_name":user.last_name,
            "email":user.email,
            "phone_no":helper.helper_number,
            "category":helper_cat.data
        }
        return Response(data,status=200)

class setHelperProfile(APIView):
    def post(self,request):
        username = request.data.get("username")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        phone_no = request.data.get("phone_no")
        email = request.data.get("email")
        categories = json.loads(request.data.get("categories"))
        user = get_object_or_404(User, username=username)
        helper = get_object_or_404(Helper, user=user)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        helper.helper_number = phone_no
        helpercategories = HelperCategory.objects.all()
        for category in helpercategories:
            if categories.get(category.name)=="True":
                helper.category.add(HelperCategory.objects.get(name=category.name))
            else:
                helper.category.remove(HelperCategory.objects.get(name=category.name))
        helper.save()
        user.save()
        return Response({"notification":"successful"},status=200)

class getHelperTasks(APIView):
    def post(self,request):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        helper = get_object_or_404(Helper, user=user)
        pending_assigns = Assign.objects.filter(helper=helper,status=AssignStatusOptions.PENDING).order_by('-created')
        accepted_assigns = Assign.objects.filter(helper=helper,status=AssignStatusOptions.ACCEPTED).order_by('-modified')
        completed_assigns = Assign.objects.filter(helper=helper,status=AssignStatusOptions.COMPLETED).order_by('-modified')
        pending_list = []
        accepted_list = []
        completed_list = []
        for assign in pending_assigns:
            task_id = assign.action.task.id
            task_category = assign.action.task.category.name
            caller_name = assign.action.task.call_request.client.name
            caller_number = assign.action.task.call_request.client.client_number
            caller_location = assign.action.task.call_request.client.location
            local_datetime = timezone.localtime(assign.action.task.created)
            local_date = local_datetime.strftime("%B %d,%Y")
            local_time = local_datetime.strftime("%I:%M %p")
            data = {"task_id":task_id,"task_category":task_category,"caller_name":caller_name,"caller_location":caller_location,
                    "caller_number":caller_number,"date":local_date,"time":local_time}
            pending_list.append(data)

        for assign in accepted_assigns:
            task_id = assign.action.task.id
            task_category = assign.action.task.category.name
            caller_name = assign.action.task.call_request.client.name
            caller_number = assign.action.task.call_request.client.client_number
            caller_location = assign.action.task.call_request.client.location
            local_datetime = timezone.localtime(assign.action.task.created)
            local_date = local_datetime.strftime("%B %d,%Y")
            local_time = local_datetime.strftime("%I:%M %p")
            data = {"task_id": task_id, "task_category": task_category, "caller_name": caller_name,"caller_location":caller_location,
                    "caller_number": caller_number, "date": local_date, "time": local_time}
            accepted_list.append(data)

        for assign in completed_assigns:
            task_id = assign.action.task.id
            task_category = assign.action.task.category.name
            caller_name = assign.action.task.call_request.client.name
            caller_number = assign.action.task.call_request.client.client_number
            caller_location = assign.action.task.call_request.client.location
            local_datetime = timezone.localtime(assign.action.task.created)
            local_date = local_datetime.strftime("%B %d,%Y")
            local_time = local_datetime.strftime("%I:%M %p")
            data = {"task_id": task_id, "task_category": task_category, "caller_name": caller_name,"caller_location":caller_location,
                    "caller_number": caller_number, "date": local_date, "time": local_time}
            completed_list.append(data)

        return Response({"pending":pending_list,"accepted":accepted_list,"completed":completed_list}, status=200)

class HelperAccept(APIView):
    def post(self,request):
        username = request.data.get("username")
        task_id = request.data.get("task_id")
        task_status = request.data.get("task_status")
        user = get_object_or_404(User, username=username)
        helper = get_object_or_404(Helper, user=user)
        task = Task.objects.get(id=task_id)
        action = Action.objects.get(task=task)
        assign = Assign.objects.filter(action=action, status=AssignStatusOptions.ACCEPTED)
        if assign:
            return Response({"notification:task already accepted"},status=200)
        assign = Assign.objects.get(action=action,helper=helper)
        if task_status=="accept":
            assign.status = AssignStatusOptions.ACCEPTED
            assign.save()
            action.status = ActionStatusOptions.ASSIGNED
            action.save()
            assign = Assign.objects.filter(action=action).exclude(status=AssignStatusOptions.ACCEPTED)
            assign.delete()
            return Response({"notification":"successful"},status=200)
        else:
            assign.status = AssignStatusOptions.REJECTED
            assign.save()
            assigns = Assign.objects.filter(action=action).exclude(status=AssignStatusOptions.REJECTED)
            if len(assigns)==0:
                assigns = Assign.objects.filter(action=action,status=AssignStatusOptions.REJECTED)
                rejected_helpers=[]
                for assign in assigns:
                    rejected_helpers.append(assign.helper.id)
                helpermethod = HelperMethods()
                data = "New Task Has Been Assigned"
                helpermethod.reassign_helpers(action,task.category,data,2,rejected_helpers)
            return Response({"notification":"successful"}, status=200)

class getQandA(APIView):
    def post(self, request):
        question = request.data.get("question")
        answer = request.data.get("answer")
        task_id = request.data.get("task_id")
        client_name = request.data.get("client_name")
        task = Task.objects.get(id=task_id)
        qanda = QandA(task=task,question=question,answer=answer)
        qanda.save()
        task.call_request.client.name = client_name
        task.call_request.client.save()
        return Response({"notification": "successful"}, status=200)

class TaskComplete(APIView):
    def post(self,request):
        task_id = request.data.get("task_id")
        task = Task.objects.get(id=task_id)
        action = Action.objects.get(task=task)
        assign = Assign.objects.get(action=action)
        task.status = TaskStatusOptions.COMPLETED
        task.save()
        action.status = ActionStatusOptions.COMPLETED
        action.save()
        assign.status = AssignStatusOptions.COMPLETED
        assign.save()
        return Response({"notification": "successful"}, status=200)

class CallForward(APIView):
    def post(self,request):
        task_id = request.data.get("task_id")
        task = Task.objects.get(id=task_id)
        action = Action.objects.get(task=task)
        assign = Assign.objects.get(action=action)
        helper_no = assign.helper.helper_number
        client_no = task.call_request.client.client_number
        Call_Forward.objects.all().delete()

        call_forward = Call_Forward(helper_no=helper_no[len(helper_no)-10:],caller_no=client_no,task=task)
        call_forward.save()
        return Response({"notification": "successful"}, status=200)

class ActivateHelper(View):
    def get(self,request,id):
        helper = Helper.objects.get(user__id = id)
        helper.login_status = 2
        helper.save()
        return HttpResponseRedirect(reverse('dashboard:home'))








