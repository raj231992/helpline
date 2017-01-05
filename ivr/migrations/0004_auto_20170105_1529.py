# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-01-05 09:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20160812_2031'),
        ('ivr', '0003_auto_20160923_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='IVR_Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(upload_to='ivr_audio/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.HelperCategory')),
                ('helpline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.HelpLine')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=20)),
                ('helpline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.HelpLine')),
            ],
        ),
        migrations.AlterField(
            model_name='ivr_call',
            name='session_next',
            field=models.CharField(choices=[(0, b'welcome'), (1, b'display_option'), (2, b'get_option'), (3, b'call_exit'), (4, b'call_forward')], max_length=256),
        ),
        migrations.AddField(
            model_name='ivr_audio',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ivr.Language'),
        ),
    ]
