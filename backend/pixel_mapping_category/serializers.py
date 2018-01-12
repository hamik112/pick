from rest_framework import serializers
from .models import PixelMappingCategory

class PixelMappingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PixelMappingCategory
        fields = '__all__'
