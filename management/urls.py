from django.conf.urls import url

from .views import (getHelplines,getHelperProfile,getHelplineCategories,setHelperProfile,getHelperTasks,
                    HelperAccept,getHelplineNumber,getQandA,TaskComplete,CallForward,ActivateHelper)

urlpatterns = [
    url(r'^gethelplines/$', getHelplines.as_view(), name='getHelplines'),
    url(r'^getHelplineNumber/$', getHelplineNumber.as_view(), name='getHelplineNumber'),
    url(r'^getHelperProfile/$', getHelperProfile.as_view(), name='getHelperProfile'),
    url(r'^setHelperProfile/$', setHelperProfile.as_view(), name='setHelperProfile'),
    url(r'^getHelplineCategories/$', getHelplineCategories.as_view(), name='getHelplineCategories'),
    url(r'^getHelperTasks/$', getHelperTasks.as_view(), name='getHelperTasks'),
    url(r'^HelperAccept/$', HelperAccept.as_view(), name='HelperAccept'),
    url(r'^getQandA/$', getQandA.as_view(), name='getQandA'),
    url(r'^TaskComplete/$', TaskComplete.as_view(), name='TaskComplete'),
    url(r'^CallForward/$', CallForward.as_view(), name='CallForward'),
    url(r'^activateHelper/(?P<id>[0-9]+)$', ActivateHelper.as_view(), name='ActivateHelper'),


]
