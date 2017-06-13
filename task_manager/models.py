"""
Models related to task management
"""

from django.db import models

from registercall.models import  Task
from register_helper.models import Helper

from .options import (ActionStatusOptions, ActionTypeOptions,
                      AssignStatusOptions)


class Action(models.Model):
    """
    Model for actions for a specific task
    Refers to task
    """
    task = models.ForeignKey(Task, related_name='actions')

    created = models.DateTimeField('Created Timestamp', auto_now_add=True)
    modified = models.DateTimeField('Modified Timestamp', auto_now=True)

    action_type = models.IntegerField(
        default=ActionTypeOptions.PRIMARY,
        choices=ActionTypeOptions.ACTION_CHOICES,
    )
    status = models.IntegerField(
        default=ActionStatusOptions.ASSIGN_PENDING,
        choices=ActionStatusOptions.STATUS_CHOICES,
    )

    def __str__(self):
        return str(self.pk)


class Assign(models.Model):
    """
    Model for helpers assigned to a particular action
    Refers to action and helper
    """
    helper = models.ForeignKey(Helper, related_name='assigned_to')
    action = models.ForeignKey(Action, related_name='assigned_to')

    created = models.DateTimeField('Created Timestamp', auto_now_add=True)
    accepted = models.DateTimeField('Accepted Timestamp', auto_now_add=True)
    modified = models.DateTimeField('Modified Timestamp', auto_now=True)

    status = models.IntegerField(
        default=AssignStatusOptions.PENDING,
        choices=AssignStatusOptions.STATUS_CHOICES,
    )

    def __str__(self):
        return str(self.pk)


class QandA(models.Model):
    """
    Model for storing the questions and answers for every task
    Refers to task
    """
    task = models.ForeignKey(Task, related_name='q_and_a')
    created = models.DateTimeField('Created Timestamp', auto_now_add=True)

    # Question obtained from primary and updated by specialist helper, Answer from specialist
    question = models.CharField(max_length=512, null=True, default=None, blank=True)
    answer = models.CharField(max_length=512, null=True, default=None, blank=True)

    # Question and Answer obtained from feedback collector
    feedback_question = models.CharField(max_length=512, null=True, default=None, blank=True)
    feedback_answer = models.CharField(max_length=512, null=True, default=None, blank=True)

    # True/False status to tell if answer given was right or wrong
    verified = models.IntegerField(null=True, blank=True)

class Feedback(models.Model):
    valid_options = (
        ('Yes','Yes'),
        ('No','No'),
    )
    status_options = (
        ('pending','pending'),
        ('completed','completed')
    )
    q_a = models.ForeignKey(QandA, related_name='q_and_a')
    helper = models.ForeignKey(Helper, related_name='helper')
    valid = models.CharField(max_length=3,choices=valid_options)
    status = models.CharField(max_length=13,choices=status_options,default='pending')

    def __str__(self):
        return str(self.id)
