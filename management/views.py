from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import HelpLine
from .serializers import HelplineSerializer
# Create your views here.

class getHelplines(APIView):
    def post(self,request):
        helplines = HelpLine.objects.all()
        helplines = HelplineSerializer(helplines,many=True)
        return JsonResponse({"helplines": helplines.data}, status=200)



