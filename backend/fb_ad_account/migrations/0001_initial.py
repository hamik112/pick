# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-20 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FbAdAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=64)),
                ('updated_by', models.CharField(max_length=64)),
                ('ad_account_id', models.BigIntegerField()),
                ('act_account_id', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=128)),
                ('account_status', models.IntegerField(default=2)),
                ('account_category', models.IntegerField(choices=[(0, 'Default Cateogry'), (1, 'Loan'), (2, 'NGO'), (3, 'Card'), (4, 'Travel'), (5, 'Shopping Mall'), (6, 'ETC'), (7, 'Insurance'), (8, 'Beauty')], default=0)),
            ],
            options={
                'db_table': 'fb_ad_accounts',
            },
        ),
    ]