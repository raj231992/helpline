# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-04-24 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivr', '0004_auto_20170424_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='isCallRaised',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feedback',
            name='isFeedbackTaken',
            field=models.BooleanField(default=False),
        ),
    ]