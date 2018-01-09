from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView

from ad_set_insight.models import AdSetInsight
from ad_set_insight.serializers import AdSetInsightSerializer

import os
import json
import logging
import traceback

logger = logging.getLogger(__name__)

class AdSetInsightByAccount(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            ad_set_insights = None

            account_id = request.query_params.get('account_id', "0")
            page = request.query_params.get('page', '1')
            start = request.query_params.get('start', '0')
            limit = request.query_params.get('limit', '25')

            ad_set_insights = AdSetInsight.objects.filter(account_id = account_id)
            paginator = Paginator(ad_set_insights, int(limit))
            try:
                insights = paginator.page(int(page))
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                insights = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                insights = paginator.page(paginator.num_pages)

            serializer = AdSetInsightSerializer(insights, many=True)

            response_data['success'] = 'YES'
            response_data['total_count'] = len(ad_set_insights)
            response_data['data'] = serializer.data
        except Exception as e:
            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
