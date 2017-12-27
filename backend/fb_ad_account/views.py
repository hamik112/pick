from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from fb_ad_account.models import FbAdAccount

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
