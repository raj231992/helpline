from django.conf.urls import url

from .views import getHelplines,getHelperProfile,getHelplineCategories,setHelperProfile,getHelperTasks,HelperAccept,getHelplineNumber

urlpatterns = [
    url(r'^gethelplines/$', getHelplines.as_view(), name='getHelplines'),
    url(r'^getHelplineNumber/$', getHelplineNumber.as_view(), name='getHelplineNumber'),
    url(r'^getHelperProfile/$', getHelperProfile.as_view(), name='getHelperProfile'),
    url(r'^setHelperProfile/$', setHelperProfile.as_view(), name='setHelperProfile'),
    url(r'^getHelplineCategories/$', getHelplineCategories.as_view(), name='getHelplineCategories'),
    url(r'^getHelperTasks/$', getHelperTasks.as_view(), name='getHelperTasks'),
    url(r'^HelperAccept/$', HelperAccept.as_view(), name='HelperAccept'),


]
