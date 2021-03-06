# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-08 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fb_ad_account', '0002_auto_20171226_1229'),
        ('account_pixel_mapping', '0002_auto_20171226_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountpixelmapping',
            name='event_mapping_name',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountpixelmapping',
            name='fb_ad_account',
            field=models.ForeignKey(db_constraint=False, default='', on_delete=django.db.models.deletion.CASCADE, to='fb_ad_account.FbAdAccount'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountpixelmapping',
            name='pixel_event_name',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
