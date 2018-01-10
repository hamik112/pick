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

                gen_obj['audience_id'] = audience_id
                gen_obj['description'] = string_to_literal(pickdata_target.description)
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
                    if operation_status_code == 441:
                        display_count = "생성중"
                    elif delivery_status_code == 300:
                        display_count = "규모가 적음"
                    elif delivery_status_code == 200:
                        display_count = audience_target.get('approximate_count')

                    gen_obj['display_count'] = display_count
                    gen_obj['name'] = audience_target.get('name')
                    gen_obj['approximate_count'] = audience_target.get('approximate_count')
                    gen_obj['delivery_status'] = audience_target.get('delivery_status')
                    gen_obj['operation_status'] = audience_target.get('operation_status')
                    gen_obj['pixel_id'] = audience_target.get('pixel_id')

                    group_target['total'].append(gen_obj)
                    group_target[group_category[pixel_mapping_category_id]].append(gen_obj)

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