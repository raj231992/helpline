"""
Admin view management for task manager app
"""
from django.contrib import admin

from .models import Action, Assign, QandA, Feedback

class QandAAdmin(admin.ModelAdmin):
    list_display = ["task","created","question","answer"]
    class Meta:
        model = QandA

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["q_a","helper","valid","status"]
    class Meta:
        model = Feedback

admin.site.register(Action)
admin.site.register(Assign)
admin.site.register(QandA,QandAAdmin)
admin.site.register(Feedback,FeedbackAdmin)

