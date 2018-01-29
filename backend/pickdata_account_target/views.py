from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from fb_ad_account.models import FbAdAccount
from pixel_mapping_category.models import PixelMappingCategory
from pixel_mapping_category.serializers import PixelMappingCategorySerializer

from .models import PickdataAccountTarget
from .serializers import PickdataAccountTargetSerializer

from ad_set.models import AdSet

from utils.facebookapis.ad_set import insight as adset_insight
from utils.facebookapis.api_init import (api_init, api_init_by_system_user, api_init_session)
from utils.facebookapis.targeting import custom_audience
from utils.facebookapis.ad_account import custom_audiences as custom_audience_api
from utils.common.string_formatter import string_to_literal
from utils.common import convert_chart_data

from utils.facebookapis.targeting import targeting_visitor, targeting_specific_page_visitor, targeting_url, targeting_purchase, targeting_addtocart, targeting_registration

from django.conf import settings

facebook_app_id = settings.FACEBOOK_APP_ID

import json
import logging
import traceback

logger = logging.getLogger(__name__)


class PickdataAccountTargetViewSet(viewsets.ModelViewSet):
    queryset = PickdataAccountTarget.objects.all()
    serializer_class = PickdataAccountTargetSerializer

class TargetPick(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            if str(facebook_app_id) == "284297631740545":
                api_init_session(request)
            else:
                api_init_by_system_user()

            fb_ad_account_id = request.query_params.get('fb_ad_account_id', None)
            target_type = request.query_params.get('target_type', None)

            if target_type == None:
                target_type = "all"

            fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)
            if fb_ad_account_id == None or fb_ad_account == None:
                raise Exception("Not Existg FbAdAccount.")

            pickdata_targets = PickdataAccountTarget.get_list(PickdataAccountTarget, fb_ad_account_id)
            dic_audience_targets = custom_audience.get_dic_custom_audiences_by_ids([pickdata_target.target_audience_id for pickdata_target in pickdata_targets])

            pixel_mapping_categories = PixelMappingCategory.objects.all()

            group_target = {"total": []}
            group_category = {}

            for pixel_mapping_category in pixel_mapping_categories:
                label = pixel_mapping_category.category_label_en
                if label.find('conversion') > -1:
                    group_target['conversion'] = []
                    group_category[pixel_mapping_category.id] = 'conversion'
                else:
                    group_target[label] = []
                    group_category[pixel_mapping_category.id] = label

            for pickdata_target in pickdata_targets:
                gen_obj = {}
                pickdata_target_id = pickdata_target.id
                pixel_mapping_category = pickdata_target.pixel_mapping_category
                audience_id = pickdata_target.target_audience_id
                pixel_mapping_category_id = pickdata_target.pixel_mapping_category_id
                target_description = string_to_literal(pickdata_target.description)

                gen_obj['id'] = pickdata_target_id
                gen_obj['audience_id'] = audience_id
                gen_obj['description'] = target_description
                gen_obj['pixel_mapping_category_id'] = pixel_mapping_category_id
                gen_obj['pixel_mapping_category'] = PixelMappingCategorySerializer(pixel_mapping_category).data

                if str(audience_id) in dic_audience_targets:
                    audience_target = dic_audience_targets[str(audience_id)]

                    delivery_status = audience_target.get('delivery_status')
                    delivery_status_code = delivery_status.get('code')
                    operation_status = audience_target.get('operation_status')
                    operation_status_code = operation_status.get('code')

                    # code 200 정상 (숫자 노출)
                    # code 300 규모가 적음
                    # code 441

                    display_count = ''
                    targeting_complete = False
                    demographic_complete = False

                    if operation_status_code == 441:
                        display_count = "생성중"
                    elif delivery_status_code == 300:
                        display_count = "규모가 적음"
                        targeting_complete = True
                    elif delivery_status_code == 200:
                        display_count = audience_target.get('approximate_count')
                        targeting_complete = True

                    gen_obj['display_count'] = display_count
                    gen_obj['name'] = audience_target.get('name')
                    gen_obj['approximate_count'] = audience_target.get('approximate_count')
                    gen_obj['delivery_status'] = audience_target.get('delivery_status')
                    gen_obj['operation_status'] = audience_target.get('operation_status')
                    gen_obj['pixel_id'] = audience_target.get('pixel_id')
                    gen_obj['targeting_complete'] = targeting_complete
                    gen_obj['demographic_complete'] = demographic_complete

                    if target_type == "all":
                        group_target['total'].append(gen_obj)
                        group_target[group_category[pixel_mapping_category_id]].append(gen_obj)
                    elif target_type == "default":
                        if target_description.get('type') == 'default':
                            group_target['total'].append(gen_obj)
                            group_target[group_category[pixel_mapping_category_id]].append(gen_obj)
                    elif target_type == "created":
                        if target_description.get('type') != 'default':
                            group_target['total'].append(gen_obj)
                            group_target[group_category[pixel_mapping_category_id]].append(gen_obj)
                    elif target_type == "targeting_completed":
                        if targeting_complete == True:
                            group_target['total'].append(gen_obj)
                            group_target[group_category[pixel_mapping_category_id]].append(gen_obj)
                    elif target_type == "targeting_progress":
                        if targeting_complete == False:
                            group_target['total'].append(gen_obj)
                            group_target[group_category[pixel_mapping_category_id]].append(gen_obj)
                    elif target_type == "demographic":
                        if demographic_complete == True:
                            group_target['total'].append(gen_obj)
                            group_target[group_category[pixel_mapping_category_id]].append(gen_obj)
                    else:
                        pass

            group_target_and_cnt = {}
            for key in group_target:
                group_target_and_cnt[key.strip()] = {
                    "count": len(group_target[key]),
                    'data': group_target[key]
                }

            response_data['success'] = 'YES'
            response_data['data'] = group_target_and_cnt

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")

