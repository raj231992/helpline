from django.conf.urls import url

from .views import getHelplines

urlpatterns = [
    url(r'^gethelplines/$', getHelplines.as_view(), name='getHelplines'),

]
