# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-12 17:53
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_auto_20180212_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 12, 18, 53, 13, 662357)),
        ),
        migrations.AlterField(
            model_name='controlpanel',
            name='threshold',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(1.0)]),
        ),
    ]
