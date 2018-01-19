from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from pixel_mapping_category.serializers import PixelMappingCategorySerializer
from pixel_mapping_category.models import PixelMappingCategory

import traceback
import logging
import json

logger = logging.getLogger(__name__)

class PixelMappingCategoryView(APIView):
    def get(self, request, format=None):
        response_data = {}
        try:

            option = request.query_params.get('option', "default")

            if option == "default":
                pixel_mapping_categories = PixelMappingCategory.get_default_pixel_mapping_categories(PixelMappingCategory)
            else:
                pixel_mapping_categories = PixelMappingCategory.get_pixel_mapping_categories(PixelMappingCategory)

            serializer = PixelMappingCategorySerializer(pixel_mapping_categories, many=True)

            response_data['success'] = 'YES'
            response_data['count'] = len(pixel_mapping_categories)
            response_data['data'] = serializer.data

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Exception as e:
            print(traceback.format_exc())
            response_data['success'] = 'NO'
            response_data['msg'] = e.args
            return HttpResponse(json.dumps(response_data), content_type="application/json")