# Generated by Django 2.0 on 2017-12-26 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fb_ad_account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fbadaccount',
            name='account_category',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='account_category.AccountCategory'),
        ),
    ]