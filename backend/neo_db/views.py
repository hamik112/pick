from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from neo_db.models import McCenterAdvertiser
from neo_db.models import McCenterAccount

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
        print(advs)

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
        print(fbadaccounts)

        response_data['success'] = 'YES'
    except Exception as e:
        response_data['success'] = 'NO'
        response_data['msg'] = e
    return HttpResponse(json.dumps(response_data), content_type="application/json")

