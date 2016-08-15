"""
Admin view management for register call
"""
from django.contrib import admin

from .models import  Helper, HelperCategory


admin.site.register(Helper)
