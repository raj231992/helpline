from django.shortcuts import render
from rest_framework.views import APIView
from .models import HelpLine,HelperCategory
from django.shortcuts import get_object_or_404
from register_helper.models import Helper
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import HelperCategorySerializer,HelplineSerializer
# Create your views here.

class getHelplines(APIView):
    def post(self,request):
        helplines = HelpLine.objects.all()
        helplines = HelplineSerializer(helplines,many=True)
        return Response({"helplines": helplines.data}, status=200)

class getHelplineCategories(APIView):
    def post(self,request):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        helper = get_object_or_404(Helper, user=user)
        helpline = helper.helpline
        helpline_categories = HelperCategory.objects.filter(helpline=helpline)
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
        print request.data
        return Response(request.data,status=200)



