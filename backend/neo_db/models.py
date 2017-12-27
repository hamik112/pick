# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class McCenterAdvertiser(models.Model):
    advertiserid = models.AutoField(db_column='advertiserId', primary_key=True)  # Field name made lowercase.
    advertisername = models.CharField(db_column='advertiserName', max_length=100)  # Field name made lowercase.
    loginid = models.CharField(db_column='loginId', unique=True, max_length=50)  # Field name made lowercase.
    homeurl = models.CharField(db_column='homeUrl', max_length=255, blank=True, null=True)  # Field name made lowercase.
    logourl = models.CharField(db_column='logoUrl', max_length=300, blank=True, null=True)  # Field name made lowercase.
    menuclass = models.CharField(db_column='menuClass', max_length=20, blank=True, null=True)  # Field name made lowercase.
    trackingdaycount = models.IntegerField(db_column='trackingDayCount', blank=True, null=True)  # Field name made lowercase.
    enableroi = models.CharField(db_column='enableRoi', max_length=6, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=30, blank=True, null=True)
    reg_date = models.DateTimeField()
    mod_date = models.DateTimeField()
    mod_user = models.CharField(max_length=50, blank=True, null=True)
    enablecategory = models.CharField(db_column='enableCategory', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enablenotice = models.CharField(db_column='enableNotice', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enabledashboard = models.CharField(db_column='enableDashboard', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enablereporting = models.CharField(db_column='enableReporting', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enablebidding = models.CharField(db_column='enableBidding', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enableissuekeyword = models.CharField(db_column='enableIssueKeyword', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enablekeywordfinder = models.CharField(db_column='enableKeywordFinder', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enablelpmonitor = models.CharField(db_column='enableLpMonitor', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enablerankmonitor = models.CharField(db_column='enableRankMonitor', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enabledrfadmin = models.CharField(db_column='enableDrfAdmin', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enabledrfnotice = models.CharField(db_column='enableDrfNotice', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enabledrfreporting = models.CharField(db_column='enableDrfReporting', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enableadmin = models.CharField(db_column='enableAdmin', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enablescheduling = models.CharField(db_column='enableScheduling', max_length=6, blank=True, null=True)  # Field name made lowercase.
    enablecaos = models.CharField(db_column='enableCaos', max_length=6, blank=True, null=True)  # Field name made lowercase.
    bingoadvser = models.CharField(db_column='bingoAdvSer', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MC_CENTER_ADVERTISER'


class McCenterAccount(models.Model):
    centeraccountid = models.AutoField(db_column='centerAccountId', primary_key=True)  # Field name made lowercase.
    accounttype = models.CharField(db_column='accountType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    advertiserid = models.IntegerField(db_column='advertiserId')  # Field name made lowercase.
    masteraccountid = models.CharField(db_column='masterAccountId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    selfaccountid = models.CharField(db_column='selfAccountId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    authusername = models.CharField(db_column='authUsername', max_length=50, blank=True, null=True)  # Field name made lowercase.
    authpassword = models.CharField(db_column='authPassword', max_length=20, blank=True, null=True)  # Field name made lowercase.
    reportstartday = models.CharField(db_column='reportStartDay', max_length=10, blank=True, null=True)  # Field name made lowercase.
    firstgetreportdate = models.DateTimeField(db_column='firstGetReportDate', blank=True, null=True)  # Field name made lowercase.
    monthlybudget = models.IntegerField(db_column='monthlyBudget', blank=True, null=True)  # Field name made lowercase.
    diamond = models.CharField(max_length=6, blank=True, null=True)
    level = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    localaccountid = models.CharField(db_column='localAccountId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    accountnickname = models.CharField(db_column='accountNickName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    reg_date = models.DateTimeField()
    mod_date = models.DateTimeField()
    mod_user = models.CharField(max_length=50, blank=True, null=True)
    usegoogleconversion = models.CharField(db_column='useGoogleConversion', max_length=6, blank=True, null=True)  # Field name made lowercase.
    siteurl = models.CharField(db_column='siteUrl', max_length=255, blank=True, null=True)  # Field name made lowercase.
    balancetype = models.CharField(db_column='balanceType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    rankingmedia = models.CharField(db_column='rankingMedia', max_length=100, blank=True, null=True)  # Field name made lowercase.
    enableautogathering = models.CharField(db_column='enableAutoGathering', max_length=6, blank=True, null=True)  # Field name made lowercase.
    neotouchauthkey = models.CharField(db_column='neoTouchAuthKey', max_length=255, blank=True, null=True)  # Field name made lowercase.
    bingompfser = models.CharField(db_column='bingoMpfSer', max_length=32, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MC_CENTER_ACCOUNT'
        unique_together = (('accounttype', 'advertiserid', 'status', 'accountnickname'),)
