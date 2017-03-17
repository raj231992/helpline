from django.db import models
from django.contrib.auth.models import User
from .options import HelperStatusOptions,LoginStatus
from management.models import HelperCategory,HelpLine


class Helper(models.Model):
    """
    Model for details of people who are willing to help
    """

    # Each helper may belong to more than one category
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    helpline = models.ForeignKey(HelpLine,on_delete=models.CASCADE)
    category = models.ManyToManyField(HelperCategory,blank=True)
    helper_number = models.CharField(max_length=16,blank=True,null=True)
    gcm_canonical_id = models.CharField(max_length=256)

    # Rating goes from 0.00 to 5.00
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=2.5)

    created = models.DateTimeField('Created Timestamp', auto_now_add=True)
    last_assigned = models.DateTimeField('Last Assigned Timestamp', auto_now_add=True)


    status = models.IntegerField(
        default=HelperStatusOptions.ACTIVE,
        choices=HelperStatusOptions.STATUS_CHOICES,
    )

    login_status = models.IntegerField(
        default=LoginStatus.PENDING,
        choices=LoginStatus.STATUS_CHOICES,
    )

    def __str__(self):
        return str(self.user)

