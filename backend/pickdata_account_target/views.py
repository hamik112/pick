from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from fb_ad_account.models import FbAdAccount
from pixel_mapping_category.models import PixelMappingCategory

from .models import PickdataAccountTarget
from .serializers import PickdataAccountTargetSerializer

from utils.facebookapis.api_init import (api_init, api_init_by_system_user)
from utils.facebookapis.ad_account import custom_audiences
from utils.common.string_formatter import string_to_literal

from utils.facebookapis.targeting import targeting_visitor

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
            api_init_by_system_user()

            fb_ad_account_id = request.query_params.get('fb_ad_account_id', None)
            target_type = request.query_params.get('target_type', None)

            if target_type == None:
                target_type = "all"

            fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)
            if fb_ad_account_id == None or fb_ad_account == None:
                raise Exception("Not Existg FbAdAccount.")

            act_account_id = fb_ad_account.act_account_id

            dic_audience_targets = custom_audiences.get_dic_custom_audiences(act_account_id)
            pickdata_targets = PickdataAccountTarget.get_list(PickdataAccountTarget, fb_ad_account_id)


            pixel_mapping_categories = PixelMappingCategory.objects.all()

            group_target = {"total" : []}
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
                audience_id = pickdata_target.target_audience_id
                pixel_mapping_category_id = pickdata_target.pixel_mapping_category_id
                target_description = string_to_literal(pickdata_target.description)

                gen_obj['audience_id'] = audience_id
                gen_obj['description'] = target_description
                gen_obj['pixel_mapping_category_id'] = pixel_mapping_category_id

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
                    "count" : len(group_target[key]),
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

