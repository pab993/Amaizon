# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-05 12:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20171029_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
