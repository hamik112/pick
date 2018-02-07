from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from fb_ad_account.models import FbAdAccount
from fb_ad_account.serializers import FbAdAccountSerializer

from neo_account.models import NeoAccount
from pixel_mapping.models import PixelMapping
from pixel_mapping_category.models import PixelMappingCategory
from pickdata_account_target.models import PickdataAccountTarget
from account_category.models import AccountCategory


from utils.facebookapis.ad_account import ads_pixels
from utils.facebookapis.targeting import targeting_visitor
from utils.facebookapis.targeting import targeting_addtocart
from utils.facebookapis.targeting import targeting_conversion
from utils.facebookapis.targeting import targeting_registration
from utils.facebookapis.targeting import targeting_step
from utils.facebookapis.targeting import targeting_purchase

from django.conf import settings

facebook_app_id = settings.FACEBOOK_APP_ID

import json
import logging
import traceback
import pprint

from utils.facebookapis.api_init import (api_init, api_init_by_system_user, api_init_session)
from utils.facebookapis.ad_account import (ad_accounts, ads_pixels)

logger = logging.getLogger(__name__)


class FbAdAccountList(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            if str(facebook_app_id) == "284297631740545":
                api_init_session(request)
            else:
                api_init_by_system_user()

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
    def post(self, request, format=None):
        response_data = {}
        try:
            act_account_id = request.data.get('act_account_id', '')
            account_category_id = request.data.get('account_category_id', '')
            pixel_id = request.data.get('pixel_id', '')

            if str(facebook_app_id) == "284297631740545":
                api_init_session(request)
            else:
                api_init_by_system_user()
            ad_account = ad_accounts.get_ad_account(act_account_id)

            ad_account_id = ad_account.get('account_id')
            act_account_id = ad_account.get('id')
            name = ad_account.get('name')

            account_statsus = ad_account.get('account_status')

            fb_ad_account = FbAdAccount.create(FbAdAccount, ad_account_id, act_account_id, name, account_statsus, account_category_id, pixel_id)

            response_data['success'] = 'YES'
            response_data['data'] = FbAdAccountSerializer(fb_ad_account).data

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
            if str(facebook_app_id) == "284297631740545":
                api_init_session(request)
            else:
                api_init_by_system_user()

            account_id = request.query_params.get('act_account_id', None)

            # print(ad_accounts.get_ad_account(account_id))
            # default_pixel = ads_pixels.get_account_default_pixel(account_id)
            pixels = ads_pixels.get_account_pixels(account_id)

            if len(pixels) > 0:
                bool_default_pixel = True
            else:
                bool_default_pixel = False

            dic_fb_ad_account = {}
            fb_ad_account =FbAdAccount.find_by_ad_account_id(FbAdAccount, account_id)
            if fb_ad_account != None:
                bool_fb_ad_account = True
                dic_fb_ad_account = {
                    "fb_ad_account_id":fb_ad_account.id,
                    "name": fb_ad_account.name,
                    "account_status": fb_ad_account.account_status,
                    "account_category_id":fb_ad_account.account_category_id,
                    "pixel_id":fb_ad_account.pixel_id
                }
            else:
                bool_fb_ad_account = False
                fb_ad_account = None

            neo_account_list = []
            custom_target_details = {}

            if fb_ad_account != None:
                neo_account_list = NeoAccount.get_list_by_fb_ad_account_id(NeoAccount, fb_ad_account_id=fb_ad_account.id)
                pixel_evnet_mapping = PixelMapping.get_list_by_fb_ad_account_id(PixelMapping, fb_ad_account_id=fb_ad_account.id)
                from pixel_mapping.serializers import PixelMappingMergeSerializer
                pixel_evnet_mapping_se = PixelMappingMergeSerializer(pixel_evnet_mapping, many=True)
                custom_target_details = generate_custom_target_details(fb_ad_account.id)

            response_data['success'] = 'YES'
            response_data['bool_default_pixel'] = bool_default_pixel
            response_data['default_pixel'] = pixels
            response_data['bool_fb_ad_account'] = bool_fb_ad_account
            response_data['fb_ad_account'] = dic_fb_ad_account
            response_data['neo_account_list'] = neo_account_list
            response_data['pixel_event_mappings'] = pixel_evnet_mapping_se.data
            response_data['custom_target_details'] = custom_target_details

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")

class FbAdAccountDetail(APIView):
    def get(self, request, pk, format=None):
        response_data = {}
        try:
            fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, pk)

            if fb_ad_account == None:
                response_data['success'] = 'YES'
            else:
                neo_account_list = []
                pixel_event_mapping_list = []

                account_category = AccountCategory.objects.get(pk=fb_ad_account.account_category_id)

                if fb_ad_account != None:
                    dic_fb_ad_account = {
                        "fb_ad_account_id": fb_ad_account.id,
                        "name": fb_ad_account.name,
                        "account_status": fb_ad_account.account_status,
                        "account_category_id": fb_ad_account.account_category_id,
                        "pixel_id": fb_ad_account.pixel_id
                    }

                    neo_account_list = NeoAccount.get_list_by_fb_ad_account_id(NeoAccount, fb_ad_account_id=fb_ad_account.id)
                    pixel_evnet_mappings = PixelMapping.get_list_by_fb_ad_account_id(PixelMapping, fb_ad_account_id=fb_ad_account.id)
                    pixel_event_dic = {pixel_event_mapping.pixel_mapping_category_id: pixel_event_mapping for
                                       pixel_event_mapping in pixel_evnet_mappings}

                    from pixel_mapping.serializers import PixelMappingMergeSerializer

                    list_pixel_event_mapping = []
                    pixel_categories = PixelMappingCategory.get_pixel_mapping_category_for_mapping_view(
                        PixelMappingCategory)
                    for pixel_category in pixel_categories:
                        data = {}
                        pixel_category_id = pixel_category.id
                        pixel_event_mapping = pixel_event_dic.get(pixel_category_id, None)

                        if pixel_event_mapping == None:
                            data["id"] = None
                            data["facebook_pixel_event_name"] = None
                        else:
                            data["id"] = pixel_category_id
                            data["facebook_pixel_event_name"] = pixel_event_mapping.facebook_pixel_event_name

                        data["fb_ad_account"] = dic_fb_ad_account
                        data["pixel_mapping_category"] = {
                            "id": pixel_category.id,
                            "category_label_kr": pixel_category.category_label_kr,
                            "category_label_en": pixel_category.category_label_en
                        }

                        list_pixel_event_mapping.append(data)

                response_data['success'] = 'YES'
                response_data['account_category_id'] = fb_ad_account.account_category_id
                response_data['account_category_name'] = account_category.category_label_kr
                response_data['neo_account_list'] = neo_account_list
                response_data['neo_account_count'] = len(neo_account_list)

                response_data['pixel_event_mappings'] = list_pixel_event_mapping
                response_data['pixel_event_mapping_count'] = len(pixel_evnet_mappings)


                response_data['fb_ad_account'] = FbAdAccountSerializer(fb_ad_account).data

        except Exception as e:
            logger.error(e)
            response_data['success'] = 'NO'
            response_data['msg'] = str(e)

        return HttpResponse(json.dumps(response_data), content_type="application/json")

