"""
Admin view management for task manager app
"""
from django.contrib import admin

from .models import Action, Assign, QandA

class QandAAdmin(admin.ModelAdmin):
    list_display = ["task","question","answer"]
    class Meta:
        model = QandA

admin.site.register(Action)
admin.site.register(Assign)
admin.site.register(QandA,QandAAdmin)