class CustomTarget(APIView):
    def post(self, request, format=None):
        response_data = {}
        try:
            fb_ad_account_id = request.POST.get('fb_ad_account_id', 0)
            fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)

            if fb_ad_account == None:
                raise Exception('Not Exist fb_ad_account.')

            # visit_site, visit_specific_pages, neo_target, utm_target, purchase, add_to_cart, registration,
            target_type = request.POST.get('target_type', 0)
            pixel_id = request.POST.get('pixel_id', 0)
            name = request.POST.get('pixel_id', None)
            retention_days = request.POST.get('retention_days', 30)

            if target_type == "visit_site":
                detail = request.POST.get('detail', '')

                description = {}

                # 전체고객
                if detail == "total":
                    created_target = targeting_visitor.create_total_customers(fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days)
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "전체",
                        "option": "",
                        "type": "custom"
                    }

                # 이용 시간 상위 고객
                elif detail == "usage_time_top":
                    input_percent = request.POST.get('input_percent', 25)
                    created_target = targeting_visitor.create_usage_time_top_customers(fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days, input_percent=input_percent)
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "이용시간상위"+str(input_percent)+"%",
                        "option": "",
                        "type": "custom"
                    }

                # 특정일 동안 미방문 고객
                elif detail == "non_visition":
                    created_target = targeting_visitor.create_non_visition_customers(fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days)
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "미방문고객",
                        "option": "",
                        "type": "custom"
                    }

                # 구매고객
                elif detail == "purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_visitor.create_visitor_and_purchase_customers(fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days, purchase_event_name="Purchase")
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "구매고객",
                        "option": "",
                        "type": "custom"
                    }

                # 미 구매고객
                elif detail == "non_purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_visitor.create_visitor_and_non_purchase_customers(fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days, purchase_event_name="Purchase")
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "미구매고객",
                        "option": "",
                        "type": "custom"
                    }

                # 장바구니 이용 고객
                elif detail == "addtocart":
                    # TODO 장바구니 이벤트 확인
                    created_target = targeting_visitor.create_visitor_and_addtocart_customers(fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days, addtocart_evnet_name="AddToCart")
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "장바구니이용고객",
                        "option": "",
                        "type": "custom"
                    }

                # 전환완료 고객
                elif detail == "conversion":
                    # TODO 전환완료 이벤트 확인
                    created_target = targeting_visitor.create_visitor_and_coversion_customers(fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days, conversion_event_name="ViewContent")
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "전환완료고객",
                        "option": "",
                        "type": "custom"
                    }

                # 미 전환 고객
                elif detail == "non_conversion":
                    # TODO 전환완료 이벤트 확인
                    create_target = targeting_visitor.create_visitor_and_non_coversion_customers(fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days, conversion_event_name="ViewContent")
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "미전환고객",
                        "option": "",
                        "type": "custom"
                    }
                # 회원가입 고객
                elif detail == "registration":
                    # TODO 회원가입 이벤트 확인
                    created_target = targeting_visitor.create_visitor_and_registration_customers(fb_ad_account.act_account_id, name, pixel_id, retention_days=30, registration_event_name="CompleteRegistration")
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "회원가입고객",
                        "option": "",
                        "type": "custom"
                    }
                else:
                    raise Exception("No valid detail parameter")

            elif target_type == "visit_specific_pages":
                total_urls = request.POST.getlist('total_urls')
                part_urls = request.POST.getlist('part_urls')
                detail = request.POST.get('detail', '')

                description = {}

                # 전체고객
                if detail == "total":
                    created_target = targeting_visitor.create_total_customers(fb_ad_account.act_account_id, name,
                                                                              pixel_id, retention_days=retention_days)
                    description = {
                        "pixel_mapping_category": "특정페이지방문",
                        "retention_days": retention_days,
                        "description": "전체",
                        "option": "",
                        "type": "custom"
                    }

                # 이용 시간 상위 고객
                elif detail == "usage_time_top":
                    input_percent = request.POST.get('input_percent', 25)
                    created_target = targeting_visitor.create_usage_time_top_customers(fb_ad_account.act_account_id,
                                                                                       name, pixel_id,
                                                                                       retention_days=retention_days,
                                                                                       input_percent=input_percent)
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "이용시간상위" + str(input_percent) + "%",
                        "option": "",
                        "type": "custom"
                    }

                # 특정일 동안 미방문 고객
                elif detail == "non_visition":
                    created_target = targeting_visitor.create_non_visition_customers(fb_ad_account.act_account_id, name,
                                                                                     pixel_id,
                                                                                     retention_days=retention_days)
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "미방문고객",
                        "option": "",
                        "type": "custom"
                    }

                # 구매고객
                elif detail == "purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_visitor.create_visitor_and_purchase_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        purchase_event_name="Purchase")
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "구매고객",
                        "option": "",
                        "type": "custom"
                    }

                # 미 구매고객
                elif detail == "non_purchase":
                    # TODO DB 구매 이벤트 유무 확인
                    created_target = targeting_visitor.create_visitor_and_non_purchase_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        purchase_event_name="Purchase")
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "미구매고객",
                        "option": "",
                        "type": "custom"
                    }

                # 장바구니 이용 고객
                elif detail == "addtocart":
                    # TODO 장바구니 이벤트 확인
                    created_target = targeting_visitor.create_visitor_and_addtocart_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        addtocart_evnet_name="AddToCart")
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "장바구니이용고객",
                        "option": "",
                        "type": "custom"
                    }

                # 전환완료 고객
                elif detail == "conversion":
                    # TODO 전환완료 이벤트 확인
                    created_target = targeting_visitor.create_visitor_and_coversion_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent")
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "전환완료고객",
                        "option": "",
                        "type": "custom"
                    }

                # 미 전환 고객
                elif detail == "non_conversion":
                    # TODO 전환완료 이벤트 확인
                    create_target = targeting_visitor.create_visitor_and_non_coversion_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=retention_days,
                        conversion_event_name="ViewContent")
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "미전환고객",
                        "option": "",
                        "type": "custom"
                    }
                # 회원가입 고객
                elif detail == "registration":
                    # TODO 회원가입 이벤트 확인
                    created_target = targeting_visitor.create_visitor_and_registration_customers(
                        fb_ad_account.act_account_id, name, pixel_id, retention_days=30,
                        registration_event_name="CompleteRegistration")
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": retention_days,
                        "description": "회원가입고객",
                        "option": "",
                        "type": "custom"
                    }
                else:
                    raise Exception("No valid detail parameter")

                pass
            elif target_type == "neo_target":
                keywords = request.POST.getlist('keywords')
                neo_ids = request.POST.getlist('neo_ids')
                neo_type = request.POST.getlist('neo_type')

                pass
            elif target_type == "utm_target":
                sources = request.POST.getlist('sources')
                mediums = request.POST.getlist('mediums')
                campaigns = request.POST.getlist('campaigns')
                terms = request.POST.getlist('terms')
                contents = request.POST.getlist('contents')
                customs = request.POST.getlist('customs')

                pass
            elif target_type == "purchase":
                pass
            elif target_type == "add_to_cart":
                pass
            elif target_type == "registration":
                pass
            elif target_type == "":
                pass

            response_data['success'] = 'YES'

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Exception as e:
            logger.error(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")



