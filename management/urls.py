from django.conf.urls import url

from .views import getHelplines,getHelperProfile,getHelplineCategories,setHelperProfile

urlpatterns = [
    url(r'^gethelplines/$', getHelplines.as_view(), name='getHelplines'),
    url(r'^getHelperProfile/$', getHelperProfile.as_view(), name='getHelperProfile'),
    url(r'^setHelperProfile/$', setHelperProfile.as_view(), name='setHelperProfile'),
    url(r'^getHelplineCategories/$', getHelplineCategories.as_view(), name='getHelplineCategories'),

]
