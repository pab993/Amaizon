# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-27 11:12
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20180117_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControlPanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.AlterField(
            model_name='assessment',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 27, 12, 12, 48, 969390)),
        ),
    ]
