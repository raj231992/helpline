# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-01-05 17:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ivr', '0012_auto_20170105_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='misc_audio',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ivr.Misc_Category'),
        ),
    ]
