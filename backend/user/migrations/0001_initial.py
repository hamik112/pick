# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-12 14:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=64)),
                ('updated_by', models.CharField(max_length=64)),
                ('username', models.CharField(max_length=64, unique=True)),
                ('password_digest', models.CharField(blank=True, max_length=128, null=True)),
                ('email', models.CharField(blank=True, max_length=128, null=True)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('fb_access_token', models.CharField(blank=True, max_length=255, null=True)),
                ('role', models.CharField(max_length=32)),
                ('language', models.CharField(default='ko', max_length=128)),
                ('login_id', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('age', models.IntegerField(default=0)),
                ('gender', models.CharField(default=None, max_length=16, null=True)),
                ('picture_url', models.CharField(blank=True, default='', max_length=255)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]