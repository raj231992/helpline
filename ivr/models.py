from __future__ import unicode_literals

from django.db import models
from .options import Session
from management.models import HelpLine,HelperCategory
from registercall.models import Task

# Create your models here.

class IVR_Call(models.Model):
    sid = models.CharField(max_length=256)
    caller_no = models.CharField(max_length=15)
    caller_location = models.CharField(max_length=256)
    helpline_no = models.CharField(max_length=15)
    language_option = models.CharField(max_length=2)
    category_option = models.CharField(max_length=2)
    session_next = models.CharField(max_length=256,choices=Session.SESSION_CHOICES)

    def __unicode__(self):
        return str(self.caller_no)

class Call_Forward(models.Model):
    helper_no = models.CharField(max_length=15)
    caller_no = models.CharField(max_length=15)

    def __unicode__(self):
        return str(self.helper_no)

class Language(models.Model):
    language = models.CharField(max_length=20)
    helpline = models.ForeignKey(HelpLine, on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.language)


class IVR_Audio(models.Model):
    helpline = models.ForeignKey(HelpLine,on_delete=models.CASCADE)
    category = models.ForeignKey(HelperCategory,on_delete=models.CASCADE)
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    audio = models.FileField(upload_to='ivr_audio/')

    def __unicode__(self):
        return str(self.category)+" "+str(self.language)

class Misc_Category(models.Model):
    category = models.CharField(max_length=20)

    def __unicode__(self):
        return str(self.category)

class Misc_Audio(models.Model):
    helpline = models.ForeignKey(HelpLine,on_delete=models.CASCADE)
    category = models.ForeignKey(Misc_Category,on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    audio = models.FileField(upload_to='ivr_audio/')

    def __unicode__(self):
        return str(self.category)+" "+str(self.language)

  # FEEDBACK SYSTEM ###

class FeedbackType(models.Model):
    helpline = models.ForeignKey(HelpLine, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    audio = models.FileField(upload_to='ivr_audio/')

    def __unicode__(self):
        return str(self.question)


class FeedbackResponse(models.Model):
    feedbackType = models.ForeignKey(FeedbackType, on_delete=models.CASCADE)
    response = models.IntegerField()

    def __unicode__(self):
        return str(self.feedbackType.question)

class Feedback(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    feedbackresponses = models.ManyToManyField(FeedbackResponse)
    # current_question = models.ForeignKey(FeedbackResponse, on_delete=models.CASCADE)
    current_question = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.id)
