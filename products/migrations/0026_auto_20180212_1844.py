# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-12 17:44
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_auto_20180212_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 12, 18, 44, 57, 71208)),
        ),
        migrations.AlterField(
            model_name='controlpanel',
            name='threshold',
            field=models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(-1.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
    ]
