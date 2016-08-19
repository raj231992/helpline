from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from register_helper.models import Helper
from register_helper.options import LoginStatus
from django.shortcuts import get_object_or_404
from management.notifications import push_notification
from rest_framework.response import Response


class Login(APIView):

    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username,password=password)
        if user is not None:
            helper = get_object_or_404(Helper,user=user)
            if helper.login_status!= LoginStatus.PENDING:
                helper.login_status = LoginStatus.LOGGED_IN
                helper.save()
                return Response({"notification": "successful"}, status=200)
            else:
                return Response({"notification": "pending"}, status=200)
        else:
            return Response({"notification": "failed"}, status=200)


class Logout(APIView):

    def post(self, request):
        data = request.data
        username = data.get("username")
        user = get_object_or_404(User,username=username)
        if user is not None:
            helper = get_object_or_404(Helper,user=user)
            helper.login_status = LoginStatus.LOGGED_OUT
            helper.save()
            return Response({"notification": "successful"}, status=200)
        else:
            return Response({"notification": "failed"}, status=200)


class ActivateHelper(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        user = get_object_or_404(User, username=username)
        if user is not None:
            helper = get_object_or_404(Helper, user=user)
            helper.login_status = LoginStatus.LOGGED_OUT
            helper.save()
            push_notification(helper.gcm_canonical_id,"Account Activated")

            return Response({"notification": "successful"}, status=200)
        else:
            return Response({"notification": "failed"}, status=200)