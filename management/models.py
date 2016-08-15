from __future__ import unicode_literals

from django.db import models

# Create your models here.


class HelpLine(models.Model):
    """
    Model for different helpline numbers
    Eg: General helping number, education specific etc.
    """
    name = models.CharField(max_length=64, default="General")
    helpline_number = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class HelperCategory(models.Model):
    """
    Model to map helpers to different categories, many-to-many from helpers side
    """
    helpline = models.ForeignKey(HelpLine,on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