class TargetChart(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            pickdata_target_id = request.query_params.get('pickdata_target_id', 0)
            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('start_date', None)


            if pickdata_target_id == 0:
                raise Exception('Not Exist Pickdata Target.')

            pickdata_target = PickdataAccountTarget.get_by_id(PickdataAccountTarget, pickdata_target_id)
            if pickdata_target == None:
                raise Exception('Not Exist Pickdata Target.')

            if str(facebook_app_id) == "284297631740545":
                api_init_session(request)
            else:
                api_init_by_system_user()

            fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, pickdata_target.fb_ad_account_id)
            act_account_id = fb_ad_account.act_account_id

            target_audience_id = pickdata_target.target_audience_id
            print(target_audience_id)
            # TODO DELETE!!!
            from random import randint

            random_i = randint(0,2)
            print(random_i)
            target_audience_id = [6081089433857, 6081089396457, 6090733823497][random_i]
            act_account_id = ['act_894360037304328', 'act_894360037304328', 'act_107850179321216'][random_i]

            adsets = AdSet.get_adsets_by_target_id(AdSet, target_audience_id)
            # for adset in adsets:
            #     print(adset.id)
            #     print(adset.adset_id)
            # print(len(adsets))
            # print([adset.adset_id for adset in adsets])
            approximate_count = custom_audience.get_custom_audience(target_audience_id).get('approximate_count')

            # print("placement insight start")
            placement_insights = adset_insight.get_adset_ids_placement_insights(act_account_id, [adset.adset_id for adset in adsets], start_date=start_date, end_date=end_date)
            # print(placement_insights)
            placement_data = convert_chart_data.convert_placement_chart_data(placement_insights)
            # print("placement insight end")

            # print("age gender insight start")
            age_gender_insights = adset_insight.get_adset_ids_agegender_insights(act_account_id, [adset.adset_id for adset in adsets], start_date=start_date, end_date=end_date)
            # print(age_gender_insights)
            age_gender_data, total_spend, total_conversion, cta = convert_chart_data.convert_agegender_chart_data(age_gender_insights)
            # print("age gender insight end")

            response_data['success'] = 'YES'
            response_data['age_gender_data'] = age_gender_data
            response_data['placement_data'] = placement_data
            response_data['audience_count'] = approximate_count
            response_data['total_spend'] = total_spend
            response_data['total_conversion'] = total_conversion
            response_data['cta'] = cta

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            logger.error(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")


class CustomTarget(APIView):
    def make_description(self, pixel_mapping_category, retention_days, description, option, type_name, params, custom_data=None):
        description = {
            "pixel_mapping_category": pixel_mapping_category,
            "retention_days": retention_days,
            "description": description,
            "option": option,
            "type": type_name,
            "params": params
        }
        if custom_data != None:
            description["custom_data"] = custom_data
        return description

    def delete(self, request, format=None):
        response_data = {}
        try:
            if str(facebook_app_id) == "284297631740545":
                api_init_session(request)
            else:
                api_init_by_system_user()

            pickdata_account_target_id = request.data.get('pickdata_account_target_id', 0)
            pickdata_account_target = PickdataAccountTarget.objects.get(id=pickdata_account_target_id)
            if pickdata_account_target == None:
                raise Exception('Not Exist pickdata_account_target')
            custom_audience_id = pickdata_account_target.target_audience_id

            try:
                pickdata_account_target.delete()
            except Exception as delete_e:
                msg = {}
                msg['request_context'] = delete_e._request_context
                msg['error'] = delete_e._error
                raise Exception(msg)
            custom_audience_api.delete_custom_audience(custom_audience_id)

            response_data['success'] = 'YES'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    def put(self, request, format=None):
        response_data = {}
        try:
            fb_ad_account_id = request.data.get('fb_ad_account_id', 0)
            fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)

            if fb_ad_account == None:
                raise Exception('Not Exist fb_ad_account.')

            # visit_site, visit_specific_pages, neo_target, utm_target, purchase, add_to_cart, registration,
            target_type = request.data.get('target_type', None)
            pixel_id = request.data.get('pixel_id', 0)
            name = request.data.get('name', None)
            retention_days = request.data.get('retention_days', 30)
            retention_days = int(retention_days)

            # Update PickdataAccountTarget
            pickdata_account_target_id = request.data.get('pickdata_account_target_id', 0)
            pickdata_account_target = PickdataAccountTarget.objects.get(id=pickdata_account_target_id)
            if pickdata_account_target == None:
                raise Exception('Not Exist pickdata_account_target')
            custom_audience_id = pickdata_account_target.target_audience_id

            # 사이트 방문
            if target_type == "visit_site":
                detail = request.data.get('detail', '')
                pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory,
                                                                                                  'visit pages')

                description = {}
                # 전체고객
                if detail == "total":
                    print('abc')
                    created_target = targeting_visitor.update_total_customers(custom_audience_id, name,
                                                                              pixel_id, retention_days=retention_days)
                    description = self.make_description("사이트방문", retention_days, "전체", "", "custom", request.data)
                # 이용 시간 상위 고객
                elif detail == "usage_time_top":
                    input_percent = request.data.get('input_percent', 25)
                    created_target = targeting_visitor.update_usage_time_top_customers(custom_audience_id,
                                                                                       name, pixel_id,
                                                                                       retention_days=retention_days,
                                                                                       input_percent=input_percent)
                    description = self.make_description("사이트방문", retention_days, "이용시간상위" + str(input_percent) + "%", "", "custom", request.data)
                # 특정일 동안 미방문 고객
                elif detail == "non_visit":
                    exclusion_retention_days = request.data.get('exclusion_retention_days', 1)
                    exclusion_retention_days = int(exclusion_retention_days)
                    created_target = targeting_visitor.update_non_visition_customers(custom_audience_id, name,
                                                                                     pixel_id,
                                                                                     retention_days=retention_days,
                                                                                     exclusion_retention_days=exclusion_retention_days)
                    description = self.make_description("사이트방문", retention_days, "미방문고객", "", "custom", request.data)
                # 구매고객
                elif detail == "purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_visitor.update_visitor_and_purchase_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        purchase_event_name="Purchase")
                    description = self.make_description("사이트방문", retention_days, "구매고객", "", "custom", request.data)
                # 미 구매고객
                elif detail == "non_purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_visitor.update_visitor_and_non_purchase_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        purchase_event_name="Purchase")
                    description = self.make_description("사이트방문", retention_days, "미구매고객", "", "custom", request.data)
                # 장바구니 이용 고객
                elif detail == "add_to_cart":
                    # TODO 장바구니 이벤트 확인
                    created_target = targeting_visitor.update_visitor_and_addtocart_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        addtocart_evnet_name="AddToCart")
                    description = self.make_description("사이트방문", retention_days, "장바구니이용고객", "", "custom", request.data)
                # 전환완료 고객
                elif detail == "conversion":
                    # TODO 전환완료 이벤트 확인
                    created_target = targeting_visitor.update_visitor_and_coversion_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent")
                    description = self.make_description("사이트방문", retention_days, "전환완료고객", "", "custom", request.data)
                # 미 전환 고객
                elif detail == "non_conversion":
                    # TODO 전환완료 이벤트 확인
                    create_target = targeting_visitor.update_visitor_and_non_coversion_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent")
                    description = self.make_description("사이트방문", retention_days, "미전환고객", "", "custom", request.data)
                # 회원가입 고객
                elif detail == "registration":
                    # TODO 회원가입 이벤트 확인
                    created_target = targeting_visitor.update_visitor_and_registration_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        registration_event_name="CompleteRegistration")
                    description = self.make_description("사이트방문", retention_days, "회원가입고객", "", "custom", request.data)
                else:
                    raise Exception("No valid detail parameter")

            # 특정페이지 방문
            elif target_type == "visit_specific_pages":
                contain_list = request.data.get('contain_list', [])
                eq_list = request.data.get('eq_list', [])
                detail = request.data.get('detail', '')
                custom_data = {
                    "contain_list": contain_list,
                    "eq_list": eq_list,
                }
                pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory,
                                                                                                  'visit specific pages')

                description = {}

                # 전체고객
                if detail == "total":
                    created_target = targeting_specific_page_visitor.update_specific_page_total_visitor_customers(
                        custom_audience_id, name,
                        pixel_id, retention_days=retention_days, contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "전체", "", "custom", request.data, custom_data)
                # 이용 시간 상위 고객
                elif detail == "usage_time_top":
                    input_percent = request.data.get('input_percent', 25)
                    created_target = targeting_specific_page_visitor.update_usage_time_top_customers(
                        custom_audience_id,
                        name, pixel_id,
                        retention_days=retention_days,
                        input_percent=input_percent, contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "이용시간상위" + str(input_percent) + "%", "", "custom", request.data, custom_data)
                # 특정일 동안 미방문 고객
                elif detail == "non_visit":
                    exclusion_retention_days = request.data.get('exclusion_retention_days', 1)
                    exclusion_retention_days = int(exclusion_retention_days)
                    created_target = targeting_specific_page_visitor.update_non_visition_customers(
                        custom_audience_id, name,
                        pixel_id,
                        retention_days=retention_days, exclusion_retention_days=exclusion_retention_days, contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "미방문고객", "", "custom", request.data, custom_data)
                # 구매고객
                elif detail == "purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_specific_page_visitor.update_specific_page_and_purchase_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        purchase_event_name="Purchase", contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "구매고객", "", "custom", request.data, custom_data)
                # 미 구매고객
                elif detail == "non_purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_specific_page_visitor.update_specific_page_and_non_purchase_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        purchase_event_name="Purchase", contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "미구매고객", "", "custom", request.data, custom_data)
                # 장바구니 이용 고객
                elif detail == "add_to_cart":
                    # TODO 장바구니 이벤트 확인
                    created_target = targeting_specific_page_visitor.update_specific_page_and_addtocart_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        addtocart_evnet_name="AddToCart", contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "장바구니이용고객", "", "custom", request.data, custom_data)
                # 전환완료 고객
                elif detail == "conversion":
                    # TODO 전환완료 이벤트 확인
                    created_target = targeting_specific_page_visitor.update_specific_page_and_coversion_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent", contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "전환완료고객", "", "custom", request.data, custom_data)
                # 미 전환 고객
                elif detail == "non_conversion":
                    # TODO 전환완료 이벤트 확인
                    create_target = targeting_specific_page_visitor.update_specific_page_and_non_coversion_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent", contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "미전환고객", "", "custom", request.data, custom_data)
                # 회원가입 고객
                elif detail == "registration":
                    # TODO 회원가입 이벤트 확인
                    created_target = targeting_specific_page_visitor.update_specific_page_and_registration_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        registration_event_name="CompleteRegistration", contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "회원가입고객", "", "custom", request.data, custom_data)
                else:
                    raise Exception("No valid detail parameter")

            elif target_type == "neo_target":
                neo_type = request.data.get('neo_type')
                keywords = request.data.get('keywords')
                neo_ids = request.data.get('neo_ids')
                detail = request.data.get('detail', '')
                custom_data = {
                    "neo_type": neo_type,
                    "keywords": keywords,
                    "neo_ids": neo_ids
                }
                pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory,
                                                                                                  'neo target')
                description = {}
                # 전체고객
                if detail == "total":
                    created_target = targeting_url.update_url_total_visitor_customers(custom_audience_id,
                                                                                      name, pixel_id,
                                                                                      retention_days=retention_days,
                                                                                      contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "전체", "", "custom", request.data, custom_data)
                # 이용 시간 상위 고객
                elif detail == "usage_time_top":
                    input_percent = request.data.get('input_percent', 25)
                    created_target = targeting_url.update_usage_time_top_customers(custom_audience_id, name,
                                                                                   pixel_id,
                                                                                   retention_days=retention_days,
                                                                                   input_percent=input_percent,
                                                                                   contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "이용시간상위" + str(input_percent) + "%", "", "custom", request.data, custom_data)
                # 특정일 동안 미방문 고객
                elif detail == "non_visit":
                    exclusion_retention_days = request.data.get('exclusion_retention_days', 1)
                    exclusion_retention_days = int(exclusion_retention_days)
                    created_target = targeting_url.update_non_visition_customers(custom_audience_id, name,
                                                                                 pixel_id,
                                                                                 retention_days=retention_days,
                                                                                 contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "미방문고객", "", "custom", request.data, custom_data)
                # 구매고객
                elif detail == "purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_url.update_url_and_purchase_customers(custom_audience_id, name,
                                                                                     pixel_id,
                                                                                     retention_days=retention_days,
                                                                                     purchase_event_name="Purchase",
                                                                                     contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "구매고객", "", "custom", request.data, custom_data)
                # 미 구매고객
                elif detail == "non_purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_url.update_url_and_non_purchase_customers(custom_audience_id,
                                                                                         name, pixel_id,
                                                                                         retention_days=retention_days,
                                                                                         purchase_event_name="Purchase",
                                                                                         contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "미구매고객", "", "custom", request.data, custom_data)
                # 장바구니 이용 고객
                elif detail == "add_to_cart":
                    # TODO 장바구니 이벤트 확인
                    created_target = targeting_url.update_url_and_addtocart_customers(custom_audience_id,
                                                                                      name, pixel_id,
                                                                                      retention_days=retention_days,
                                                                                      addtocart_evnet_name="AddToCart",
                                                                                      contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "장바구니이용고객", "", "custom", request.data, custom_data)
                # 전환완료 고객
                elif detail == "conversion":
                    # TODO 전환완료 이벤트 확인
                    created_target = targeting_url.update_specific_page_and_coversion_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent", contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "전환완료고객", "", "custom", request.data, custom_data)
                # 미 전환 고객
                elif detail == "non_conversion":
                    # TODO 전환완료 이벤트 확인
                    created_target = targeting_url.update_url_and_non_coversion_customers(custom_audience_id,
                                                                                          name, pixel_id,
                                                                                          retention_days=retention_days,
                                                                                          conversion_event_name="ViewContent",
                                                                                          contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "미전환고객", "", "custom", request.data, custom_data)
                # 회원가입 고객
                elif detail == "registration":
                    # TODO 회원가입 이벤트 확인
                    created_target = targeting_url.update_specific_page_and_registration_customers(
                        custom_audience_id, name, pixel_id, retention_days=retention_days,
                        registration_event_name="CompleteRegistration", contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "회원가입고객", "", "custom", request.data, custom_data)
                else:
                    raise Exception("No valid detail parameter")

            # pickdata Database Update Call
            target = PickdataAccountTarget.update(PickdataAccountTarget, pickdata_account_target, fb_ad_account, created_target.get('id'),
                                                  pixel_mapping_category, json.dumps(description), username='test')
            serializer = PickdataAccountTargetSerializer(target)

            response_data['success'] = 'YES'
            response_data['data'] = serializer.data

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    def post(self, request, format=None):
        response_data = {}
        try:
            print(request.data)
            fb_ad_account_id = request.data.get('fb_ad_account_id', 0)
            fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)

            if fb_ad_account == None:
                raise Exception('Not Exist fb_ad_account.')

            # visit_site, visit_specific_pages, neo_target, utm_target, purchase, add_to_cart, registration,
            target_type = request.data.get('target_type', None)
            pixel_id = request.data.get('pixel_id', 0)
            name = request.data.get('name', None)
            retention_days = request.data.get('retention_days', 30)
            retention_days = int(retention_days)

            # 사이트 방문
            if target_type == "visit_site":
                detail = request.data.get('detail', '')
                pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory,
                                                                                                  'visit pages')

                description = {}
                # 전체고객
                if detail == "total":
                    created_target = targeting_visitor.create_total_customers(fb_ad_account.act_account_id, name,
                                                                              pixel_id, retention_days=retention_days)
                    description = self.make_description("사이트방문", retention_days, "전체", "", "custom", request.data)

                # 이용 시간 상위 고객
                elif detail == "usage_time_top":
                    input_percent = request.data.get('input_percent', 25)
                    created_target = targeting_visitor.create_usage_time_top_customers(fb_ad_account.act_account_id,
                                                                                       name, pixel_id,
                                                                                       retention_days=retention_days,
                                                                                       input_percent=input_percent)
                    description = self.make_description("사이트방문", retention_days, "이용시간상위" + str(input_percent) + "%", "", "custom", request.data)

                # 특정일 동안 미방문 고객
                elif detail == "non_visit":
                    exclusion_retention_days = request.data.get('exclusion_retention_days', 1)
                    exclusion_retention_days = int(exclusion_retention_days)
                    created_target = targeting_visitor.create_non_visition_customers(fb_ad_account.act_account_id, name,
                                                                                     pixel_id,
                                                                                     retention_days=retention_days,
                                                                                     exclusion_retention_days=exclusion_retention_days)
                    description = self.make_description("사이트방문", retention_days, "미방문고객", "", "custom", request.data)

                # 구매고객
                elif detail == "purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_visitor.create_visitor_and_purchase_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        purchase_event_name="Purchase")
                    description = self.make_description("사이트방문", retention_days, "구매고객", "", "custom", request.data)

                # 미 구매고객
                elif detail == "non_purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_visitor.create_visitor_and_non_purchase_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        purchase_event_name="Purchase")
                    description = self.make_description("사이트방문", retention_days, "미구매고객", "", "custom", request.data)

                # 장바구니 이용 고객
                elif detail == "add_to_cart":
                    # TODO 장바구니 이벤트 확인
                    created_target = targeting_visitor.create_visitor_and_addtocart_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        addtocart_evnet_name="AddToCart")
                    description = self.make_description("장바구니이용고객", retention_days, "미구매고객", "", "custom", request.data)

                # 전환완료 고객
                elif detail == "conversion":
                    # TODO 전환완료 이벤트 확인
                    created_target = targeting_visitor.create_visitor_and_coversion_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent")
                    description = self.make_description("장바구니이용고객", retention_days, "전환완료고객", "", "custom", request.data)

                # 미 전환 고객
                elif detail == "non_conversion":
                    # TODO 전환완료 이벤트 확인
                    create_target = targeting_visitor.create_visitor_and_non_coversion_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent")
                    description = self.make_description("장바구니이용고객", retention_days, "미전환고객", "", "custom", request.data)
                # 회원가입 고객
                elif detail == "registration":
                    # TODO 회원가입 이벤트 확인
                    created_target = targeting_visitor.create_visitor_and_registration_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        registration_event_name="CompleteRegistration")
                    description = self.make_description("장바구니이용고객", retention_days, "회원가입고객", "", "custom", request.data)
                else:
                    raise Exception("No valid detail parameter")

            # 특정페이지 방문
            elif target_type == "visit_specific_pages":

                contain_list = request.data.get('contain_list', [])
                eq_list = request.data.get('eq_list', [])
                detail = request.data.get('detail', '')
                custom_data = {
                    "contain_list": contain_list,
                    "eq_list": eq_list,
                }
                pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory,
                                                                                                  'visit specific pages')

                description = {}

                # 전체고객
                if detail == "total":
                    created_target = targeting_specific_page_visitor.create_specific_page_total_visitor_customers(
                        fb_ad_account.act_account_id, name,
                        pixel_id, retention_days=retention_days, contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "전체", "", "custom", request.data, custom_data)

                # 이용 시간 상위 고객
                elif detail == "usage_time_top":
                    input_percent = request.data.get('input_percent', 25)
                    created_target = targeting_specific_page_visitor.create_usage_time_top_customers(
                        fb_ad_account.act_account_id,
                        name, pixel_id,
                        retention_days=retention_days,
                        input_percent=input_percent, contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "이용시간상위" + str(input_percent) + "%", "", "custom", request.data, custom_data)

                # 특정일 동안 미방문 고객
                elif detail == "non_visit":
                    exclusion_retention_days = request.data.get('exclusion_retention_days', 1)
                    exclusion_retention_days = int(exclusion_retention_days)
                    created_target = targeting_specific_page_visitor.create_non_visition_customers(
                        fb_ad_account.act_account_id, name,
                        pixel_id,
                        retention_days=retention_days, exclusion_retention_days=exclusion_retention_days, contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "미방문고객", "", "custom", request.data, custom_data)

                # 구매고객
                elif detail == "purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_specific_page_visitor.create_specific_page_and_purchase_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        purchase_event_name="Purchase", contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "구매고객", "", "custom", request.data, custom_data)

                # 미 구매고객
                elif detail == "non_purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_specific_page_visitor.create_specific_page_and_non_purchase_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        purchase_event_name="Purchase", contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "미구매고객", "", "custom", request.data, custom_data)

                # 장바구니 이용 고객
                elif detail == "add_to_cart":
                    # TODO 장바구니 이벤트 확인
                    created_target = targeting_specific_page_visitor.create_specific_page_and_addtocart_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        addtocart_evnet_name="AddToCart", contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "장바구니이용고객", "", "custom", request.data, custom_data)

                # 전환완료 고객
                elif detail == "conversion":
                    # TODO 전환완료 이벤트 확인
                    created_target = targeting_specific_page_visitor.create_specific_page_and_coversion_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent", contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "전환완료고객", "", "custom", request.data, custom_data)

                # 미 전환 고객
                elif detail == "non_conversion":
                    # TODO 전환완료 이벤트 확인
                    create_target = targeting_specific_page_visitor.create_specific_page_and_non_coversion_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent", contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "미전환고객", "", "custom", request.data, custom_data)
                # 회원가입 고객
                elif detail == "registration":
                    # TODO 회원가입 이벤트 확인
                    created_target = targeting_specific_page_visitor.create_specific_page_and_registration_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        registration_event_name="CompleteRegistration", contain_list=contain_list, eq_list=eq_list)
                    description = self.make_description("특정페이지방문", retention_days, "회원가입고객", "", "custom", request.data, custom_data)
                else:
                    raise Exception("No valid detail parameter")

            elif target_type == "neo_target":
                neo_type = request.data.get('neo_type')
                keywords = request.data.get('keywords')
                neo_ids = request.data.get('neo_ids')
                detail = request.data.get('detail', '')

                custom_data = {
                    "neo_type": neo_type,
                    "keywords": keywords,
                    "neo_ids": neo_ids
                }

                pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory,
                                                                                                  'neo target')

                description = {}

                # 전체고객
                if detail == "total":
                    created_target = targeting_url.create_url_total_visitor_customers(fb_ad_account.act_account_id,
                                                                                      name, pixel_id,
                                                                                      retention_days=retention_days,
                                                                                      contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "전체", "", "custom", request.data, custom_data)

                # 이용 시간 상위 고객
                elif detail == "usage_time_top":
                    input_percent = request.data.get('input_percent', 25)
                    created_target = targeting_url.create_usage_time_top_customers(fb_ad_account.act_account_id, name,
                                                                                   pixel_id,
                                                                                   retention_days=retention_days,
                                                                                   input_percent=input_percent,
                                                                                   contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "이용시간상위" + str(input_percent) + "%", "", "custom", request.data, custom_data)

                # 특정일 동안 미방문 고객
                elif detail == "non_visit":
                    exclusion_retention_days = request.data.get('exclusion_retention_days', 1)
                    exclusion_retention_days = int(exclusion_retention_days)
                    created_target = targeting_url.create_non_visition_customers(fb_ad_account.act_account_id, name,
                                                                                 pixel_id,
                                                                                 retention_days=retention_days,
                                                                                 contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "미방문고객", "", "custom", request.data, custom_data)

                # 구매고객
                elif detail == "purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_url.create_url_and_purchase_customers(fb_ad_account.act_account_id, name,
                                                                                     pixel_id,
                                                                                     retention_days=retention_days,
                                                                                     purchase_event_name="Purchase",
                                                                                     contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "구매고객", "", "custom", request.data, custom_data)

                # 미 구매고객
                elif detail == "non_purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_url.create_url_and_non_purchase_customers(fb_ad_account.act_account_id,
                                                                                         name, pixel_id,
                                                                                         retention_days=retention_days,
                                                                                         purchase_event_name="Purchase",
                                                                                         contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "미구매고객", "", "custom", request.data, custom_data)

                # 장바구니 이용 고객
                elif detail == "add_to_cart":
                    # TODO 장바구니 이벤트 확인
                    created_target = targeting_url.create_url_and_addtocart_customers(fb_ad_account.act_account_id,
                                                                                      name, pixel_id,
                                                                                      retention_days=retention_days,
                                                                                      addtocart_evnet_name="AddToCart",
                                                                                      contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "장바구니이용고객", "", "custom", request.data, custom_data)

                # 전환완료 고객
                elif detail == "conversion":
                    # TODO 전환완료 이벤트 확인
                    created_target = targeting_url.create_specific_page_and_coversion_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent", contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "전환완료고객", "", "custom", request.data, custom_data)

                # 미 전환 고객
                elif detail == "non_conversion":
                    # TODO 전환완료 이벤트 확인
                    created_target = targeting_url.create_url_and_non_coversion_customers(fb_ad_account.act_account_id,
                                                                                          name, pixel_id,
                                                                                          retention_days=retention_days,
                                                                                          conversion_event_name="ViewContent",
                                                                                          contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "미전환고객", "", "custom", request.data, custom_data)
                # 회원가입 고객
                elif detail == "registration":
                    # TODO 회원가입 이벤트 확인
                    created_target = targeting_url.create_specific_page_and_registration_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        registration_event_name="CompleteRegistration", contain_list=neo_ids)
                    description = self.make_description("네오타겟", retention_days, "회원가입고객", "", "custom", request.data, custom_data)
                else:
                    raise Exception("No valid detail parameter")

            # 구글애널리틱스
            elif target_type == "utm_target":
                sources = request.data.get('sources')
                mediums = request.data.get('mediums')
                campaigns = request.data.get('campaigns')
                terms = request.data.get('terms')
                contents = request.data.get('contents')
                customs = request.data.get('customs')

                convert_sources = []
                convert_mediums = []
                convert_campaigns = []
                convert_terms = []
                convert_contents = []

                for source in sources:
                    convert_sources.append("utm_source="+source)

                for medium in mediums:
                    convert_mediums.append("utm_medium=" + medium)

                for campaign in campaigns:
                    convert_campaigns.append("utm_campaign=" + campaign)

                for term in terms:
                    convert_terms.append("utm_term="+term)

                for content in contents:
                    convert_contents.append("utm_content="+content)

                utm_ids = convert_sources + convert_mediums + convert_campaigns + convert_terms + convert_contents + customs


                detail = request.data.get('detail', '')

                custom_data = {
                    "sources": sources,
                    "mediums": mediums,
                    "campaigns": campaigns,
                    "terms": terms,
                    "contents": contents,
                    "customs": customs
                }

                pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory,
                                                                                                  'utm target')

                description = {}

                # 전체고객
                if detail == "total":
                    created_target = targeting_url.create_url_total_visitor_customers(fb_ad_account.act_account_id,
                                                                                      name, pixel_id,
                                                                                      retention_days=retention_days,
                                                                                      contain_list=utm_ids)
                    description = self.make_description("UTM타겟", retention_days, "전체", "", "custom", request.data, custom_data)
                # 이용 시간 상위 고객
                elif detail == "usage_time_top":
                    input_percent = request.data.get('input_percent', 25)
                    created_target = targeting_url.create_usage_time_top_customers(fb_ad_account.act_account_id, name,
                                                                                   pixel_id,
                                                                                   retention_days=retention_days,
                                                                                   input_percent=input_percent,
                                                                                   contain_list=utm_ids)
                    description = self.make_description("UTM타겟", retention_days, "이용시간상위" + str(input_percent) + "%", "", "custom", request.data, custom_data)
                # 특정일 동안 미방문 고객
                elif detail == "non_visit":
                    exclusion_retention_days = request.data.get('exclusion_retention_days', 1)
                    exclusion_retention_days = int(exclusion_retention_days)
                    created_target = targeting_url.create_non_visition_customers(fb_ad_account.act_account_id, name,
                                                                                 pixel_id,
                                                                                 retention_days=retention_days,
                                                                                 contain_list=utm_ids)
                    description = self.make_description("UTM타겟", retention_days, "미방문고객", "", "custom", request.data, custom_data)
                # 구매고객
                elif detail == "purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_url.create_url_and_purchase_customers(fb_ad_account.act_account_id, name,
                                                                                     pixel_id,
                                                                                     retention_days=retention_days,
                                                                                     purchase_event_name="Purchase",
                                                                                     contain_list=utm_ids)
                    description = self.make_description("UTM타겟", retention_days, "구매고객", "", "custom", request.data, custom_data)
                # 미 구매고객
                elif detail == "non_purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_url.create_url_and_non_purchase_customers(fb_ad_account.act_account_id,
                                                                                         name, pixel_id,
                                                                                         retention_days=retention_days,
                                                                                         purchase_event_name="Purchase",
                                                                                         contain_list=utm_ids)
                    description = self.make_description("UTM타겟", retention_days, "미구매고객", "", "custom", request.data, custom_data)
                # 장바구니 이용 고객
                elif detail == "add_to_cart":
                    # TODO 장바구니 이벤트 확인
                    created_target = targeting_url.create_url_and_addtocart_customers(fb_ad_account.act_account_id,
                                                                                      name, pixel_id,
                                                                                      retention_days=retention_days,
                                                                                      addtocart_evnet_name="AddToCart",
                                                                                      contain_list=utm_ids)
                    description = self.make_description("UTM타겟", retention_days, "장바구니이용고객", "", "custom", request.data, custom_data)
                # 전환완료 고객
                elif detail == "conversion":
                    # TODO 전환완료 이벤트 확인
                    created_target = targeting_url.create_specific_page_and_coversion_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent", contain_list=utm_ids)
                    description = self.make_description("UTM타겟", retention_days, "전환완료고객", "", "custom", request.data, custom_data)
                # 미 전환 고객
                elif detail == "non_conversion":
                    # TODO 전환완료 이벤트 확인
                    created_target = targeting_url.create_url_and_non_coversion_customers(fb_ad_account.act_account_id,
                                                                                          name, pixel_id,
                                                                                          retention_days=retention_days,
                                                                                          conversion_event_name="ViewContent",
                                                                                          contain_list=utm_ids)
                    description = self.make_description("UTM타겟", retention_days, "미전환고객", "", "custom", request.data, custom_data)
                # 회원가입 고객
                elif detail == "registration":
                    # TODO 회원가입 이벤트 확인
                    created_target = targeting_url.create_specific_page_and_registration_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        registration_event_name="CompleteRegistration", contain_list=utm_ids)
                    description = self.make_description("UTM타겟", retention_days, "회원가입고객", "", "custom", request.data, custom_data)
                else:
                    raise Exception("No valid detail parameter")

            # 구매
            elif target_type == "purchase":
                detail = request.data.get('detail', '')

                pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory,
                                                                                                  'purchase')

                if detail == "total":
                    created_target = targeting_purchase.create_purchase_customers(fb_ad_account.act_account_id, name,
                                                                                  pixel_id,
                                                                                  retention_days=retention_days,
                                                                                  purchase_event_name="Purchase")
                    description = self.make_description("구매", retention_days, "전체", "", "custom", request.data)
                elif detail == "purchase_count":
                    purchase_count = request.data.get('purchase_count', 0)
                    created_target = targeting_purchase.create_more_than_x_timtes_purchase_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        purchase_evnet_name="Purchase", purchase_cnt=purchase_count)
                    description = self.make_description("구매", retention_days, "구매횟수", str(purchase_count), "custom", request.data, { "purchase_count": purchase_count })
                elif detail == "purchase_amount":
                    purchase_amount = request.data.get('purchase_amount', 0)
                    created_target = targeting_purchase.create_more_than_x_amount_purchjase_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        purchase_evnet_name="Purchase", minimum_val=purchase_amount)
                    description = self.make_description("구매", retention_days, "구매금액", purchase_amount, "custom", request.data, { "purchase_amount": purchase_amount })
                else:
                    raise Exception("No valid detail parameter")

            # 장바구니
            elif target_type == "add_to_cart":
                detail = request.data.get('detail', '')

                pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory,
                                                                                                  'add to cart')

                if detail == "total":
                    created_target = targeting_addtocart.create_addtocart_customers(fb_ad_account.act_account_id, name,
                                                                                    pixel_id,
                                                                                    retention_days=retention_days,
                                                                                    addtocart_event_name="AddToCart")
                    description = self.make_description("장바구니", retention_days, "전체", "", "custom", request.data)
                elif detail == "non_purchase":
                    created_target = targeting_addtocart.create_addtocart_and_non_purchase_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        addtocart_evnet_name="AddToCart", puchase_event_name="Purchase")
                    description = self.make_description("장바구니", retention_days, "미구매고객", "", "custom", request.data)
                else:
                    raise Exception("No valid detail parameter")

            # 회원가입
            elif target_type == "registration":
                detail = request.data.get('detail', '')

                pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory,
                                                                                                  'registration')

                if detail == "total":
                    created_target = targeting_registration.create_regestration_customers(fb_ad_account.act_account_id,
                                                                                          name, pixel_id,
                                                                                          retention_days=retention_days,
                                                                                          registration_event_name="CompleteRegistration")
                    description = self.make_description("회원가입", retention_days, "전체", "", "custom", request.data)
                elif detail == "usage_time_top":
                    input_percent = request.data.get('input_percent', 25)
                    created_target = targeting_registration.create_regestration_usage_time_top_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        regestration_event_name="CompleteRegistration", input_percent=input_percent)
                    description = self.make_description("회원가입", retention_days, "이용시간상위" + str(input_percent) + "%", "", "custom", request.data)
                elif detail == "non_purchase":
                    created_target = targeting_registration.create_regestration_and_non_purchase_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        regestration_event_name="CompleteRegistration",
                        purchase_event_name="Purchase")
                    description = self.make_description("회원가입", retention_days, "미구매", "", "custom", request.data)
                elif detail == "conversion":
                    created_target = targeting_registration.create_regestration_and_conversion_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=30,
                        regestration_event_name="CompleteRegistration",
                        conversion_event_name="ViewContent")
                    description = self.make_description("회원가입", retention_days, "전환고객", "", "custom", request.data)
                elif detail == "non_conversion":
                    created_target = targeting_registration.create_regestration_non_conversion_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=30,
                        regestration_event_name="CompleteRegistration",
                        conversion_event_name="ViewContent")
                    description = self.make_description("회원가입", retention_days, "미전환고객", "", "custom", request.data)
                else:
                    raise Exception("No valid detail parameter")

            elif target_type == "conversion":
                pass

            else:
                raise  Exception("No valid target_type.")

            target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account, created_target.get('id'),
                                                  pixel_mapping_category, json.dumps(description), username='test')
            serializer = PickdataAccountTargetSerializer(target)

            response_data['success'] = 'YES'
            response_data['data'] = serializer.data

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Exception as e:
            logger.error(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")
