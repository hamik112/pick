# Generated by Django 2.0 on 2017-12-26 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_pixel_mapping', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountpixelmapping',
            name='event_mapping_name',
        ),
        migrations.RemoveField(
            model_name='accountpixelmapping',
            name='fb_ad_account',
        ),
        migrations.RemoveField(
            model_name='accountpixelmapping',
            name='pixel_event_name',
        ),
    ]
