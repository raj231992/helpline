# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-05 14:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('registercall', '0004_auto_20160305_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='helper',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 5, 14, 37, 9, 432246, tzinfo=utc), verbose_name='Created Timestamp'),
        ),
    ]
