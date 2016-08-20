from django.contrib import admin
from .models import IVR_Call

# Register your models here.

class IVR_Admin(admin.ModelAdmin):
    list_display = ["caller_no","caller_location"]
    class Meta:
        model= IVR_Call


admin.site.register(IVR_Call,IVR_Admin)