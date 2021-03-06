# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-16 06:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        ('sports', '0005_sport_sport_image'),
        ('playground', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='playground_destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playground.Playground'),
        ),
        migrations.AddField(
            model_name='event',
            name='sport_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports.Sport'),
        ),
    ]
