# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-10 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='McCenterAccount',
            fields=[
                ('centeraccountid', models.AutoField(db_column='centerAccountId', primary_key=True, serialize=False)),
                ('accounttype', models.CharField(blank=True, db_column='accountType', max_length=30, null=True)),
                ('advertiserid', models.IntegerField(db_column='advertiserId')),
                ('masteraccountid', models.CharField(blank=True, db_column='masterAccountId', max_length=100, null=True)),
                ('selfaccountid', models.CharField(blank=True, db_column='selfAccountId', max_length=100, null=True)),
                ('authusername', models.CharField(blank=True, db_column='authUsername', max_length=50, null=True)),
                ('authpassword', models.CharField(blank=True, db_column='authPassword', max_length=20, null=True)),
                ('reportstartday', models.CharField(blank=True, db_column='reportStartDay', max_length=10, null=True)),
                ('firstgetreportdate', models.DateTimeField(blank=True, db_column='firstGetReportDate', null=True)),
                ('monthlybudget', models.IntegerField(blank=True, db_column='monthlyBudget', null=True)),
                ('diamond', models.CharField(blank=True, max_length=6, null=True)),
                ('level', models.CharField(blank=True, max_length=30, null=True)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('localaccountid', models.CharField(blank=True, db_column='localAccountId', max_length=50, null=True)),
                ('accountnickname', models.CharField(blank=True, db_column='accountNickName', max_length=100, null=True)),
                ('reg_date', models.DateTimeField()),
                ('mod_date', models.DateTimeField()),
                ('mod_user', models.CharField(blank=True, max_length=50, null=True)),
                ('usegoogleconversion', models.CharField(blank=True, db_column='useGoogleConversion', max_length=6, null=True)),
                ('siteurl', models.CharField(blank=True, db_column='siteUrl', max_length=255, null=True)),
                ('balancetype', models.CharField(blank=True, db_column='balanceType', max_length=30, null=True)),
                ('rankingmedia', models.CharField(blank=True, db_column='rankingMedia', max_length=100, null=True)),
                ('enableautogathering', models.CharField(blank=True, db_column='enableAutoGathering', max_length=6, null=True)),
                ('neotouchauthkey', models.CharField(blank=True, db_column='neoTouchAuthKey', max_length=255, null=True)),
                ('bingompfser', models.CharField(blank=True, db_column='bingoMpfSer', max_length=32, null=True)),
            ],
            options={
                'db_table': 'MC_CENTER_ACCOUNT',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='McCenterAdvertiser',
            fields=[
                ('advertiserid', models.AutoField(db_column='advertiserId', primary_key=True, serialize=False)),
                ('advertisername', models.CharField(db_column='advertiserName', max_length=100)),
                ('loginid', models.CharField(db_column='loginId', max_length=50, unique=True)),
                ('homeurl', models.CharField(blank=True, db_column='homeUrl', max_length=255, null=True)),
                ('logourl', models.CharField(blank=True, db_column='logoUrl', max_length=300, null=True)),
                ('menuclass', models.CharField(blank=True, db_column='menuClass', max_length=20, null=True)),
                ('trackingdaycount', models.IntegerField(blank=True, db_column='trackingDayCount', null=True)),
                ('enableroi', models.CharField(blank=True, db_column='enableRoi', max_length=6, null=True)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('reg_date', models.DateTimeField()),
                ('mod_date', models.DateTimeField()),
                ('mod_user', models.CharField(blank=True, max_length=50, null=True)),
                ('enablecategory', models.CharField(blank=True, db_column='enableCategory', max_length=6, null=True)),
                ('enablenotice', models.CharField(blank=True, db_column='enableNotice', max_length=6, null=True)),
                ('enabledashboard', models.CharField(blank=True, db_column='enableDashboard', max_length=6, null=True)),
                ('enablereporting', models.CharField(blank=True, db_column='enableReporting', max_length=6, null=True)),
                ('enablebidding', models.CharField(blank=True, db_column='enableBidding', max_length=6, null=True)),
                ('enableissuekeyword', models.CharField(blank=True, db_column='enableIssueKeyword', max_length=6, null=True)),
                ('enablekeywordfinder', models.CharField(blank=True, db_column='enableKeywordFinder', max_length=6, null=True)),
                ('enablelpmonitor', models.CharField(blank=True, db_column='enableLpMonitor', max_length=6, null=True)),
                ('enablerankmonitor', models.CharField(blank=True, db_column='enableRankMonitor', max_length=6, null=True)),
                ('enabledrfadmin', models.CharField(blank=True, db_column='enableDrfAdmin', max_length=6, null=True)),
                ('enabledrfnotice', models.CharField(blank=True, db_column='enableDrfNotice', max_length=6, null=True)),
                ('enabledrfreporting', models.CharField(blank=True, db_column='enableDrfReporting', max_length=6, null=True)),
                ('enableadmin', models.CharField(blank=True, db_column='enableAdmin', max_length=6, null=True)),
                ('enablescheduling', models.CharField(blank=True, db_column='enableScheduling', max_length=6, null=True)),
                ('enablecaos', models.CharField(blank=True, db_column='enableCaos', max_length=6, null=True)),
                ('bingoadvser', models.CharField(blank=True, db_column='bingoAdvSer', max_length=16, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'MC_CENTER_ADVERTISER',
            },
        ),
        migrations.CreateModel(
            name='McRoiReport',
            fields=[
                ('roireportid', models.BigAutoField(db_column='roiReportId', primary_key=True, serialize=False)),
                ('reg_date', models.DateTimeField(blank=True, null=True)),
                ('mod_date', models.DateTimeField(blank=True, null=True)),
                ('mod_user', models.CharField(blank=True, max_length=50, null=True)),
                ('centerroiid', models.BigIntegerField(db_column='centerRoiId')),
                ('centerpageid', models.CharField(db_column='centerPageId', max_length=255)),
                ('centeraccountid', models.IntegerField(blank=True, db_column='centerAccountId', null=True)),
                ('accounttype', models.CharField(blank=True, db_column='accountType', max_length=30, null=True)),
                ('keywordid', models.BigIntegerField(blank=True, db_column='keywordId', null=True)),
                ('roireportday', models.CharField(db_column='roiReportDay', max_length=10)),
                ('roireporttime', models.CharField(blank=True, db_column='roiReportTime', max_length=8, null=True)),
                ('campaignid', models.BigIntegerField(blank=True, db_column='campaignId', null=True)),
                ('adgroupid', models.BigIntegerField(blank=True, db_column='adGroupId', null=True)),
                ('mediaid', models.CharField(blank=True, db_column='mediaId', max_length=64, null=True)),
                ('directory', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('views', models.BigIntegerField(blank=True, null=True)),
                ('purchaseprice', models.FloatField(blank=True, db_column='purchasePrice', null=True)),
                ('returnfulldata', models.TextField(blank=True, db_column='returnFullData', null=True)),
                ('accountname', models.CharField(blank=True, db_column='accountName', max_length=255, null=True)),
                ('adgroupname', models.CharField(blank=True, db_column='adGroupName', max_length=255, null=True)),
                ('campaignname', models.CharField(blank=True, db_column='campaignName', max_length=255, null=True)),
                ('keywordname', models.CharField(blank=True, db_column='keywordName', max_length=255, null=True)),
                ('reg_user', models.CharField(blank=True, max_length=50, null=True)),
                ('searchkeyword', models.CharField(blank=True, db_column='searchKeyword', max_length=255, null=True)),
                ('landingtime', models.DateTimeField(blank=True, db_column='landingTime', null=True)),
                ('assistantkeywordname', models.CharField(blank=True, db_column='assistantKeywordName', max_length=255, null=True)),
                ('assistantaccounttype', models.CharField(blank=True, db_column='assistantAccountType', max_length=255, null=True)),
                ('centerroiname', models.CharField(blank=True, db_column='centerRoiName', max_length=255, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
    ]
