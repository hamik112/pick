from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from neo_db.models import (McCenterAdvertiser, McCenterAccount, McRoiReport)
from neo_db.serializers import (McCenterAdvertiserSerializer, McCenterAccountSerializer, McRoiReportSerializer)
from django.conf import settings
from neo_account.models import NeoAccount

import json
import logging
import traceback
import pprint

pp = pprint.PrettyPrinter(indent=4)

@csrf_exempt
def get_neo_advertisers(request):
    response_data = {}
    try:
        advs = McCenterAdvertiser.get_all_advertisers(McCenterAdvertiser)
        serializer = McCenterAdvertiserSerializer(advs, many=True)

        response_data['success'] = 'YES'
        response_data['total_count'] = len(serializer.data)
        response_data['data'] = serializer.data

        response_data['success'] = 'YES'
    except Exception as e:
        response_data['success'] = 'NO'
        response_data['msg'] = e
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def get_neo_accounts(request):
    response_data = {}
    try:
        fbadaccounts = McCenterAccount.objects.using('neo_v1_db').all()
        serializer = McCenterAccountSerializer(fbadaccounts, many=True)

        response_data['success'] = 'YES'
        response_data['total_count'] = len(serializer.data)
        response_data['data'] = serializer.data

    except Exception as e:
        response_data['success'] = 'NO'
        response_data['msg'] = e
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def search_neo_accounts_by_adv_name(request):
    response_data = {}
    try:
        adv_name = request.GET.get('adv_name', None)
        search_advs = McCenterAdvertiser.get_search_advertisers(McCenterAdvertiser, adv_name)

        adv_ids = []
        adv_dic = {}

        for adv in search_advs:
            adv_ids.append(adv.advertiserid)
            adv_dic[adv.advertiserid] = adv

        fbadaccounts = McCenterAccount.objects.using('neo_v1_db').filter(advertiserid__in = adv_ids)
        serializer = McCenterAccountSerializer(fbadaccounts, many=True)

        return_data = []
        for data in serializer.data:
            adv_id = data.get('advertiserid')

            data['advertisername'] = adv_dic[adv_id].advertisername
            return_data.append(data)

        response_data['success'] = 'YES'
        response_data['total_count'] = len(serializer.data)
        response_data['data'] = return_data

    except Exception as e:
        response_data['success'] = 'NO'
        response_data['msg'] = e
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def get_roi_report(request):
    response_data = {}
    try:
        fb_ad_account_id = request.GET.get('fb_ad_account_id', 0)
        # adv_id = request.GET.get('adv_id', 0)
        neo_report_type = request.GET.get('type', '')

        if fb_ad_account_id == 0:
            raise Exception('No fb_ad_account_id ID.')

        day = settings.ROI_REPORT_DAYS

        neo_accounts = NeoAccount.get_list_by_fb_ad_account_id(NeoAccount, fb_ad_account_id)
        print("neo_accounts : ", neo_accounts)

        adv_id = None
        account_ids = []

        for neo_account in neo_accounts:
            adv_id = neo_account.get('neo_adv_id')
            account_ids.append(neo_account.get('neo_account_id'))

        if adv_id == None:
            raise Exception('No NeoAccount.')

        print("adv_id : ", adv_id)

        if neo_report_type == "account":
            roi_report = McRoiReport.get_media_roi_report(McRoiReport, adv_id, account_ids, day=day)
        elif neo_report_type == "campaign":
            roi_report = McRoiReport.get_campaign_roi_report(McRoiReport, adv_id, account_ids, day=day)
        elif neo_report_type == "keyword":
            roi_report = McRoiReport.get_keyword_roi_report(McRoiReport, adv_id, account_ids, day=day)
        else:
            roi_report = McRoiReport.get_media_roi_report(McRoiReport, adv_id, account_ids, day=day)

        response_data['success'] = 'YES'
        response_data['total_count'] = len(roi_report)
        response_data['data'] = roi_report
    except Exception as e:
        response_data['success'] = 'NO'
        response_data['msg'] = e
    return HttpResponse(json.dumps(response_data), content_type="application/json")


