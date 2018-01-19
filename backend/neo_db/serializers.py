from neo_db.models import (McCenterAdvertiser, McCenterAccount, McRoiReport)
from rest_framework import serializers


class McCenterAdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = McCenterAdvertiser
        fields = (
            'advertiserid', 'advertisername', 'loginid', 'homeurl', 'logourl', 'menuclass', 'trackingdaycount',
            'enableroi', 'status', 'reg_date', 'mod_date', 'mod_user', 'enablecategory', 'enablenotice',
            'enabledashboard', 'enablereporting', 'enablebidding', 'enableissuekeyword', 'enablekeywordfinder',
            'enablelpmonitor', 'enablerankmonitor', 'enabledrfadmin', 'enabledrfnotice', 'enabledrfreporting',
            'enableadmin', 'enablescheduling', 'enablecaos', 'bingoadvser')

class McCenterAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = McCenterAccount
        fields = (
            'centeraccountid', 'accounttype', 'advertiserid', 'masteraccountid', 'selfaccountid', 'authusername',
            'authpassword', 'reportstartday', 'firstgetreportdate', 'monthlybudget', 'diamond', 'level', 'status',
            'localaccountid', 'accountnickname', 'reg_date', 'mod_date', 'mod_user', 'usegoogleconversion', 'siteurl',
            'balancetype', 'rankingmedia', 'enableautogathering', 'neotouchauthkey', 'bingompfser')


class McRoiReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = McRoiReport
        fields = (
            'roireportid', 'reg_date', 'mod_date', 'mod_user', 'centerroiid', 'centerpageid', 'centeraccountid',
            'accounttype', 'keywordid', 'roireportday', 'roireporttime', 'campaignid', 'adgroupid', 'mediaid',
            'directory', 'category', 'views', 'purchaseprice', 'returnfulldata', 'accountname', 'adgroupname',
            'campaignname', 'keywordname', 'reg_user', 'searchkeyword', 'landingtime', 'assistantkeywordname',
            'assistantaccounttype', 'centerroiname')
