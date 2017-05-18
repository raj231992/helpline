# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-05-18 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivr', '0007_call_forward_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call_forward_details',
            name='status',
            field=models.CharField(choices=[('initiated', 'initiated'), ('not_answered', 'not_answered'), ('completed', 'completed')], default='initiated', max_length=15),
        ),
    ]
