from django.http import HttpResponse
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.conf import settings
from django.shortcuts import render
from django.db.models import Count, Min, Sum, Avg
from rest_framework.views import APIView

from account_category.models import AccountCategory
from pixel_mapping.models import PixelMapping
from pixel_mapping_category.models import PixelMappingCategory
from fb_ad_account.models import FbAdAccount
from ad_set_insight.models import AdSetInsight
from ad_set.models import AdSet as AdSetModel
from ad_set_insight.serializers import AdSetInsightSerializer

from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.customconversion import CustomConversion
from utils.facebookapis.api_init import (api_init, api_init_by_system_user)
from utils.facebookapis.ad_account import ad_sets as ad_sets_api
from utils.common import download_helper
from utils.common.excel_report import ExcelReport
from utils.common.string_formatter import string_to_literal

import os
import json
import urllib.request
import requests
import logging
import traceback
from datetime import datetime
from itertools import groupby
from operator import itemgetter
import itertools
import operator
import xlwt

logger = logging.getLogger(__name__)

class AdSetInsightByAccount(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            api_init_by_system_user()
            # TODO Session token

            # ad_set_insights = None

            fb_account_id = request.query_params.get('account_id', '0')
            category_name = request.query_params.get('category_name', 'all')
            page = request.query_params.get('page', '1')
            start = request.query_params.get('start', '0')
            limit = request.query_params.get('limit', '25')

            since = request.query_params.get('since', '')
            until = request.query_params.get('until', '')
            # since = '2017-12-14'
            # until = '2017-12-15'
            start = datetime.strptime(since, '%Y-%m-%d')
            end = datetime.strptime(until, '%Y-%m-%d')
            diff = end - start
            date_diff = diff.days + 1

            if fb_account_id == '0':
                # 전체 광고 계정 인사이트
                if category_name == 'all':
                    accounts = FbAdAccount.objects.all()
                else:
                    account_category = AccountCategory.objects.filter(category_label_en=category_name)
                    for category in account_category:
                        category_id = category.id

                    accounts = FbAdAccount.objects.filter(account_category_id=category_id)

                target_insights = []
                pixel_mapping_category_list = []
                for account in accounts:
                    fb_account_id = account.ad_account_id
                    account_name = account.name
                    account_category = AccountCategory.objects.get(pk=account.account_category_id)
                    account_category_name = account_category.category_label_kr
                    account_category_name_en = account_category.category_label_en
                    # 픽셀매핑
                    pixel_mapping = PixelMapping.get_list_by_fb_ad_account_id(PixelMapping, account.id)
                    for pm in pixel_mapping:
                        pixel_dict = {}
                        pixel_dict['fb_event'] = pm.facebook_pixel_event_name
                        pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_id(PixelMappingCategory, pm.pixel_mapping_category_id)
                        pixel_dict['name'] = pixel_mapping_category.category_label_kr
                        pixel_dict['custom_event'] =pixel_mapping_category.category_label_en
                        pixel_mapping_category_list.append(pixel_dict)

                    target_insight = self.targetInsight(fb_account_id, since, until, date_diff, account_name, account_category_name)
                    target_insights += target_insight

                # Pixel Mapping (FB 이벤트명과 Pickdata DB 저장된 CUSTOM EVENT 이름 매핑)
                for da in target_insights:
                    result = []
                    spend = da.get('spend')
                    for key, items in da.items():
                        if '_event' in key:
                            if type(items) is dict:
                                for pix in pixel_mapping_category_list:
                                    if items['name'] == pix['fb_event']:
                                        custom = {}
                                        # custom_name => 정해진 pixel_mapping 이벤트의 이름
                                        custom['custom_name'] = pix['name']
                                        # fb_event => 실제 fb_event (유저가 매핑하는 대로 dynamic하게 바뀜)
                                        custom['value'] = items['value']
                                        logger.info(custom)
                                        result.append(custom)
                                        # 각 pixel_mapping 화면용
                                        if pix['name'] == '전환 완료':
                                            da['pickdata_custom_conv_total'] = items['value']
                                            da['pickdata_custom_conv_total_cost'] = round(items['value']/spend, 0)
                                        if pix['name'] == '전환 1단계':
                                            da['pickdata_custom_conv_first'] = items['value']
                                        if pix['name'] == '전환 2단계':
                                            da['pickdata_custom_conv_second'] = items['value']
                                        if pix['name'] == '전환 3단계':
                                            da['pickdata_custom_conv_third'] = items['value']
                                        if pix['name'] == '전환 4단계':
                                            da['pickdata_custom_conv_fourth'] = items['value']
                                        if pix['name'] == '전환 5단계':
                                            da['pickdata_custom_conv_fifth'] = items['value']
                                        if pix['name'] == '전환단계 URL':
                                            da['pickdata_custom_conv_url'] = items['value']
                                        if pix['name'] == '회원가입':
                                            da['pickdata_custom_conv_register'] = items['value']
                                        if pix['name'] == '장바구니':
                                            da['pickdata_custom_conv_cart'] = items['value']
                                        if pix['name'] == '구매':
                                            da['pickdata_custom_conv_purchase'] = items['value']
                                        if pix['name'] == 'UTM타겟':
                                            da['pickdata_custom_conv_utm'] = items['value']
                                        if pix['name'] == 'NEO타겟':
                                            da['pickdata_custom_conv_neo'] = items['value']
                                        if pix['name'] == '특정페이지 방문':
                                            da['pickdata_custom_conv_visit_page'] = items['value']
                                        if pix['name'] == '사이트 방문':
                                            da['pickdata_custom_conv_visit_site'] = items['value']

                    da['pickdata_custom_pixel_event'] = result

            else:
                # 광고계정 별 인사이트
                account = FbAdAccount.find_by_ad_account_id(FbAdAccount, 'act_'+fb_account_id)
                if fb_account_id == None or account == None:
                    raise Exception("Not Existing FbAdAccount.")
                account_name = account.name
                # 카테고리
                account_category = AccountCategory.objects.get(pk=account.account_category_id)
                account_category_name = account_category.category_label_kr
                account_category_name_en = account_category.category_label_en
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

                target_insights = self.targetInsight(fb_account_id, since, until, date_diff, account_name, account_category_name)

                # Pixel Mapping (FB 이벤트명과 Pickdata DB 저장된 CUSTOM EVENT 이름 매핑)
                for da in target_insights:
                    result = []
                    spend = da.get('spend')
                    for key, items in da.items():
                        if '_event' in key:
                            if type(items) is dict:
                                for pix in pixel_mapping_category_list:
                                    if items['name'] == pix['fb_event']:
                                        custom = {}
                                        # custom_name => 정해진 pixel_mapping 이벤트의 이름
                                        custom['custom_name'] = pix['name']
                                        # fb_event => 실제 fb_event (유저가 매핑하는 대로 dynamic하게 바뀜)
                                        custom['fb_event'] = items['name']
                                        custom['value'] = items['value']
                                        logger.info(custom)
                                        result.append(custom)

                                        # 각 pixel_mapping 화면용
                                        if pix['name'] == '전환 완료':
                                            da['pickdata_custom_conv_total'] = items['value']
                                            da['pickdata_custom_conv_total_cost'] = round(items['value']/spend, 0)
                                        if pix['name'] == '전환 1단계':
                                            da['pickdata_custom_conv_first'] = items['value']
                                        if pix['name'] == '전환 2단계':
                                            da['pickdata_custom_conv_second'] = items['value']
                                        if pix['name'] == '전환 3단계':
                                            da['pickdata_custom_conv_third'] = items['value']
                                        if pix['name'] == '전환 4단계':
                                            da['pickdata_custom_conv_fourth'] = items['value']
                                        if pix['name'] == '전환 5단계':
                                            da['pickdata_custom_conv_fifth'] = items['value']
                                        if pix['name'] == '전환단계 URL':
                                            da['pickdata_custom_conv_url'] = items['value']
                                        if pix['name'] == '회원가입':
                                            da['pickdata_custom_conv_register'] = items['value']
                                        if pix['name'] == '장바구니':
                                            da['pickdata_custom_conv_cart'] = items['value']
                                        if pix['name'] == '구매':
                                            da['pickdata_custom_conv_purchase'] = items['value']
                                        if pix['name'] == 'UTM타겟':
                                            da['pickdata_custom_conv_utm'] = items['value']
                                        if pix['name'] == 'NEO타겟':
                                            da['pickdata_custom_conv_neo'] = items['value']
                                        if pix['name'] == '특정페이지 방문':
                                            da['pickdata_custom_conv_visit_page'] = items['value']
                                        if pix['name'] == '사이트 방문':
                                            da['pickdata_custom_conv_visit_site'] = items['value']

                    da['pickdata_custom_pixel_event'] = result

            paginator = Paginator(target_insights, int(limit))
            try:
                contacts = paginator.page(int(page))
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                contacts = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                contacts = paginator.page(paginator.num_pages)

            response_data['success'] = 'YES'
            response_data['total_count'] = len(target_insights)
            response_data['data'] = list(contacts)
        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def targetInsight(self, fb_account_id, since, until, date_diff, account_name, account_category_name):

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
        actions_insights = AdSetInsight.objects.filter(account_id=fb_account_id,date_stop__range=(since,until)).values('adset_id', 'date_stop', 'actions', 'video_10_sec_watched_actions', 'video_30_sec_watched_actions', 'carousel_actions')
        actions_insights_list = []
        video_10_sec_insights_list = []
        video_30_sec_insights_list = []
        carousel_action_insights_list = []
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

            carousel_action_report = {}
            carousel_action_report['adset_id'] = action_insight['adset_id']
            carousel_action_report['date_stop'] = action_insight['date_stop']
            if action_insight['carousel_actions'] != None:
                actions = eval(action_insight['carousel_actions'])
                carousel_action_report['carousel_actions'] = actions
            else:
                carousel_action_report['carousel_actions'] = None

            carousel_action_insights_list.append(carousel_action_report)

        actions_insights_list = sorted(actions_insights_list, key=itemgetter('adset_id'))
        video_10_sec_insights_list = sorted(video_10_sec_insights_list, key=itemgetter('adset_id'))
        video_30_sec_insights_list = sorted(video_30_sec_insights_list, key=itemgetter('adset_id'))
        carousel_action_insights_list = sorted(carousel_action_insights_list, key=itemgetter('adset_id'))

        # actions 안에 있는 모든 event
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

        report_dict_carousel_actions = {}
        for key, value in itertools.groupby(carousel_action_insights_list, key=itemgetter('adset_id')):
            result = []
            for i in value:
                if i.get('carousel_actions') != None:
                    result += i.get('carousel_actions')
                else:
                    result += ''
                report_dict_carousel_actions[key] = result

        # Django model aggregation values
        pixel_group = []
        target_insights = []
        for insight in ad_set_insights:
            result = {}
            # target report data
            adset_id = insight['adset_id']
            try:
                adset = AdSetModel.objects.get(adset_id=adset_id)

                adset_name = adset.adset_name
                objective = adset.campaign_objective
                campaign_name = adset.campaign_name
                targeting = adset.targeting
                genders = adset.gender
                genders = string_to_literal(genders)
                g = ''
                gender = ''.join(str(g) for g in genders)
                if gender == '1':
                    gender = 'male'
                elif gender == '2':
                    gender = 'female'
                elif gender == '0':
                    gender = 'all'
                else:
                    gender = ''

                interests = adset.include_interests
                interests = string_to_literal(interests)
                custom_audiences = adset.custom_audiences
                custom_audiences = string_to_literal(custom_audiences)

                interest_list = []
                if interests != []:
                    for interest in interests:
                        item = interest['name']
                        interest_list.append(item)
                else:
                    pass

                custom_audience_list = []
                if custom_audiences != '[]':
                    for audience in custom_audiences:
                        item = audience['name']
                        custom_audience_list.append(item)
                else:
                    pass

                age_max = adset.age_max
                age_min = adset.age_min
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


                result['custom_audience'] = custom_audience_list
                result['account_name'] = account_name
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
                if inline_link_clicks != 0:
                    result['inline_link_click_cpc'] = round(spend/inline_link_clicks, 0)
                else:
                    result['inline_link_click_cpc'] = 0
                result['pickdata_custom_pixel_event'] = []
                # 픽셀 매핑 값 (화면용)
                result['pickdata_custom_conv_total'] = 0
                result['pickdata_custom_conv_total_cost'] = 0
                result['pickdata_custom_conv_first'] = 0
                result['pickdata_custom_conv_second'] = 0
                result['pickdata_custom_conv_third'] = 0
                result['pickdata_custom_conv_fourth'] = 0
                result['pickdata_custom_conv_fifth'] = 0
                result['pickdata_custom_conv_url'] = 0
                result['pickdata_custom_conv_register'] = 0
                result['pickdata_custom_conv_cart'] = 0
                result['pickdata_custom_conv_purchase'] = 0
                result['pickdata_custom_conv_utm'] = 0
                result['pickdata_custom_conv_neo'] = 0
                result['pickdata_custom_conv_visit_page'] = 0
                result['pickdata_custom_conv_visit_site'] = 0

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
                                if (impressions != 0):
                                    result['video_10_sec_watched_vtr'] = round(sum(v_list)/impressions*100, 2)
                                else:
                                    result['video_10_sec_watched_vtr'] = 0
                                if (spend != 0):
                                    result['video_10_sec_watched_cpv'] = round(sum(v_list)/spend, 2)
                                else:
                                    result['video_10_sec_watched_cpv'] = 0

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
                                # result['video_30_sec_watched_vtr'] = round(sum(v_list)/impressions*100, 2)
                                # result['video_30_sec_watched_cpv'] = round(sum(v_list)/spend, 2)
                                if (impressions != 0):
                                    result['video_30_sec_watched_vtr'] = round(sum(v_list)/impressions*100, 2)
                                else:
                                    result['video_30_sec_watched_vtr'] = 0
                                if (spend != 0):
                                    result['video_30_sec_watched_cpv'] = round(sum(v_list)/spend, 2)
                                else:
                                    result['video_30_sec_watched_cpv'] = 0

                # Carousel 소재 링크 클릭 값
                for key, items in report_dict_carousel_actions.items():
                    if key == adset_id:
                        if items != None:
                            grouper = itemgetter("action_carousel_card_id", "action_carousel_card_name")
                            r = []
                            for key, grp in groupby(sorted(items, key = grouper), grouper):
                                temp_dict = dict(zip(["action_carousel_card_id", "action_carousel_card_id"], key))
                                temp_dict["value"] = sum(int(item["value"]) for item in grp)
                                r.append(temp_dict)
                            result['carousel_actions'] = r
                            # TODO ID로 groupby를하고 id 랑  name이랑 매치. value 를 가져와서 id같은것들끼리 SUM?

                target_insights.append(result)

                pixel_group += pixels
            except ObjectDoesNotExist:
                pass
                # raise CommandError('does not exist')
        pixel_group = list(set(pixel_group))

        # pixel id, 이름 호출
        custom_pixel = []
        for pix in pixel_group:
            custom = CustomConversion(pix)
            result = custom.remote_read(fields=['id', 'name'])
            custom_pixel.append(result._json)

        # 기본 픽셀 이벤트 네이밍 (FB기준)
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
        # print(target_insights)

        return target_insights


class ReportExcelDownload(APIView):
    def get(self, request, format=None):
        response_data = {}
        file_path = ''
        file_name = ''
        try:
            insights = AdSetInsightByAccount()

            api_init_by_system_user()
            # TODO Session token

            fb_account_id = request.query_params.get('account_id', '0')
            category_name = request.query_params.get('category_name', 'all')
            since = request.query_params.get('since', '2018-01-01')
            until = request.query_params.get('until', '2018-01-29')
            start = datetime.strptime(since, '%Y-%m-%d')
            end = datetime.strptime(until, '%Y-%m-%d')
            diff = end - start
            date_diff = diff.days + 1

            if fb_account_id == '0':
                # 전체 광고 계정 인사이트
                if category_name == 'all':
                    accounts = FbAdAccount.objects.all()
                else:
                    account_category = AccountCategory.objects.filter(category_label_en=category_name)
                    for category in account_category:
                        category_id = category.id

                    accounts = FbAdAccount.objects.filter(account_category_id=category_id)

                target_insights = []
                for account in accounts:
                    fb_account_id = account.ad_account_id
                    account_name = account.name
                    account_category = AccountCategory.objects.get(pk=account.account_category_id)
                    account_category_name = account_category.category_label_kr
                    account_category_name_en = account_category.category_label_en
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

                    target_insight = insights.targetInsight(fb_account_id, since, until, date_diff, account_name, account_category_name)
                    # print(target_insight)
                    target_insights += target_insight

                # TODO 전체 데이터 모아서, 픽셀매핑 필요
                # Pixel Mapping (FB 이벤트명과 Pickdata DB 저장된 CUSTOM EVENT 이름 매핑)
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
                                        logger.info(custom)
                                        result.append(custom)
                    da['pickdata_custom_pixel_event'] = result

            else:
                # 광고계정 별 인사이트
                account = FbAdAccount.find_by_ad_account_id(FbAdAccount, 'act_'+fb_account_id)
                if fb_account_id == None or account == None:
                    raise Exception("Not Existing FbAdAccount.")
                account_name = account.name
                # 카테고리
                account_category = AccountCategory.objects.get(pk=account.account_category_id)
                account_category_name = account_category.category_label_kr
                account_category_name_en = account_category.category_label_en
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

                target_insights = insights.targetInsight(fb_account_id, since, until, date_diff, account_name, account_category_name)

                # Pixel Mapping (FB 이벤트명과 Pickdata DB 저장된 CUSTOM EVENT 이름 매핑)
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
                                        logger.info(custom)
                                        result.append(custom)
                    da['pickdata_custom_pixel_event'] = result

            # 인사이트 다운로드
            file_path = 'logs/'
            file_path = os.path.join(settings.PROJECT_DIR, file_path)
            # logger.info('file_path : %s' % (file_path))
            # file_path = '/Users/chloelim/Desktop/'
            file_name = "target_report.xls"

            excel_report = ExcelReport()
            excel_report = excel_report.write_workbook(file_path, file_name, target_insights)
            res = download_helper.respond_as_attachment(request, os.path.join(file_path, file_name), file_name)

            response_data['success'] = 'YES'
        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
        finally:
            if os.path.exists(os.path.join(file_path, file_name)):
                os.remove(os.path.join(file_path, file_name))
        return res
