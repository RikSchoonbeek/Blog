# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-06 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20171206_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.DateField(),
        ),
    ]
