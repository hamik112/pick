from rest_framework import serializers
from .models import PixelMapping


class PixelMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PixelMapping
        fields = '__all__'
