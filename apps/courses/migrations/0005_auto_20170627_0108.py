# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-06-27 01:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_lesson_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='url',
        ),
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='\u8bbf\u95ee\u94fe\u63a5'),
        ),
    ]
