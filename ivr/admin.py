from django.contrib import admin
from .models import IVR_Call,Call_Forward,Language,IVR_Audio,Misc_Audio,Misc_Category

# Register your models here.

class IVR_Admin(admin.ModelAdmin):
    list_display = ["caller_no","caller_location"]
    class Meta:
        model= IVR_Call


admin.site.register(IVR_Call,IVR_Admin)
admin.site.register(Call_Forward)
admin.site.register(Language)
admin.site.register(IVR_Audio)
admin.site.register(Misc_Audio)
admin.site.register(Misc_Category)