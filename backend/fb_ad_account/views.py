from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from fb_ad_account.models import FbAdAccount

from neo_account.models import NeoAccount
from pixel_mapping.models import PixelMapping
from pixel_mapping_category.models import PixelMappingCategory
from pickdata_account_target.models import PickdataAccountTarget

from utils.facebookapis.targeting import targeting_visitor
from utils.facebookapis.targeting import targeting_addtocart
from utils.facebookapis.targeting import targeting_conversion
from utils.facebookapis.targeting import targeting_registration
from utils.facebookapis.targeting import targeting_step
from utils.facebookapis.targeting import targeting_purchase

import json
import logging
import traceback
import pprint

from utils.facebookapis.api_init import (api_init, api_init_by_system_user)
from utils.facebookapis.ad_account import (ad_accounts, ads_pixels)

logger = logging.getLogger(__name__)


class FbAdAccountList(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            api_init_by_system_user()
            # TODO Session token

            me_accounts = ad_accounts.get_my_ad_accounts()

            response_data['success'] = 'YES'
            response_data['count'] = len(me_accounts)
            response_data['data'] = me_accounts

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")

class CheckAccountId(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            api_init_by_system_user()
            # TODO Session token

            account_id = request.query_params.get('act_account_id', None)

            # print(ad_accounts.get_ad_account(account_id))

            default_pixel = ads_pixels.get_account_default_pixel(account_id)
            if default_pixel != None:
                bool_default_pixel = True
            else:
                bool_default_pixel = False

            fb_ad_account =FbAdAccount.find_by_ad_account_id(FbAdAccount, account_id)
            if fb_ad_account != None:
                bool_fb_ad_account = True
                dic_fb_ad_account = {
                    "fb_ad_account_id":fb_ad_account.id,
                    "name": fb_ad_account.name,
                    "account_status": fb_ad_account.account_status,
                    "account_category_id":fb_ad_account.account_category_id
                }
            else:
                bool_fb_ad_account = False
                fb_ad_account = None

            neo_account_list = []
            if fb_ad_account != None:
                neo_account_list = NeoAccount.get_list_by_fb_ad_account_id(NeoAccount, fb_ad_account_id=fb_ad_account.id)
                pixel_evnet_mapping = PixelMapping.get_list_by_fb_ad_account_id(PixelMapping, fb_ad_account_id=fb_ad_account.id)

                from pixel_mapping.serializers import PixelMappingMergeSerializer

                pixel_evnet_mapping_se = PixelMappingMergeSerializer(pixel_evnet_mapping, many=True)

            response_data['success'] = 'YES'
            response_data['bool_default_pixel'] = bool_default_pixel
            response_data['default_pixel'] = default_pixel
            response_data['bool_fb_ad_account'] = bool_fb_ad_account
            response_data['fb_ad_account'] = dic_fb_ad_account
            response_data['neo_account_list'] = neo_account_list
            response_data['pixel_event_mappings'] = pixel_evnet_mapping_se.data


            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")


class FbAdAccountCategory(APIView):
    def get(self, request, fb_account_id, format=None):
        response_data = {}
        try:
            fb_ad_account = FbAdAccount.find_by_ad_account_id(FbAdAccount, fb_account_id)

            category = None
            if fb_ad_account != None:
                # TODO category
                pass
                # category = fb_ad_account.category

            response_data['success'] = 'YES'
            response_data['account_category'] = category

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    def post(self, request, format=None):
        response_data = {}
        try:
            ad_account_id = request.POST.get('ad_account_id', None)
            name = request.POST.get('ad_account_id', None)
            account_status = request.POST.get('account_status', None)
            account_category = request.POST.get('account_status', None)

            # ad_account_id = models.BigIntegerField()
            # act_account_id = models.CharField(max_length=64)
            # name = models.CharField(max_length=128)
            # account_status = models.IntegerField(default=2)
            # account_category = models.ForeignKey('account_category.AccountCategory', db_constraint=False, null=False)

            response_data['success'] = 'YES'

        except Exception as e:
            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
            logger.error(traceback.format_exc())

        return HttpResponse(json.dumps(response_data), content_type="application/json")

class FbAdAccountDefaultTarget(APIView):
    def get(self, request, fb_account_id, format=None):
        response_data = {}
        try:
            fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_account_id)

            if  fb_ad_account == None:
                raise Exception("FbAdAccount Not Exsit.")

            print(fb_ad_account.id)
            ad_account_name = fb_ad_account.name
            act_account_id = fb_ad_account.act_account_id

            api_init_by_system_user()
            default_pixel = ads_pixels.get_account_default_pixel(act_account_id)

            if default_pixel == None:
                raise Exception("Account Pixel Not Exsit.")

            pixel_id = default_pixel.get('id')

            if pixel_id != '':

                pixel_mappings = PixelMapping.objects.filter(fb_ad_account_id = fb_account_id)

                pixel_categories = {}

                for pixel_mapping in pixel_mappings:
                    pixel_categories[pixel_mapping.pixel_mapping_category_id] = pixel_mapping

                # print("pixel_categories : ", pixel_categories)

                ad_account_name = ad_account_name + "_"

                visit_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory, 'visit pages')
                purchase_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory, 'purchase')
                addtocart_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory, 'add to cart')
                registration_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory, 'registration')
                conversion_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory, 'conversion complete')

                step1_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory, 'conversion 1step')
                step2_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory, 'conversion 2step')
                step3_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory, 'conversion 3step')
                step4_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory, 'conversion 4step')
                step5_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(PixelMappingCategory, 'conversion 5step')


                # print('pixel_mapping_category : ', pixel_mapping_category)
                # print("pixel_mapping_category.id : ", pixel_mapping_category.id)

                #### 기본 1
                name = ad_account_name + "방문 고객_30일간"
                description = {
                    "pixel_mapping_category" : "사이트방문",
                    "retention_days" : 30,
                    "description" : "전체",
                    "option" : ""
                }

                check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, visit_pixel_mapping_category, str(description))

                if check_target:
                    target_audience = targeting_visitor.create_total_customers(act_account_id, name, pixel_id)
                    target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account, target_audience.get('id'), visit_pixel_mapping_category, description)
                    # print(target_audience)

                #### 기본 2
                name = ad_account_name + "미 방문 고객_30일간"
                description = {
                    "pixel_mapping_category" : "사이트방문",
                    "retention_days" : 30,
                    "description" : "미방문고객",
                    "option": ""
                }
                check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, visit_pixel_mapping_category, str(description))

                if check_target:

                    target_audience = targeting_visitor.create_non_visition_customers(act_account_id, name, pixel_id)
                    target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account, target_audience.get('id'), visit_pixel_mapping_category, description)
                    # print(target_audience)

                #### 기본 3
                name = ad_account_name + "이용 시간 상위 5%_30일간"
                description = {
                    "pixel_mapping_category" : "사이트방문",
                    "retention_days" : 30,
                    "description" : "이용시간상위5%",
                    "option": ""
                }

                check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, visit_pixel_mapping_category, str(description))

                if check_target:
                    target_audience = targeting_visitor.create_usage_time_top_customers(act_account_id, name, pixel_id, input_percent=5)
                    target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account, target_audience.get('id'), visit_pixel_mapping_category, description)
                    # print(target_audience)


                #### A
                if purchase_pixel_mapping_category.id in pixel_categories:
                    # print("pixel_category :", pixel_categories.get(purchase_pixel_mapping_category.id))
                    purchase_event_name = pixel_categories.get(purchase_pixel_mapping_category.id).facebook_pixel_event_name

                    #### A-1
                    name = ad_account_name + "방문 고객 중 미 구매고객_30일간"
                    description = {
                        "pixel_mapping_category": "사이트방문",
                        "retention_days": 30,
                        "description": "미구매고객",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, visit_pixel_mapping_category, str(description))
                    if check_target:
                        target_audience = targeting_visitor.create_visitor_and_non_purchase_customers(act_account_id, name, pixel_id, purchase_event_name=purchase_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'), visit_pixel_mapping_category, description)
                        # print(target_audience)

                    #### A-2
                    name = ad_account_name + "구매한 사람_1일간"
                    description = {
                        "pixel_mapping_category": "구매",
                        "retention_days": 1,
                        "description": "전체",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, purchase_pixel_mapping_category, str(description))
                    if check_target:
                        # target_audience = targeting_visitor.create_visitor_and_purchase_customers(act_account_id, name, pixel_id, retention_days=1, purchase_event_name=purchase_event_name)
                        target_audience = targeting_purchase.create_purchase_customers(act_account_id, name, pixel_id, retention_days=1, purchase_event_name=purchase_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'), purchase_pixel_mapping_category,description)
                        # print(target_audience)

                    #### A-3
                    name = ad_account_name + "구매한 사람_7일간"
                    description = {
                        "pixel_mapping_category": "구매",
                        "retention_days": 7,
                        "description": "전체",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, purchase_pixel_mapping_category, str(description))
                    if check_target:
                        # target_audience = targeting_visitor.create_visitor_and_purchase_customers(act_account_id, name, pixel_id, retention_days=7, purchase_event_name=purchase_event_name)
                        target_audience = targeting_purchase.create_purchase_customers(act_account_id, name, pixel_id,retention_days=7,purchase_event_name=purchase_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'), purchase_pixel_mapping_category,description)
                        # print(target_audience)

                    #### A-4
                    name = ad_account_name + "구매한 사람_30일간"
                    description = {
                        "pixel_mapping_category": "구매",
                        "retention_days": 30,
                        "description": "전체",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, purchase_pixel_mapping_category, str(description))
                    if check_target:
                        # target_audience = targeting_visitor.create_visitor_and_purchase_customers(act_account_id, name, pixel_id, retention_days=30, purchase_event_name=purchase_event_name)
                        target_audience = targeting_purchase.create_purchase_customers(act_account_id, name, pixel_id,retention_days=30,purchase_event_name=purchase_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'), purchase_pixel_mapping_category,description)
                        # print(target_audience)

                #### B
                if addtocart_pixel_mapping_category.id in pixel_categories:
                    # print("pixel_category :", pixel_categories.get(addtocart_pixel_mapping_category.id))
                    addtocart_event_name = pixel_categories.get(addtocart_pixel_mapping_category.id).facebook_pixel_event_name

                    #### B-1
                    name = ad_account_name + "장바구니 이용고객_1일간"
                    description = {
                        "pixel_mapping_category": "장바구니",
                        "retention_days": 1,
                        "description": "전체",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, addtocart_pixel_mapping_category, str(description))
                    if check_target:
                        # target_audience = targeting_visitor.create_visitor_and_addtocart_customers(act_account_id, name, pixel_id, retention_days=1, addtocart_evnet_name=addtocart_event_name)
                        target_audience = targeting_addtocart.create_addtocart_customers(act_account_id, name, pixel_id, retention_days=1, addtocart_event_name=addtocart_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'),addtocart_pixel_mapping_category, description)
                        # print(target_audience)

                    #### B-2
                    name = ad_account_name + "장바구니 이용고객_7일간"
                    description = {
                        "pixel_mapping_category": "장바구니",
                        "retention_days": 7,
                        "description": "전체",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,addtocart_pixel_mapping_category,str(description))
                    if check_target:
                        # target_audience = targeting_visitor.create_visitor_and_addtocart_customers(act_account_id, name, pixel_id, retention_days=7, addtocart_evnet_name=addtocart_event_name)
                        target_audience = targeting_addtocart.create_addtocart_customers(act_account_id, name,pixel_id,retention_days=7,addtocart_event_name=addtocart_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'),addtocart_pixel_mapping_category, description)
                        # print(target_audience)

                    if purchase_pixel_mapping_category.id in pixel_categories:
                        #### B-3
                        name = ad_account_name + "장바구니 이용고객 중 미구매고객_1일간"
                        description = {
                            "pixel_mapping_category": "장바구니",
                            "retention_days": 1,
                            "description": "미구매고객",
                            "option": ""
                        }
                        check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,addtocart_pixel_mapping_category,str(description))
                        if check_target:
                           target_audience = targeting_addtocart.create_addtocart_and_non_purchase_customers(act_account_id, name, pixel_id, retention_days=1, addtocart_evnet_name=addtocart_event_name, puchase_event_name=purchase_event_name)
                           target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'),addtocart_pixel_mapping_category, description)
                           print(target_audience)

                        #### B-4
                        name = ad_account_name + "장바구니 이용고객 중 미구매고객_3일간"
                        description = {
                            "pixel_mapping_category": "장바구니",
                            "retention_days": 3,
                            "description": "미구매고객",
                            "option": ""
                        }
                        check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,addtocart_pixel_mapping_category,str(description))
                        if check_target:
                            target_audience = targeting_addtocart.create_addtocart_and_non_purchase_customers(act_account_id, name, pixel_id, retention_days=3, addtocart_evnet_name=addtocart_event_name, puchase_event_name=purchase_event_name)
                            target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'),addtocart_pixel_mapping_category, description)
                            print(target_audience)

                        #### B-5
                        name = ad_account_name + "장바구니 이용고객 중 미구매고객_7일간"
                        description = {
                            "pixel_mapping_category": "장바구니",
                            "retention_days": 7,
                            "description": "미구매고객",
                            "option": ""
                        }
                        check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,addtocart_pixel_mapping_category,str(description))
                        if check_target:
                            target_audience = targeting_addtocart.create_addtocart_and_non_purchase_customers(act_account_id, name, pixel_id, retention_days=7, addtocart_evnet_name=addtocart_event_name, puchase_event_name=purchase_event_name)
                            target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'),addtocart_pixel_mapping_category, description)
                            print(target_audience)


                if conversion_pixel_mapping_category.id in pixel_categories:
                    # print("pixel_category :", pixel_categories.get(conversion_pixel_mapping_category.id))
                    conversion_event_name = pixel_categories.get(conversion_pixel_mapping_category.id).facebook_pixel_event_name

                    #### C-1
                    name = ad_account_name + "방문 고객 중 미 전환고객_30일간"
                    description = {

                        "pixel_mapping_category": "사이트방문",
                        "retention_days": 30,
                        "description": "미전환고객",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,visit_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_visitor.create_visitor_and_non_coversion_customers(act_account_id, name, pixel_id, conversion_event_name=conversion_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'),visit_pixel_mapping_category, description)
                        # print(target_audience)

                    #### C-2
                    name = ad_account_name + "전환 완료 고객_30일간"
                    description = {

                        "pixel_mapping_category": "단계별 전환",
                        "retention_days": 30,
                        "description": "전환완료",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,conversion_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_conversion.create_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=conversion_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'), conversion_pixel_mapping_category,description)
                        # print(target_audience)

                    #### C-3
                    name = ad_account_name + "미 전환 고객_30일간"
                    description = {
                        "pixel_mapping_category": "단계별 전환",
                        "retention_days": 30,
                        "description": "미전환",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,conversion_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_visitor.create_visitor_and_non_coversion_customers(act_account_id, name, pixel_id, conversion_event_name=conversion_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'), conversion_pixel_mapping_category,description)
                        # print(target_audience)



                if registration_pixel_mapping_category.id in pixel_categories:
                    # print("pixel_category :", pixel_categories.get(registration_pixel_mapping_category.id))
                    registration_event_name = pixel_categories.get(registration_pixel_mapping_category.id).facebook_pixel_event_name

                    #### D-1
                    name = ad_account_name + "회원가입 완료 고객_30일간"
                    description = {
                        "pixel_mapping_category": "회원가입",
                        "retention_days": 30,
                        "description": "전체",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,registration_pixel_mapping_category,str(description))
                    if check_target:
                        # target_audience = targeting_visitor.create_visitor_and_registration_customers(act_account_id, name, pixel_id, registration_event_name=registration_event_name)
                        target_audience = targeting_registration.create_regestration_customers(act_account_id,name, pixel_id,registration_event_name=registration_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'),registration_pixel_mapping_category, description)
                        # print(target_audience)

                    if purchase_pixel_mapping_category.id in pixel_categories:
                        #### D-2
                        name = ad_account_name + "회원가입 완료 고객 중 미구매 고객_30일간"
                        description = {
                            "pixel_mapping_category": "회원가입",
                            "retention_days": 30,
                            "description": "미구매",
                            "option": ""
                        }
                        check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,registration_pixel_mapping_category,str(description))
                        if check_target:
                            target_audience = targeting_registration.create_regestration_and_non_purchase_customers(act_account_id, name, pixel_id, regestration_event_name=registration_event_name, purchase_event_name=purchase_event_name)
                            target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'),registration_pixel_mapping_category, description)
                            # print(target_audience)

                # E
                if step1_pixel_mapping_category.id in pixel_categories:
                    # print("pixel_category :", pixel_categories.get(step1_pixel_mapping_category.id))
                    step1_event_name = pixel_categories.get(step1_pixel_mapping_category.id).facebook_pixel_event_name

                    name = ad_account_name + "전환 1단계 완료 고객_30일간"
                    description = {
                        "pixel_mapping_category": "단계별 전환",
                        "retention_days": 30,
                        "description": "전환1단계완료",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,step1_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step1_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'),step1_pixel_mapping_category, description)
                        # print(target_audience)


                # F
                if step2_pixel_mapping_category.id in pixel_categories:
                    # print("pixel_category :", pixel_categories.get(step2_pixel_mapping_category.id))
                    step2_event_name = pixel_categories.get(step2_pixel_mapping_category.id).facebook_pixel_event_name

                    name = ad_account_name + "전환 2단계 완료 고객_30일간"
                    description = {
                        "pixel_mapping_category": "단계별 전환",
                        "retention_days": 30,
                        "description": "전환2단계완료",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,step2_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step2_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'),step2_pixel_mapping_category, description)
                        # print(target_audience)

                # G
                if step3_pixel_mapping_category.id in pixel_categories:
                    # print("pixel_category :", pixel_categories.get(step3_pixel_mapping_category.id))
                    step3_event_name = pixel_categories.get(step3_pixel_mapping_category.id).facebook_pixel_event_name

                    name = ad_account_name + "전환 3단계 완료 고객_30일간"
                    description = {
                        "pixel_mapping_category": "단계별 전환",
                        "retention_days": 30,
                        "description": "전환3단계완료",
                        "option": ""
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,step3_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step3_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'), step3_pixel_mapping_category,description)
                        # print(target_audience)

                # H
                if step4_pixel_mapping_category.id in pixel_categories:
                    # print("pixel_category :", pixel_categories.get(step4_pixel_mapping_category.id))
                    step4_event_name = pixel_categories.get(step4_pixel_mapping_category.id).facebook_pixel_event_name

                    name = ad_account_name + "전환 4단계 완료 고객_30일간"
                    description = {
                        "pixel_mapping_category": "단계별 전환",
                        "retention_days": 30,
                        "description": "전환4단계완료",
                        "option": ""
                    }

                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,step4_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step4_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'), step4_pixel_mapping_category,description)
                        # print(target_audience)

                # H
                if step5_pixel_mapping_category.id in pixel_categories:
                    # print("pixel_category :", pixel_categories.get(step5_pixel_mapping_category.id))
                    step_event_name = pixel_categories.get(step5_pixel_mapping_category.id).facebook_pixel_event_name

                    name = ad_account_name + "전환 5단계 완료 고객_30일간"
                    description = {
                        "pixel_mapping_category": "단계별 전환",
                        "retention_days": 30,
                        "description": "전환5단계완료",
                        "option": ""
                    }

                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,step5_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, 'test', fb_ad_account,target_audience.get('id'), step5_pixel_mapping_category,description)
                        # print(target_audience)

            response_data['success'] = 'YES'


        except Exception as e:
            print(traceback.format_exc())

            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
            logger.error(traceback.format_exc())

        return HttpResponse(json.dumps(response_data), content_type="application/json")
