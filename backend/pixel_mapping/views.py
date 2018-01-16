from rest_framework import viewsets
from rest_framework.views import APIView
from .models import PixelMapping
from .serializers import PixelMappingSerializer, PixelMappingMergeSerializer
from django.http import HttpResponse

from fb_ad_account.models import FbAdAccount

import json
import os
import logging
import traceback
import pprint

logger = logging.getLogger(__name__)

class PixelMappingViewSet(viewsets.ModelViewSet):
    queryset = PixelMapping.objects.all()
    serializer_class = PixelMappingSerializer


class PixelMappingView(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:
            fb_ad_account_id = request.query_params.get('fb_ad_account_id', 0)
            fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)

            if fb_ad_account == None:
                raise Exception('Not Exist fb_ad_account.')

            pixel_event_mappings = PixelMapping.get_list_by_fb_ad_account_id(PixelMapping, fb_ad_account_id=fb_ad_account.id)

            serializer = PixelMappingMergeSerializer(pixel_event_mappings, many=True)

            response_data['success'] = 'YES'
            response_data['data'] = serializer.data

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            logger.error(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")


    def post(self, request, format=None):
        response_data = {}
        try:
            fb_ad_account_id = request.POST.get('fb_ad_account_id', 0)
            fb_ad_account = FbAdAccount.find_by_fb_ad_account_id(FbAdAccount, fb_ad_account_id)


            if fb_ad_account == None:
                raise Exception('Not Exist fb_ad_account.')

            facebook_pixel_event_names = request.POST.get('facebook_pixel_event_names', [])
            pixel_mapping_category_ids = request.POST.get('pixel_mapping_category_ids', [])

            username = request.POST.get('username', 'TEST')

            created_cnt = PixelMapping.create(PixelMapping, fb_ad_account, facebook_pixel_event_names=facebook_pixel_event_names, pixel_mapping_category_ids=pixel_mapping_category_ids)

            response_data['success'] = 'YES'
            response_data['count'] = created_cnt

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Exception as e:
            logger.error(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")

