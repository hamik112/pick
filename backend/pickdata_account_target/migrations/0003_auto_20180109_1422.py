# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-09 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pickdata_account_target', '0002_auto_20171226_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pickdataaccounttarget',
            name='extra_pixel_mapping_id',
        ),
        migrations.RemoveField(
            model_name='pickdataaccounttarget',
            name='rentention_days',
        ),
        migrations.AddField(
            model_name='pickdataaccounttarget',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
