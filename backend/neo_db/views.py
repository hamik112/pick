from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from neo_db.models import (McCenterAdvertiser, McCenterAccount, McRoiReport)
from neo_db.serializers import (McCenterAdvertiserSerializer, McCenterAccountSerializer, McRoiReportSerializer)


import json
import logging
import traceback
import pprint

pp = pprint.PrettyPrinter(indent=4)

@csrf_exempt
def get_neo_advertisers(request):
    response_data = {}
    try:
        advs = McCenterAdvertiser.objects.using('neo_v1_db').all()
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
def get_roi_report(request):
    response_data = {}
    try:
        adv_id = request.GET.get('adv_id', 0)

        if adv_id == 0:
            raise Exception('No Advertiser ID.')

        McRoiReport._meta.db_table = "MC_ROI_REPORT_ADV_" + str(adv_id)
        roi_report = McRoiReport.objects.using('neo_v1_db').all()

        serializer = McRoiReportSerializer(roi_report, many=True)

        response_data['success'] = 'YES'
        response_data['total_count'] = len(serializer.data)
        response_data['data'] = serializer.data
    except Exception as e:
        response_data['success'] = 'NO'
        response_data['msg'] = e
    return HttpResponse(json.dumps(response_data), content_type="application/json")


