# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-23 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsapp', '0005_auto_20180622_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='profile_picture/'),
        ),
    ]