class AccountPixelEvent(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            act_account_id = request.query_params.get('act_account_id', 0)
            # fb_ad_account_id = request.query_params.get('fb_ad_account_id', 0)
            # fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)

            # if fb_ad_account == None:
            #     raise Exception('Not Exist fb_ad_account.')

            if str(facebook_app_id) == "284297631740545":
                api_init_session(request)
            else:
                api_init_by_system_user()
            # events = ads_pixels.get_account_pixel_events(fb_ad_account.act_account_id)
            events = ads_pixels.get_account_pixel_events(act_account_id)

            response_data['success'] = 'YES'
            response_data['data'] = events

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            logger.error(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")


class PixelEvent(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            pixel_id = request.query_params.get('pixel_id', 0)
            # fb_ad_account_id = request.query_params.get('fb_ad_account_id', 0)
            # fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)

            # if fb_ad_account == None:
            #     raise Exception('Not Exist fb_ad_account.')

            if str(facebook_app_id) == "284297631740545":
                api_init_session(request)
            else:
                api_init_by_system_user()
            # events = ads_pixels.get_account_pixel_events(fb_ad_account.act_account_id)
            events = ads_pixels.get_pixel_events(pixel_id)

            response_data['success'] = 'YES'
            response_data['data'] = events

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            logger.error(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")

class AccountPixel(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            fb_ad_account_id = request.query_params.get('fb_ad_account_id', 0)
            act_account_id = request.query_params.get('act_account_id', '')

            if str(facebook_app_id) == "284297631740545":
                api_init_session(request)
            else:
                api_init_by_system_user()

            if fb_ad_account_id == 0 and act_account_id == '':
                raise  Exception("No Valid Params")

            elif fb_ad_account_id != 0:
                fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)

                if fb_ad_account == None:
                    raise Exception('Not Exist fb_ad_account.')

                pixels = ads_pixels.get_account_pixels(fb_ad_account.act_account_id)

            elif act_account_id != '':
                pixels = ads_pixels.get_account_pixels(act_account_id)

            response_data['success'] = 'YES'
            response_data['data'] = pixels

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            logger.error(traceback.format_exc())
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

            if str(facebook_app_id) == "284297631740545":
                api_init_session(request)
            else:
                api_init_by_system_user()

            # default_pixel = ads_pixels.get_account_default_pixel(act_account_id)
            #
            # if default_pixel == None:
            #     raise Exception("Account Pixel Not Exsit.")
            #
            # pixel_id = default_pixel.get('id')
            pixel_id = fb_ad_account.pixel_id

            if pixel_id != '':

                pixel_mappings = PixelMapping.objects.filter(fb_ad_account_id = fb_account_id)

                pixel_categories = {}

                for pixel_mapping in pixel_mappings:
                    pixel_categories[pixel_mapping.pixel_mapping_category_id] = pixel_mapping

                # print("pixel_categories : ", pixel_categories)

                # ad_account_name = ad_account_name + "_"
                ad_account_name = ""

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
                    "option" : "",
                    "type" : "default"
                }

                check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, visit_pixel_mapping_category, str(description))

                if check_target:
                    target_audience = targeting_visitor.create_total_customers(act_account_id, name, pixel_id)
                    target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account, target_audience.get('id'), visit_pixel_mapping_category, description, username='test')
                    # print(target_audience)

                #### 기본 2
                name = ad_account_name + "미 방문 고객_30일간"
                description = {
                    "pixel_mapping_category" : "사이트방문",
                    "retention_days" : 30,
                    "description" : "미방문고객",
                    "option": "",
                    "type": "default"
                }
                check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, visit_pixel_mapping_category, str(description))

                if check_target:

                    target_audience = targeting_visitor.create_non_visition_customers(act_account_id, name, pixel_id)
                    target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account, target_audience.get('id'), visit_pixel_mapping_category, description, username='test')
                    # print(target_audience)

                #### 기본 3
                name = ad_account_name + "이용 시간 상위 5%_30일간"
                description = {
                    "pixel_mapping_category" : "사이트방문",
                    "retention_days" : 30,
                    "description" : "이용시간상위5%고객",
                    "option": "",
                    "type": "default"
                }

                check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, visit_pixel_mapping_category, str(description))

                if check_target:
                    target_audience = targeting_visitor.create_usage_time_top_customers(act_account_id, name, pixel_id, input_percent=5)
                    target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account, target_audience.get('id'), visit_pixel_mapping_category, description, username='test')
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
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, visit_pixel_mapping_category, str(description))
                    if check_target:
                        target_audience = targeting_visitor.create_visitor_and_non_purchase_customers(act_account_id, name, pixel_id, purchase_event_name=purchase_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'), visit_pixel_mapping_category, description, username='test')
                        # print(target_audience)

                    #### A-2
                    name = ad_account_name + "구매한 사람_1일간"
                    description = {
                        "pixel_mapping_category": "구매",
                        "retention_days": 1,
                        "description": "전체",
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, purchase_pixel_mapping_category, str(description))
                    if check_target:
                        # target_audience = targeting_visitor.create_visitor_and_purchase_customers(act_account_id, name, pixel_id, retention_days=1, purchase_event_name=purchase_event_name)
                        target_audience = targeting_purchase.create_purchase_customers(act_account_id, name, pixel_id, retention_days=1, purchase_event_name=purchase_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'), purchase_pixel_mapping_category,description, username='test')
                        # print(target_audience)

                    #### A-3
                    name = ad_account_name + "구매한 사람_7일간"
                    description = {
                        "pixel_mapping_category": "구매",
                        "retention_days": 7,
                        "description": "전체",
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, purchase_pixel_mapping_category, str(description))
                    if check_target:
                        # target_audience = targeting_visitor.create_visitor_and_purchase_customers(act_account_id, name, pixel_id, retention_days=7, purchase_event_name=purchase_event_name)
                        target_audience = targeting_purchase.create_purchase_customers(act_account_id, name, pixel_id,retention_days=7,purchase_event_name=purchase_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'), purchase_pixel_mapping_category,description, username='test')
                        # print(target_audience)

                    #### A-4
                    name = ad_account_name + "구매한 사람_30일간"
                    description = {
                        "pixel_mapping_category": "구매",
                        "retention_days": 30,
                        "description": "전체",
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, purchase_pixel_mapping_category, str(description))
                    if check_target:
                        # target_audience = targeting_visitor.create_visitor_and_purchase_customers(act_account_id, name, pixel_id, retention_days=30, purchase_event_name=purchase_event_name)
                        target_audience = targeting_purchase.create_purchase_customers(act_account_id, name, pixel_id,retention_days=30,purchase_event_name=purchase_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'), purchase_pixel_mapping_category,description, username='test')
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
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account, addtocart_pixel_mapping_category, str(description))
                    if check_target:
                        # target_audience = targeting_visitor.create_visitor_and_addtocart_customers(act_account_id, name, pixel_id, retention_days=1, addtocart_evnet_name=addtocart_event_name)
                        target_audience = targeting_addtocart.create_addtocart_customers(act_account_id, name, pixel_id, retention_days=1, addtocart_event_name=addtocart_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'),addtocart_pixel_mapping_category, description, username='test')
                        # print(target_audience)

                    #### B-2
                    name = ad_account_name + "장바구니 이용고객_7일간"
                    description = {
                        "pixel_mapping_category": "장바구니",
                        "retention_days": 7,
                        "description": "전체",
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,addtocart_pixel_mapping_category,str(description))
                    if check_target:
                        # target_audience = targeting_visitor.create_visitor_and_addtocart_customers(act_account_id, name, pixel_id, retention_days=7, addtocart_evnet_name=addtocart_event_name)
                        target_audience = targeting_addtocart.create_addtocart_customers(act_account_id, name,pixel_id,retention_days=7,addtocart_event_name=addtocart_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'),addtocart_pixel_mapping_category, description, username='test')
                        # print(target_audience)

                    if purchase_pixel_mapping_category.id in pixel_categories:
                        #### B-3
                        name = ad_account_name + "장바구니 이용고객 중 미구매고객_1일간"
                        description = {
                            "pixel_mapping_category": "장바구니",
                            "retention_days": 1,
                            "description": "미구매고객",
                            "option": "",
                            "type": "default"
                        }
                        check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,addtocart_pixel_mapping_category,str(description))
                        if check_target:
                           target_audience = targeting_addtocart.create_addtocart_and_non_purchase_customers(act_account_id, name, pixel_id, retention_days=1, addtocart_evnet_name=addtocart_event_name, puchase_event_name=purchase_event_name)
                           target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'),addtocart_pixel_mapping_category, description, username='test')
                           print(target_audience)

                        #### B-4
                        name = ad_account_name + "장바구니 이용고객 중 미구매고객_3일간"
                        description = {
                            "pixel_mapping_category": "장바구니",
                            "retention_days": 3,
                            "description": "미구매고객",
                            "option": "",
                            "type": "default"
                        }
                        check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,addtocart_pixel_mapping_category,str(description))
                        if check_target:
                            target_audience = targeting_addtocart.create_addtocart_and_non_purchase_customers(act_account_id, name, pixel_id, retention_days=3, addtocart_evnet_name=addtocart_event_name, puchase_event_name=purchase_event_name)
                            target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'),addtocart_pixel_mapping_category, description, username='test')
                            print(target_audience)

                        #### B-5
                        name = ad_account_name + "장바구니 이용고객 중 미구매고객_7일간"
                        description = {
                            "pixel_mapping_category": "장바구니",
                            "retention_days": 7,
                            "description": "미구매고객",
                            "option": "",
                            "type": "default"
                        }
                        check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,addtocart_pixel_mapping_category,str(description))
                        if check_target:
                            target_audience = targeting_addtocart.create_addtocart_and_non_purchase_customers(act_account_id, name, pixel_id, retention_days=7, addtocart_evnet_name=addtocart_event_name, puchase_event_name=purchase_event_name)
                            target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'),addtocart_pixel_mapping_category, description, username='test')
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
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,visit_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_visitor.create_visitor_and_non_coversion_customers(act_account_id, name, pixel_id, conversion_event_name=conversion_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'),visit_pixel_mapping_category, description, username='test')
                        # print(target_audience)

                    #### C-2
                    name = ad_account_name + "전환 완료 고객_30일간"
                    description = {

                        "pixel_mapping_category": "단계별 전환",
                        "retention_days": 30,
                        "description": "전환완료고객",
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,conversion_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_conversion.create_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=conversion_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'), conversion_pixel_mapping_category,description, username='test')
                        # print(target_audience)

                    #### C-3
                    name = ad_account_name + "미 전환 고객_30일간"
                    description = {
                        "pixel_mapping_category": "단계별 전환",
                        "retention_days": 30,
                        "description": "미전환고객",
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,conversion_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_visitor.create_visitor_and_non_coversion_customers(act_account_id, name, pixel_id, conversion_event_name=conversion_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'), conversion_pixel_mapping_category,description, username='test')
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
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,registration_pixel_mapping_category,str(description))
                    if check_target:
                        # target_audience = targeting_visitor.create_visitor_and_registration_customers(act_account_id, name, pixel_id, registration_event_name=registration_event_name)
                        target_audience = targeting_registration.create_regestration_customers(act_account_id,name, pixel_id,registration_event_name=registration_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'),registration_pixel_mapping_category, description, username='test')
                        # print(target_audience)

                    if purchase_pixel_mapping_category.id in pixel_categories:
                        #### D-2
                        name = ad_account_name + "회원가입 완료 고객 중 미구매 고객_30일간"
                        description = {
                            "pixel_mapping_category": "회원가입",
                            "retention_days": 30,
                            "description": "미구매",
                            "option": "",
                            "type": "default"
                        }
                        check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,registration_pixel_mapping_category,str(description))
                        if check_target:
                            target_audience = targeting_registration.create_regestration_and_non_purchase_customers(act_account_id, name, pixel_id, regestration_event_name=registration_event_name, purchase_event_name=purchase_event_name)
                            target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'),registration_pixel_mapping_category, description, username='test')
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
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,step1_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step1_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'),step1_pixel_mapping_category, description, username='test')
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
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,step2_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step2_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'),step2_pixel_mapping_category, description, username='test')
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
                        "option": "",
                        "type": "default"
                    }
                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,step3_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step3_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'), step3_pixel_mapping_category,description, username='test')
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
                        "option": "",
                        "type": "default"
                    }

                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,step4_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step4_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'), step4_pixel_mapping_category,description, username='test')
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
                        "option": "",
                        "type": "default"
                    }

                    check_target = PickdataAccountTarget.check_by_description(PickdataAccountTarget, fb_ad_account,step5_pixel_mapping_category,str(description))
                    if check_target:
                        target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step_event_name)
                        target = PickdataAccountTarget.create(PickdataAccountTarget, fb_ad_account,target_audience.get('id'), step5_pixel_mapping_category,description, username='test')
                        # print(target_audience)

            response_data['success'] = 'YES'


        except Exception as e:
            print(traceback.format_exc())

            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
            logger.error(traceback.format_exc())

        return HttpResponse(json.dumps(response_data), content_type="application/json")

class FbAdAccountListByCategory(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            accounts = ''
            category_name = request.query_params.get('account_category', 'all')
            if category_name == 'all':
                account_category = AccountCategory.objects.all()
                accounts = FbAdAccount.objects.all()
            else:
                account_category = AccountCategory.objects.filter(category_label_en=category_name)
                for category in account_category:
                    category_id = category.id

                accounts = FbAdAccount.objects.filter(account_category_id=category_id)

            serializer = FbAdAccountSerializer(accounts, many=True)

            response_data['success'] = 'YES'
            response_data['count'] = len(serializer.data)
            response_data['data'] = serializer.data

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")

def generate_custom_target_details(fb_ad_account_id):
    try:
        # pixel_category
        visit_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(
            PixelMappingCategory, 'visit pages')
        purchase_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(
            PixelMappingCategory, 'purchase')
        addtocart_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(
            PixelMappingCategory, 'add to cart')
        registration_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(
            PixelMappingCategory, 'registration')
        conversion_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(
            PixelMappingCategory, 'conversion complete')

        step1_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(
            PixelMappingCategory, 'conversion 1step')
        step2_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(
            PixelMappingCategory, 'conversion 2step')
        step3_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(
            PixelMappingCategory, 'conversion 3step')
        step4_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(
            PixelMappingCategory, 'conversion 4step')
        step5_pixel_mapping_category = PixelMappingCategory.get_pixel_mapping_category_by_label(
            PixelMappingCategory, 'conversion 5step')

        pixel_mappings = PixelMapping.objects.filter(fb_ad_account_id=fb_ad_account_id)

        pixel_categories = {}

        for pixel_mapping in pixel_mappings:
            pixel_categories[pixel_mapping.pixel_mapping_category_id] = pixel_mapping

        is_visit_pixel, is_purchase_pixel, is_addtocart_pixel, is_registration_pixel, is_conversion_pixel, \
        is_step1_pixel, is_step2_pixel, is_step2_pixel, is_step3_pixel, is_step4_pixel, is_step5_pixel = False

        if purchase_pixel_mapping_category.id in pixel_categories:
            is_purchase_pixel = True
        if addtocart_pixel_mapping_category.id in pixel_categories:
            is_addtocart_pixel = True
        if registration_pixel_mapping_category.id in pixel_categories:
            is_registration_pixel = True
        if conversion_pixel_mapping_category.id in pixel_categories:
            is_conversion_pixel = True
        if step1_pixel_mapping_category.id in pixel_categories:
            is_step1_pixel = True
        if step2_pixel_mapping_category.id in pixel_categories:
            is_step2_pixel = True
        if step3_pixel_mapping_category.id in pixel_categories:
            is_step3_pixel = True
        if step4_pixel_mapping_category.id in pixel_categories:
            is_step4_pixel = True
        if step5_pixel_mapping_category.id in pixel_categories:
            is_step5_pixel = True

        total_detail = {
            "name": "전체 고객",
            "value": "total"
        }

        usage_time_top_detail = {
            "name": "이용 시간 상위 고객",
            "value": "usage_time_top"
        }

        non_visit_detail = {
            "name": "특정일 동안 미방문 고객",
            "value": "non_visit"
        }

        purchase_detail = {
            "name": "구매고객",
            "value": "purchase"
        }

        non_purchase_detail = {
            "name": "미 구매고객",
            "value": "non_purchase"
        }

        add_to_cart_detail = {
            "name": "장바구니 이용 고객",
            "value": ""
        }

        conversion_detail = {
            "name": "전환완료 고객",
            "value": "conversion"
        }

        non_conversion_detail = {
            "name": "미 전환 고객",
            "value": "non_conversion"
        }

        registration_detail = {
            "name": "회원가입 고객",
            "value": "registration"
        }

        purchase_count_detail = {
            "name": "특정 구매횟수 이상 구매 고객",
            "value": "purchase_count"
        }

        purchase_amount_detail = {
            "name": "특정 구매금액 이상 구매 고객",
            "value": "purchase_amount"
        }

        default_details = []
        purchase_details = []
        addtocart_details = []
        registration_details = []
        conversion_details = []

        # default_details
        default_details.append(total_detail)
        default_details.append(usage_time_top_detail)
        default_details.append(non_visit_detail)
        if is_purchase_pixel:
            default_details.append(purchase_detail)
            default_details.append(non_purchase_detail)
        if is_addtocart_pixel:
            default_details.append(add_to_cart_detail)
        if is_conversion_pixel:
            default_details.append(conversion_detail)
            default_details.append(non_conversion_detail)
        if is_registration_pixel:
            default_details.append(registration_detail)

        # purchase_details
        if is_purchase_pixel:
            purchase_details.append(total_detail)
            purchase_details.append(purchase_count_detail)
            purchase_details.append(purchase_amount_detail)

        # addtocart details
        if is_addtocart_pixel:
            addtocart_details.append(total_detail)
            if is_purchase_pixel:
                addtocart_details.append(purchase_detail)

        # registration_details
        if is_registration_pixel:
            registration_details.append(total_detail)
            registration_details.append(usage_time_top_detail)
            if is_purchase_pixel:
                registration_details.append(purchase_detail)
            if is_conversion_pixel:
                registration_details.append(conversion_detail)
                registration_details.append(non_conversion_detail)

        # coversion_details
        if is_conversion_pixel:
            conversion_details.append(conversion_detail)
            conversion_details.append(non_conversion_detail)
        if is_step1_pixel:
            conversion_details.append({
                "name": "전환 1단계 완료 고객",
                "value": "conversion 1step"
            })
        if is_step2_pixel:
            conversion_details.append({
                "name": "전환 2단계 완료 고객",
                "value": "conversion 2step"
            })
        if is_step3_pixel:
            conversion_details.append({
                "name": "전환 3단계 완료 고객",
                "value": "conversion 3step"
            })
        if is_step4_pixel:
            conversion_details.append({
                "name": "전환 4단계 완료 고객",
                "value": "conversion 4step"
            })
        if is_step5_pixel:
            conversion_details.append({
                "name": "전환 5단계 완료 고객",
                "value": "conversion 5step"
            })

        conversion_details.append({
            "name": "특정 단계 완료(URL)",
            "value": "conversion url"
        })

        custom_target_details = {
            "default_details":default_details,
            "purchase_details": purchase_details,
            "addtocart_details": addtocart_details,
            "registration_details": registration_details,
            "conversion_details": conversion_details
        }

        return custom_target_details

    except Exception as e:
        print(traceback.format_exc())
        logger.info(traceback.format_exc())
        raise Exception(e)