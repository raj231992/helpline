from django.conf.urls import url
from .views import Home,Helper_Profile,Yearly_Stats,Task_Details


urlpatterns = [
url(r'^$', Home.as_view(), name='home'),
url(r'^helper_profile/(?P<pk>[0-9]+)/(?P<cat>[a-zA-Z]+)/(?P<year>[0-9]{4})/', Helper_Profile.as_view(), name='helper_profile'),
url(r'^yearly_stats/(?P<cat>[a-zA-Z]+)/(?P<year>[0-9]{4})/', Yearly_Stats.as_view(), name='yearly_stats'),
url(r'^task_details/(?P<pk>[0-9]+)/', Task_Details.as_view(), name='task_details'),
]