from rest_framework import serializers
from .models import PickdataAccountTarget
from pixel_mapping_category.serializers import PixelMappingCategorySerializer

class PickdataAccountTargetSerializer(serializers.ModelSerializer):
    # field 명과 변수 이름을 동일하게 맞춰준다.
    pixel_mapping_category = PixelMappingCategorySerializer()
    class Meta:
        model = PickdataAccountTarget
        fields = '__all__'
