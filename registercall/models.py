"""
Register Call Models
"""
from django.db import models
from management.models import HelpLine,HelperCategory
from register_client.models import Client
from registercall.options import (CallRequestStatusOptions,
                                         ClientStatusOptions,
                                         TaskStatusOptions)







class CallRequest(models.Model):
    """
    Model for storing incoming call requests
        Calls for whom task is already pending is merged
        Calls for whom client is blocked is blocked
        If above two condition fails is when task is created

    Refers to helpline and client
    """

    helpline = models.ForeignKey(HelpLine, related_name='call_requests')
    client = models.ForeignKey(Client, related_name='call_requests')

    created = models.DateTimeField('Created Timestamp', auto_now_add=True)

    status = models.IntegerField(
        default=CallRequestStatusOptions.CREATED,
        choices=CallRequestStatusOptions.STATUS_CHOICES,
    )

    def __str__(self):
        return str(self.pk)


class Task(models.Model):
    """
    Model for the actual Tasks created
    Creates only when request is valid and task not already pending

    Refers to call request
    """
    # Each helper may belong to more than one category
    call_request = models.ForeignKey(CallRequest, related_name='tasks')
    category = models.ForeignKey(
        HelperCategory,
        related_name='tasks',
        default=None,
        blank=True,
        null=True,
    )

    created = models.DateTimeField('Created Timestamp', auto_now_add=True)
    modified = models.DateTimeField('Modified Timestamp', auto_now=True)

    status = models.IntegerField(
        default=TaskStatusOptions.PENDING,
        choices=TaskStatusOptions.STATUS_CHOICES,
    )

    def __str__(self):
        return str(self.pk)
