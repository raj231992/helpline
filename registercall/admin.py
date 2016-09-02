"""
Admin view management for register call
"""
from django.contrib import admin

from .models import CallRequest, Task

class AdminRegisterCall(admin.ModelAdmin):
    list_display = ['helpline','client','created','status']
    class Meta:
        model = CallRequest

class AdminTask(admin.ModelAdmin):
    list_display = ['request_call_id','helpline','category','created','modified','status']
    class Meta:
        model = Task
    def request_call_id(self,obj):
        return obj.call_request
    def helpline(self,obj):
        return obj.call_request.helpline.name

admin.site.register(CallRequest,AdminRegisterCall)
admin.site.register(Task,AdminTask)
