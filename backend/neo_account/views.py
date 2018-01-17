from django.http import HttpResponse

from rest_framework.views import APIView
from neo_account.models import NeoAccount

import traceback
import logging
import json

logger = logging.getLogger(__name__)


class NeoAccountView(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:

            fb_ad_account_id = request.query_params.get('fb_ad_account_id', 0)

            neo_accounts = NeoAccount.get_list_by_fb_ad_account_id(NeoAccount, fb_ad_account_id)

            response_data['success'] = 'YES'
            response_data['count'] = len(neo_accounts)
            response_data['data'] = neo_accounts

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    def post(self, request, format=None):
        response_data = {}
        try:

            fb_ad_account_id = request.data.get('fb_ad_account_id', 0)
            neo_adv_ids = request.data.getlist('neo_adv_ids', [])
            neo_account_ids = request.data.getlist('neo_account_ids', [])

            create_cnt = NeoAccount.create_list(self, fb_ad_account_id, neo_adv_ids, neo_account_ids)

            response_data['success'] = 'YES'
            response_data['count'] = create_cnt

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")