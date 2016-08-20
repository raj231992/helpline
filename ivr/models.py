from __future__ import unicode_literals

from django.db import models
from .options import Session

# Create your models here.

class IVR_Call(models.Model):
    sid = models.CharField(max_length=256)
    caller_no = models.CharField(max_length=15)
    caller_location = models.CharField(max_length=256)
    helpline_no = models.CharField(max_length=15)
    category_option = models.CharField(max_length=2)
    session_next = models.CharField(max_length=256,choices=Session.SESSION_CHOICES)

    def __unicode__(self):
        return str(self.caller_no)