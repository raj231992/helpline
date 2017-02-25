from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.models import Assign
from register_helper.models import Helper
# Create your views here.

class Home(LoginRequiredMixin,View):
    login_url = '/web_auth/login/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        user = request.user
        helper = Helper.objects.filter(user=user)
        if helper:
            print helper[0].helpline
            assigns = Assign.objects.filter(helper__helpline=helper[0].helpline).order_by('-id')
            for assign in assigns:
                print assign.helper.helpline
            pending = 0
            completed = 0
            rejected = 0
            total = 0
            for assign in assigns:
                if assign.action.task.status == 1:
                    pending += 1
                elif assign.action.task.status == 2:
                    completed += 1
                elif assign.action.task.status == 3:
                    rejected += 1
                total += 1
        else:
            assigns = Assign.objects.all().order_by('-id')
            pending = 0
            completed = 0
            rejected = 0
            total = 0
            for assign in assigns:
                if assign.action.task.status==1:
                    pending+=1
                elif assign.action.task.status==2:
                    completed+=1
                elif assign.action.task.status == 3:
                    rejected += 1
                total+=1
        context = {
            'assigns': assigns,
            'pending': pending,
            'completed': completed,
            'rejected': rejected,
            'total': total,
        }
        return render(request,'dashboard.html',context)
