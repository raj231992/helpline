# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-05-18 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivr', '0008_auto_20170518_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call_forward_details',
            name='status',
            field=models.CharField(choices=[('not_answered', 'not_answered'), ('completed', 'completed')], default='not_answered', max_length=15),
        ),
    ]