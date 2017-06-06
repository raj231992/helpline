"""
Url config file for Register Helper App
"""
from django.conf.urls import url

from .views import Login,Logout,ActivateHelper,ResetPassword

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^activatehelper/$', ActivateHelper.as_view(), name='activatehelper'),
    url(r'^reset_password/$', ResetPassword.as_view(), name='resetpassword'),
]
