from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import render
from django.db.models import Count, Min, Sum, Avg
from rest_framework.views import APIView

from ad_set_insight.models import AdSetInsight
from ad_set_insight.serializers import AdSetInsightSerializer

from facebookads.adobjects.adset import AdSet
from utils.facebookapis.api_init import (api_init, api_init_by_system_user)
from utils.facebookapis.ad_account import ad_sets as ad_sets_api

import os
import json
import logging
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)

class AdSetInsightByAccount(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            api_init_by_system_user()
            # TODO Session token

            ad_set_insights = None

            account_id = request.query_params.get('account_id', '0')
            page = request.query_params.get('page', '1')
            start = request.query_params.get('start', '0')
            limit = request.query_params.get('limit', '25')

            since = request.query_params.get('since', '2018-01-13')
            until = request.query_params.get('until', '2018-01-14')

            # since = '2018-01-13'
            # until = '2018-01-14'
            start = datetime.strptime(since, '%Y-%m-%d')
            end = datetime.strptime(until, '%Y-%m-%d')
            diff = end - start
            date_diff = diff.days + 1

            # TODO 기간 나타내는 방법
            ad_set_insights = AdSetInsight.objects.filter(account_id = account_id, date_stop__range=(since, until)
                                                            ).values('adset_id'
                                                            ).annotate(call_to_action_clicks=Sum('call_to_action_clicks'),
                                                            inline_link_clicks=Sum('inline_link_clicks'),
                                                            impressions=Sum('impressions'),
                                                            clicks=Sum('clicks'),
                                                            reach=Sum('reach'),
                                                            spend=Sum('spend'),
                                                            cpc=Sum('cpc')/int(date_diff),
                                                            cpm=Sum('cpm')/int(date_diff),
                                                            cpp=Sum('cpp')/int(date_diff),
                                                            ctr=Sum('ctr')/int(date_diff),
                                                            conversions=Sum('total_actions'),
                                                            frequency=Sum('frequency')/int(date_diff),
                                                            inline_link_click_ctr=Sum('inline_link_click_ctr')/int(date_diff)
                                                            ).order_by('adset_id')

            target_insights = []
            for insight in ad_set_insights:
                # logger.info(insight)
                result = {}
                # target report data
                adset_id = insight['adset_id']
                adset = ad_sets_api.get_ad_set(adset_id)
                adset_name = adset.get('name')
                campaign = adset.get('campaign')
                objective = campaign['objective']
                campaign_name = campaign['name']
                targeting = adset.get('targeting')

                if 'flexible_spec' in targeting:
                    flexible_spec = targeting.get('flexible_spec')
                    for fs in flexible_spec:
                        interests = fs['interests']
                else:
                    interests = []

                g = ''
                if 'genders' in targeting:
                    genders = targeting['genders']
                    gender = ''.join(str(g) for g in genders)
                    if gender == "1":
                        gender = 'male'
                    elif gender == "2":
                        gender = 'female'
                    elif gender == "0":
                        gender = 'all'
                    else:
                        gender = ''
                        logger.info(gender)
                else:
                    gender = 'all'

                age_max = targeting['age_max']
                age_min = targeting['age_min']
                age = str(age_min) + '-' + str(age_max)
                report_date = str(since) + ' ~ ' + str(until)
                impressions = insight.get('impressions')
                clicks = insight.get('clicks')
                reach = insight.get('reach')
                spend = insight.get('spend')
                inline_link_clicks = insight.get('inline_link_clicks')
                cpc = insight.get('cpc')
                cpm = insight.get('cpm')
                ctr = insight.get('ctr')
                cpp = insight.get('cpp')
                conversions = insight.get('conversions')

                # result['targeting'] = targeting
                result['interest_num'] = len(interests)
                result['age'] = age
                result['gender'] = gender
                result['adset_id'] = adset_id
                result['adset_name'] = adset_name
                result['campaign_name'] = campaign_name
                result['objective'] = objective
                result['report_date'] = report_date
                result['impressions'] = impressions
                result['reach'] = reach
                result['spend'] = spend
                result['clicks'] = clicks
                result['inline_link_clicks'] = inline_link_clicks
                result['cpc'] = cpc
                result['ctr'] = ctr
                result['cpp'] = cpp
                result['conversions'] = conversions

                target_insights.append(result)

            # TODO 인사이트 필요한 나머지 데이터 추가
            print(target_insights)

            response_data['success'] = 'YES'
            response_data['total_count'] = len(target_insights)
            response_data['data'] = target_insights
        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
