from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import render
from django.db.models import Count, Min, Sum, Avg
from rest_framework.views import APIView

from account_category.models import AccountCategory
from pixel_mapping.models import PixelMapping
from pixel_mapping_category.models import PixelMappingCategory
from fb_ad_account.models import FbAdAccount
from ad_set_insight.models import AdSetInsight
from ad_set_insight.serializers import AdSetInsightSerializer

from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.customconversion import CustomConversion
from utils.facebookapis.api_init import (api_init, api_init_by_system_user)
from utils.facebookapis.ad_account import ad_sets as ad_sets_api

import os
import json
import logging
import traceback
from datetime import datetime
from itertools import groupby
from operator import itemgetter
import itertools
import operator

logger = logging.getLogger(__name__)

class AdSetInsightByAccount(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            api_init_by_system_user()
            # TODO Session token

            ad_set_insights = None

            fb_account_id = request.query_params.get('account_id', '0')
            page = request.query_params.get('page', '1')
            start = request.query_params.get('start', '0')
            limit = request.query_params.get('limit', '25')

            # 13일 14일 포함 확인
            since = request.query_params.get('since', '2018-01-13')
            until = request.query_params.get('until', '2018-01-14')
            # since = '2017-12-14'
            # until = '2017-12-15'
            start = datetime.strptime(since, '%Y-%m-%d')
            end = datetime.strptime(until, '%Y-%m-%d')
            diff = end - start
            date_diff = diff.days + 1

            account = FbAdAccount.find_by_ad_account_id(FbAdAccount, 'act_'+fb_account_id)
            if fb_account_id == None or account == None:
                raise Exception("Not Existing FbAdAccount.")
            # 카테고리
            account_category = AccountCategory.objects.get(pk=account.account_category_id)
            account_category_name = account_category.category_label_kr
            # 픽셀매핑
            pixel_mapping_category_list = []
            pixel_mapping = PixelMapping.get_list_by_fb_ad_account_id(PixelMapping, account.id)
            for pm in pixel_mapping:
                pixel_dict = {}
                pixel_dict['fb_event'] = pm.facebook_pixel_event_name
                pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_id(PixelMappingCategory, pm.pixel_mapping_category_id)
                pixel_dict['name'] = pixel_mapping_category.category_label_kr
                pixel_dict['custom_event'] =pixel_mapping_category.category_label_en
                pixel_mapping_category_list.append(pixel_dict)

            print(pixel_mapping_category_list)

            # TODO 기간 나타내는 방법
            ad_set_insights = AdSetInsight.objects.filter(account_id=fb_account_id, date_stop__range=(since, until)
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

            # Custom Event CUSTOM SORT/SUM
            actions_insights = AdSetInsight.objects.filter(account_id=fb_account_id,date_stop__range=(since,until)).values('adset_id', 'date_stop', 'actions', 'video_10_sec_watched_actions', 'video_30_sec_watched_actions')
            actions_insights_list = []
            video_10_sec_insights_list = []
            video_30_sec_insights_list = []
            for action_insight in actions_insights:
                # action 전체
                report = {}
                report['adset_id'] = action_insight['adset_id']
                report['date_stop'] = action_insight['date_stop']
                if action_insight['actions'] != None:
                    actions = eval(action_insight['actions'])
                    report['actions'] = actions
                else:
                    report['actions'] = None

                # video_10_sec_view
                video_10sec_report = {}
                video_10sec_report['adset_id'] = action_insight['adset_id']
                video_10sec_report['date_stop'] = action_insight['date_stop']
                if action_insight['video_10_sec_watched_actions'] != None:
                    actions = eval(action_insight['video_10_sec_watched_actions'])
                    video_10sec_report['video_10_sec_watched_actions'] = actions
                else:
                    video_10sec_report['video_10_sec_watched_actions'] = None

                # video_30_sec_view
                video_30sec_report = {}
                video_30sec_report['adset_id'] = action_insight['adset_id']
                video_30sec_report['date_stop'] = action_insight['date_stop']
                if action_insight['video_30_sec_watched_actions'] != None:
                    actions = eval(action_insight['video_30_sec_watched_actions'])
                    video_30sec_report['video_30_sec_watched_actions'] = actions
                else:
                    video_30sec_report['video_30_sec_watched_actions'] = None

                actions_insights_list.append(report)
                video_10_sec_insights_list.append(video_10sec_report)
                video_30_sec_insights_list.append(video_30sec_report)

            actions_insights_list = sorted(actions_insights_list, key=itemgetter('adset_id'))
            video_10_sec_insights_list = sorted(video_10_sec_insights_list, key=itemgetter('adset_id'))
            video_30_sec_insights_list = sorted(video_30_sec_insights_list, key=itemgetter('adset_id'))

            report_dict = {}
            for key, value in itertools.groupby(actions_insights_list, key=itemgetter('adset_id')):
                result = []
                for i in value:
                    if i.get('actions') != None:
                        result += i.get('actions')
                    else:
                        result += ''
                    report_dict[key] = result

            # video_10sec
            report_dict_video_10_sec = {}
            for key, value in itertools.groupby(video_10_sec_insights_list, key=itemgetter('adset_id')):
                result = []
                for i in value:
                    if i.get('video_10_sec_watched_actions') != None:
                        result += i.get('video_10_sec_watched_actions')
                    else:
                        result += ''
                    report_dict_video_10_sec[key] = result

            # video_30sec
            report_dict_video_30_sec = {}
            for key, value in itertools.groupby(video_30_sec_insights_list, key=itemgetter('adset_id')):
                result = []
                for i in value:
                    if i.get('video_30_sec_watched_actions') != None:
                        result += i.get('video_30_sec_watched_actions')
                    else:
                        result += ''
                    report_dict_video_30_sec[key] = result

            # Django model aggregation values
            pixel_group = []
            target_insights = []
            for insight in ad_set_insights:
                result = {}
                # target report data
                adset_id = insight['adset_id']
                adset = ad_sets_api.get_ad_set(adset_id)
                adset_name = adset.get('name')
                campaign = adset.get('campaign')
                objective = campaign['objective']
                campaign_name = campaign['name']
                targeting = adset.get('targeting')

                interest_list = []
                if 'flexible_spec' in targeting:
                    flexible_spec = targeting.get('flexible_spec')
                    for fs in flexible_spec:
                        interests = fs['interests']
                        for interest in interests:
                            name = interest['name']
                            interest_list.append(name)
                else:
                    interests = []

                custom_audience_list = []
                if 'custom_audiences' in targeting:
                    custom_audiences = targeting.get('custom_audiences')
                    for ca in custom_audiences:
                        name = ca['name']
                        custom_audience_list.append(name)
                else:
                    custom_audience_list = []

                g = ''
                if 'genders' in targeting:
                    genders = targeting['genders']
                    gender = ''.join(str(g) for g in genders)
                    if gender == '1':
                        gender = 'male'
                    elif gender == '2':
                        gender = 'female'
                    elif gender == '0':
                        gender = 'all'
                    else:
                        gender = ''
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
                frequency = insight.get('frequency')
                inline_link_click_ctr = insight.get('inline_link_click_ctr')

                # result['targeting'] = targeting
                result['custom_audience'] = custom_audience_list
                result['account_category'] = account_category_name
                result['interest_num'] = len(interests)
                result['interest_list'] = interest_list
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
                result['cpc'] = round(cpc, 2)
                result['ctr'] = round(ctr, 2)
                result['cpp'] = round(cpp, 2)
                result['conversions'] = conversions
                result['frequency'] = round(frequency, 2)
                result['inline_link_click_ctr'] = round(inline_link_click_ctr, 2)
                result['pickdata_custom_pixel_event'] = []

                # Custom Event 계산 추가
                pixels = []
                # 모든 action event total -
                for key, items in report_dict.items():
                    if key == adset_id:
                        if items != None:
                            action_sort = sorted(items, key=itemgetter('action_type'))
                            for key, value in itertools.groupby(action_sort, key=itemgetter('action_type')):
                                if 'offsite_conversion.custom.' in key:
                                    pixel_id = key[26:]
                                    pixels.append(pixel_id)

                                v_list = []
                                for v in value:
                                    v = list(v.values())
                                    v.remove(key)
                                    v_list += v

                                v_list = list(map(int, v_list))
                                key = key + '_event'
                                result[key] = sum(v_list)

                # actions field로는 video_view total 만 가져올수있으므로 따로 다시 기간 adset_id별로 분류+합 해야한다.

                # 10_sec_video_view total
                for key, items in report_dict_video_10_sec.items():
                    if key == adset_id:
                        if items != None:
                            action_sort = sorted(items, key=itemgetter('action_type'))
                            for key, value in itertools.groupby(action_sort, key=itemgetter('action_type')):
                                v_list = []
                                for v in value:
                                    v = list(v.values())
                                    v.remove(key)
                                    v_list += v

                                v_list = list(map(int, v_list))
                                result['video_10_sec_watched_actions'] = sum(v_list)

                # 30_sec_video_view total
                for key, items in report_dict_video_30_sec.items():
                    if key == adset_id:
                        if items != None:
                            action_sort = sorted(items, key=itemgetter('action_type'))
                            for key, value in itertools.groupby(action_sort, key=itemgetter('action_type')):
                                v_list = []
                                for v in value:
                                    v = list(v.values())
                                    v.remove(key)
                                    v_list += v

                                v_list = list(map(int, v_list))
                                result['video_30_sec_watched_actions'] = sum(v_list)

                target_insights.append(result)

                pixel_group += pixels
            pixel_group = list(set(pixel_group))

            # pixel id, 이름 호출
            custom_pixel = []
            for pix in pixel_group:
                custom = CustomConversion(pix)
                result = custom.remote_read(fields=['id', 'name'])
                custom_pixel.append(result._json)

            # 기본 픽셀 이벤트 네이밍
            for data in target_insights:
                for key, items in data.items():
                    result = {}
                    if 'fb_pixel_complete_registration' in key:
                        result['name'] = 'CompleteRegistration'
                        result['value'] = items
                        data[key] = result
                    if 'fb_pixel_add_to_wishlist' in key:
                        result['name'] = 'AddToWishlist'
                        result['value'] = items
                        data[key] = result
                    if 'fb_pixel_add_to_cart' in key:
                        result['name'] = 'AddToCart'
                        result['value'] = items
                        data[key] = result
                    if 'fb_pixel_view_content' in key:
                        result['name'] = 'ViewContent'
                        result['value'] = items
                        data[key] = result
                    if 'fb_pixel_search' in key:
                        result['name'] = 'Search'
                        result['value'] = items
                        data[key] = result
                    if 'fb_pixel_initiate_checkout' in key:
                        result['name'] = 'InitiateCheckout'
                        result['value'] = items
                        data[key] = result
                    if 'fb_pixel_add_payment_info' in key:
                        result['name'] = 'AddPaymentInfo'
                        result['value'] = items
                        data[key] = result
                    if 'fb_pixel_purchase' in key:
                        result['name'] = 'Purchase'
                        result['value'] = items
                        data[key] = result
                    if 'fb_pixel_lead' in key:
                        result['name'] = 'Lead'
                        result['value'] = items
                        data[key] = result
                    if 'fb_pixel_custom' in key:
                        result['name'] = 'CustomBehavior'
                        result['value'] = items
                        data[key] = result

                    # Custom Event Name
                    for p in custom_pixel:
                        if p['id'] in key:
                            output = {}
                            output['value'] = items
                            output['name'] = p['name']
                            data[key] = output

            # Pixel Mapping (FB 이벤트명과 Pickdata CUSTOM EVENT 이름 매핑)
            for da in target_insights:
                result = []
                for key, items in da.items():
                    if '_event' in key:
                        if type(items) is dict:
                            # result = []
                            for pix in pixel_mapping_category_list:
                                if items['name'] == pix['fb_event']:
                                    # print(pix['fb_event'])
                                    custom = {}
                                    custom['custom_name'] = pix['name']
                                    custom['fb_event'] = items['name']
                                    custom['value'] = items['value']
                                    print(custom)
                                    result.append(custom)
                da['pickdata_custom_pixel_event'] = result

            response_data['success'] = 'YES'
            response_data['total_count'] = len(target_insights)
            response_data['data'] = target_insights
        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
