# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-02 20:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20171001_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='globalstatistic',
            name='pair_y_r',
        ),
    ]