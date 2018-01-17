from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView

from ad_set.models import AdSet
from ad_set.serializers import AdSetSerializer

import os
import json
import logging
import traceback

logger = logging.getLogger(__name__)

class AdSetAll(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            # account_id = request.query_params.get('account_id', "0")

            ad_sets = AdSet.objects.all()

            serializer = AdSetSerializer(ad_sets, many=True)

            response_data['success'] = 'YES'
            response_data['total_count'] = len(ad_sets)
            response_data['data'] = serializer.data
        except Exception as e:
            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

class AdSetDetail(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            account_id = request.query_params.get('account_id', '0')

            # account_id = 'act_349408409'
            ad_sets = AdSet.objects.filter(account_id=account_id)

            serializer = AdSetSerializer(ad_sets, many=True)

            response_data['success'] = 'YES'
            response_data['total_count'] = len(ad_sets)
            response_data['data'] = serializer.data
        except Exception as e:
            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
