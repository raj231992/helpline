"""dtss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('authentication.urls', namespace='authentication')),
    url(r'^web_auth/', include('web_auth.urls', namespace='web_auth')),
    url(r'^management/', include('management.urls', namespace='management')),
    url(r'^registercall/', include('registercall.urls', namespace='register_call')),
    url(r'^taskmanager/', include('task_manager.urls', namespace='task_manager')),
    url(r'^registerhelper/', include('register_helper.urls', namespace='register_helper')),
    url(r'^ivr/', include('ivr.urls', namespace='ivr')),
    url(r'^', include('dashboard.urls', namespace='dashboard')),
]

urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)