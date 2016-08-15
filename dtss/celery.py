"""
Settings file for celery
"""

import os

from celery import Celery
from django import setup
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtss.settings.local')
setup()

app = Celery('dtss')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
