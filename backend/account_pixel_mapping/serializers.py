from rest_framework import serializers
from .models import AccountPixelMapping


class AccountPixelMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountPixelMapping
        fields = '__all__'
