# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-06-26 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='', max_length=50, verbose_name='\u8bfe\u7a0b\u7c7b\u522b'),
        ),
    ]