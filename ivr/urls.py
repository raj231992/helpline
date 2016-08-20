from django.conf.urls import url

from .views import IVR

urlpatterns = [
    url(r'^$', IVR.as_view(), name='getHelplines'),

]