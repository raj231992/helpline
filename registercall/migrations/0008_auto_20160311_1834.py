# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-11 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registercall', '0007_auto_20160311_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='helpercategory',
            old_name='category',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='helper',
            name='category',
            field=models.ManyToManyField(to='registercall.HelperCategory'),
        ),
    ]
