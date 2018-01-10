from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from fb_ad_account.models import FbAdAccount

from pixel_mapping.models import PixelMapping

from utils.facebookapis.ad_account import ads_pixels
from utils.facebookapis.targeting import targeting_visitor
from utils.facebookapis.targeting import targeting_addtocart
from utils.facebookapis.targeting import targeting_conversion
from utils.facebookapis.targeting import targeting_registration
from utils.facebookapis.targeting import targeting_step

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
            response_data['data'] = me_accounts
            response_data['count'] = len(me_accounts)

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")


class FbAdAccountPixelCheck(APIView):
    def get(self, request, fb_account_id, format=None):
        response_data = {}
        try:
            api_init_by_system_user()
            # TODO Session token

            default_pixel = ads_pixels.get_account_default_pixel(fb_account_id)

            check_status = False

            if default_pixel != None:
                check_status = True

            response_data['success'] = 'YES'
            response_data['check_status'] = check_status
            response_data['data'] = default_pixel

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

                print("pixel_categories : ", pixel_categories)

                ad_account_name = ad_account_name + "_"

                #### default 개발 완료
                # name = ad_account_name + "방문 고객_30일간"
                # target_audience = targeting_visitor.create_total_customers(act_account_id, name, pixel_id)
                # print(target_audience)
                #
                # name = ad_account_name + "미 방문 고객_30일간"
                # target_audience = targeting_visitor.create_non_visition_customers(act_account_id, name, pixel_id)
                # print(target_audience)
                #
                # name = ad_account_name + "이용 시간 상위 5%_30일간"
                # target_audience = targeting_visitor.create_usage_time_top_customers(act_account_id, name, pixel_id, input_percent=5)
                # print(target_audience)


                #### A
                if 1 in pixel_categories:
                    print("pixel_category :", pixel_categories.get(1))
                    puchase_event_name = pixel_categories.get(1).facebook_pixel_event_name
                    #
                    # name = ad_account_name + "방문 고객 중 미 구매고객_30일간"
                    # target_audience = targeting_visitor.create_visitor_and_non_purchase_customers(act_account_id, name, pixel_id, purchase_evnet_name=puchase_event_name)
                    # print(target_audience)
                    #
                    # name = ad_account_name + "구매한 사람_1일간"
                    # target_audience = targeting_visitor.create_visitor_and_purchase_customers(act_account_id, name, pixel_id, retention_days=1, purchase_evnet_name=puchase_event_name)
                    # print(target_audience)
                    #
                    # name = ad_account_name + "구매한 사람_7일간"
                    # target_audience = targeting_visitor.create_visitor_and_purchase_customers(act_account_id, name, pixel_id, retention_days=7, purchase_evnet_name=puchase_event_name)
                    # print(target_audience)
                    #
                    # name = ad_account_name + "구매한 사람_30일간"
                    # target_audience = targeting_visitor.create_visitor_and_purchase_customers(act_account_id, name, pixel_id, retention_days=30, purchase_evnet_name=puchase_event_name)
                    # print(target_audience)


                #### B
                if 2 in pixel_categories:
                    print("pixel_category :", pixel_categories.get(2))
                    addtocart_event_name = pixel_categories.get(2).facebook_pixel_event_name
                    #
                    # name = ad_account_name + "장바구니 이용고객_1일간"
                    # target_audience = targeting_visitor.create_visitor_and_addtocart_customers(act_account_id, name, pixel_id, retention_days=1, addtocart_evnet_name=addtocart_event_name)
                    # print(target_audience)
                    #
                    # name = ad_account_name + "장바구니 이용고객_7일간"
                    # target_audience = targeting_visitor.create_visitor_and_addtocart_customers(act_account_id, name, pixel_id, retention_days=7, addtocart_evnet_name=addtocart_event_name)
                    # print(target_audience)
                    #
                    # if 1 in pixel_categories:
                    #     name = ad_account_name + "장바구니 이용고객 중 미구매고객_1일간"
                    #     target_audience = targeting_addtocart.create_addtocart_and_non_purchase_customers(act_account_id, name, pixel_id, retention_days=1, addtocart_evnet_name=addtocart_event_name, puchase_event_name=puchase_event_name)
                    #     print(target_audience)
                    #
                    #     name = ad_account_name + "장바구니 이용고객 중 미구매고객_3일간"
                    #     target_audience = targeting_addtocart.create_addtocart_and_non_purchase_customers(act_account_id, name, pixel_id, retention_days=3, addtocart_evnet_name=addtocart_event_name, puchase_event_name=puchase_event_name)
                    #     print(target_audience)
                    #
                    #     name = ad_account_name + "장바구니 이용고객 중 미구매고객_7일간"
                    #     target_audience = targeting_addtocart.create_addtocart_and_non_purchase_customers(act_account_id, name, pixel_id, retention_days=7, addtocart_evnet_name=addtocart_event_name, puchase_event_name=puchase_event_name)
                    #     print(target_audience)

                #### C
                if 3 in pixel_categories:
                    print("pixel_category :", pixel_categories.get(3))
                    conversion_event_name = pixel_categories.get(3).facebook_pixel_event_name

                    # name = ad_account_name + "방문 고객 중 미 구매고객_30일간"
                    # target_audience = targeting_visitor.create_visitor_and_non_coversion_customers(act_account_id, name, pixel_id, conversions_name=conversion_event_name)
                    # print(target_audience)

                    # name = ad_account_name + "전환 완료 고객_30일간"
                    # target_audience = targeting_conversion.create_conversion_customers(act_account_id, name, pixel_id, conversions_name=conversion_event_name)
                    # print(target_audience)

                    # name = ad_account_name + "미 전환 고객_30일간"
                    # target_audience = targeting_visitor.create_visitor_and_non_coversion_customers(act_account_id, name, pixel_id, conversions_name=conversion_event_name)
                    # print(target_audience)



                #### D
                if 4 in pixel_categories:
                    print("pixel_category :", pixel_categories.get(4))
                    registration_event_name = pixel_categories.get(4).facebook_pixel_event_name

                    # name = ad_account_name + "회원가입 완료 고객_30일간"
                    # target_audience = targeting_visitor.create_visitor_and_registration_customers(act_account_id, name, pixel_id, registration_event_name=registration_event_name)
                    # print(target_audience)

                    # if 1 in pixel_categories:
                        # name = ad_account_name + "회원가입 완료 고객 중 미구매 고객_30일간"
                        # target_audience = targeting_registration.create_regestration_and_non_purchase_customers(act_account_id, name, pixel_id, regestration_event_name=registration_event_name, purchase_event_name=puchase_event_name)
                        # print(target_audience)

                # E
                if 5 in pixel_categories:
                    print("pixel_category :", pixel_categories.get(5))
                    step_event_name = pixel_categories.get(5).facebook_pixel_event_name

                    # name = ad_account_name + "전환 1단계 완료 고객_30일간"
                    # target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step_event_name)
                    # print(target_audience)


                # F
                if 6 in pixel_categories:
                    print("pixel_category :", pixel_categories.get(6))
                    step_event_name = pixel_categories.get(6).facebook_pixel_event_name

                    # name = ad_account_name + "전환 2단계 완료 고객_30일간"
                    # target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step_event_name)
                    # print(target_audience)

                # G
                if 7 in pixel_categories:
                    print("pixel_category :", pixel_categories.get(7))
                    step_event_name = pixel_categories.get(7).facebook_pixel_event_name

                    # name = ad_account_name + "전환 3단계 완료 고객_30일간"
                    # target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step_event_name)
                    # print(target_audience)

                # H
                if 8 in pixel_categories:
                    print("pixel_category :", pixel_categories.get(8))
                    step_event_name = pixel_categories.get(8).facebook_pixel_event_name

                    # name = ad_account_name + "전환 4단계 완료 고객_30일간"
                    # target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step_event_name)
                    # print(target_audience)

                # H
                if 9 in pixel_categories:
                    print("pixel_category :", pixel_categories.get(9))
                    step_event_name = pixel_categories.get(9).facebook_pixel_event_name

                    # name = ad_account_name + "전환 5단계 완료 고객_30일간"
                    # target_audience = targeting_step.create_step_conversion_customers(act_account_id, name, pixel_id, conversion_event_name=step_event_name)
                    # print(target_audience)


            response_data['success'] = 'YES'


        except Exception as e:
            print(traceback.format_exc())

            response_data['success'] = 'NO'
            response_data['msg'] = str(e)
            logger.error(traceback.format_exc())

        return HttpResponse(json.dumps(response_data), content_type="application/json")
