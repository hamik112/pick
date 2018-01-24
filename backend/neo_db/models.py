# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import connections
from django.db import models
from django.db.models import Count
from utils.common import date_formatter

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

    def get_all_advertisers(self):
        advs = McCenterAdvertiser.objects.using('neo_v1_db').all()

        return advs

    def get_search_advertisers(self, search_text):
        advs = McCenterAdvertiser.objects.using('neo_v1_db').filter(advertisername__contains=search_text)
        return advs

    def get_advertisers_by_ids(self, adv_ids):
        advs =  McCenterAdvertiser.objects.using('neo_v1_db').filter(advertiserid__in=adv_ids)
        return advs

    def get_advertiser(self, id):
        adv = McCenterAdvertiser.objects.using('neo_v1_db').get(pk=id)
        return adv

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

    def get_accounts_by_ids(self, account_ids):
        advs =  McCenterAccount.objects.using('neo_v1_db').filter(centeraccountid__in=account_ids)
        return advs

    class Meta:
        managed = False
        db_table = 'MC_CENTER_ACCOUNT'
        unique_together = (('accounttype', 'advertiserid', 'status', 'accountnickname'),)


class McRoiReport(models.Model):
    roireportid = models.BigAutoField(db_column='roiReportId', primary_key=True)  # Field name made lowercase.
    reg_date = models.DateTimeField(blank=True, null=True)
    mod_date = models.DateTimeField(blank=True, null=True)
    mod_user = models.CharField(max_length=50, blank=True, null=True)
    centerroiid = models.BigIntegerField(db_column='centerRoiId')  # Field name made lowercase.
    centerpageid = models.CharField(db_column='centerPageId', max_length=255)  # Field name made lowercase.
    centeraccountid = models.IntegerField(db_column='centerAccountId', blank=True, null=True)  # Field name made lowercase.
    accounttype = models.CharField(db_column='accountType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    keywordid = models.BigIntegerField(db_column='keywordId', blank=True, null=True)  # Field name made lowercase.
    roireportday = models.CharField(db_column='roiReportDay', max_length=10)  # Field name made lowercase.
    roireporttime = models.CharField(db_column='roiReportTime', max_length=8, blank=True, null=True)  # Field name made lowercase.
    campaignid = models.BigIntegerField(db_column='campaignId', blank=True, null=True)  # Field name made lowercase.
    adgroupid = models.BigIntegerField(db_column='adGroupId', blank=True, null=True)  # Field name made lowercase.
    mediaid = models.CharField(db_column='mediaId', max_length=64, blank=True, null=True)  # Field name made lowercase.
    directory = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    views = models.BigIntegerField(blank=True, null=True)
    purchaseprice = models.FloatField(db_column='purchasePrice', blank=True, null=True)  # Field name made lowercase.
    returnfulldata = models.TextField(db_column='returnFullData', blank=True, null=True)  # Field name made lowercase.
    accountname = models.CharField(db_column='accountName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adgroupname = models.CharField(db_column='adGroupName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    campaignname = models.CharField(db_column='campaignName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    keywordname = models.CharField(db_column='keywordName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    reg_user = models.CharField(max_length=50, blank=True, null=True)
    searchkeyword = models.CharField(db_column='searchKeyword', max_length=255, blank=True, null=True)  # Field name made lowercase.
    landingtime = models.DateTimeField(db_column='landingTime', blank=True, null=True)  # Field name made lowercase.
    assistantkeywordname = models.CharField(db_column='assistantKeywordName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    assistantaccounttype = models.CharField(db_column='assistantAccountType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    centerroiname = models.CharField(db_column='centerRoiName', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def get_media_roi_report(self, adv_id, account_ids, day=30, adv_info={"adv_id": 0,"adv_name": ""}):
        # print("adv_id : ", adv_id)
        # print("account_ids : ", account_ids)
        # print("adv_info : ", adv_info)
        # print("get_media_roi_report table : ", "MC_ROI_REPORT_ADV_" + str(adv_id))
        calday = date_formatter.caldate(day)

        query = '''
            SELECT centerAccountId, accountName, count(roiReportId) as count
            FROM MC_ROI_REPORT_ADV_'''+ str(adv_id) +'''
            WHERE centerAccountId in ''' + str(tuple(account_ids)) + '''
            AND roiReportDay >= ''' + str(calday) + '''
            GROUP BY centerAccountId
            ORDER BY count DESC
        '''

        cursor = connections['neo_v1_db'].cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return_data = []

        for roi_obj in result:
            return_data.append({
                "advid": adv_info.get('adv_id'),
                "advname": adv_info.get('adv_name'),
                "centeraccountid":roi_obj[0],
                "accountname": roi_obj[1],
                "count": roi_obj[2],
                "param" : str(adv_id) + "." + str(roi_obj[0])
            })

        return return_data

    def get_campaign_roi_report(self, adv_id, account_ids, day=30, adv_info={"adv_id": 0,"adv_name": ""}):
        # print("get_campaign_roi_report")
        # print("adv_id : ", adv_id)
        # print("account_ids : ", account_ids)
        # print("adv_info : ", adv_info)
        # print("get_media_roi_report table : ", "MC_ROI_REPORT_ADV_" + str(adv_id))
        calday = date_formatter.caldate(day)

        query = '''
            SELECT centerAccountId, accountName, campaignId, campaignName, count(roiReportId) as count
            FROM MC_ROI_REPORT_ADV_'''+ str(adv_id) +'''
            WHERE centerAccountId in ''' + str(tuple(account_ids)) + '''
            AND roiReportDay >= ''' + str(calday) + '''
            GROUP BY centerAccountId, campaignId
            ORDER BY count DESC
        '''

        print(query)

        # McRoiReport._meta.db_table = "MC_ROI_REPORT_ADV_" + str(adv_id)
        # roi_report = McRoiReport.objects.using('neo_v1_db').filter(roireportday__gte=date_formatter.caldate(day), centeraccountid__in=account_ids).values('centeraccountid', 'accountname', 'campaignid', 'campaignname').annotate(count=Count('roireportid')).order_by('-count')[:200]
        # print(roi_report.query)
        # print(roi_report)

        cursor = connections['neo_v1_db'].cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return_data = []

        for roi_obj in result:
            return_data.append({
                "advid": adv_info.get('adv_id'),
                "advname": adv_info.get('adv_name'),
                "centeraccountid":roi_obj[0],
                "accountname": roi_obj[1],
                "campaignid": roi_obj[2],
                "campaignname": roi_obj[3],
                "count": roi_obj[4],
                "param": str(adv_id) + "." + str(roi_obj[0]) + "." + str(roi_obj[2])
            })

        return return_data


    def get_keyword_roi_report(self, adv_id, account_ids, day=30, adv_info={"adv_id": 0,"adv_name": ""}):
        print("get_keyword_roi_report")
        # print("adv_id : ", adv_id)
        # print("account_ids : ", account_ids)
        # print("adv_info : ", adv_info)
        # print("get_media_roi_report table : ", "MC_ROI_REPORT_ADV_" + "MC_ROI_REPORT_ADV_" + str(adv_id))

        calday = date_formatter.caldate(day)

        query = '''
            SELECT centerAccountId, accountName, campaignId, campaignName, keywordId, keywordName, count(roiReportId) as count
            FROM MC_ROI_REPORT_ADV_'''+ str(adv_id) +'''
            WHERE roiReportDay >= ''' + str(calday) + '''
            AND centerAccountId in ''' + str(tuple(account_ids)) + '''
            GROUP BY centerAccountId, campaignId, keywordId
            ORDER BY count DESC
            LIMIT 200
        '''
        print(query)

        # McRoiReport._meta.db_table = "MC_ROI_REPORT_ADV_" + str(adv_id)
        # roi_report = McRoiReport.objects.using('neo_v1_db').filter(roireportday__gte=date_formatter.caldate(day), centeraccountid__in=account_ids).values('centeraccountid', 'accountname', 'campaignid', 'campaignname', 'keywordid', 'keywordname').annotate(count=Count('roireportid')).order_by('-count')[:200]
        cursor = connections['neo_v1_db'].cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return_data = []

        for roi_obj in result:
            return_data.append({
                "advid": adv_info.get('adv_id'),
                "advname": adv_info.get('adv_name'),
                "centeraccountid":roi_obj[0],
                "accountname": roi_obj[1],
                "campaignid": roi_obj[2],
                "campaignname": roi_obj[3],
                "keywordid": roi_obj[4],
                "keywordname": roi_obj[5],
                "count": roi_obj[6],
                "param": str(adv_id) + "." + str(roi_obj[0]) + "." + str(roi_obj[2]) + "." + str(roi_obj[4])
            })

        return return_data


    class Meta:
        managed = False
