from rest_framework import serializers
from .models import FbAdAccount


class FbAdAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FbAdAccount
        fields = '__all__'
