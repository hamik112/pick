from rest_framework import serializers
from .models import PixelMapping

from fb_ad_account.serializers import FbAdAccountSerializer
from pixel_mapping_category.serializers import PixelMappingCategorySerializer

class PixelMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PixelMapping
        fields = '__all__'


class PixelMappingMergeSerializer(serializers.ModelSerializer):
    fb_ad_account = FbAdAccountSerializer(read_only=True)
    pixel_mapping_category = PixelMappingCategorySerializer(read_only=True)

    class Meta:
        model = PixelMapping
        fields = '__all__'