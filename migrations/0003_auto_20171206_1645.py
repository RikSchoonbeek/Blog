# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-06 15:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 6, 15, 45, 3, 467076, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
