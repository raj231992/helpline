# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-08 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0003_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='status',
            field=models.CharField(choices=[(b'pending', b'pending'), (b'completed', b'completed')], default=b'pending', max_length=13),
        ),
    ]