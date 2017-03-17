from django.conf.urls import url

from .views import IVR, Feedback


urlpatterns = [
    url(r'^feedback/$', Feedback.as_view(), name='getFeedback'),
    url(r'^$', IVR.as_view(), name='getHelplines'),
]
