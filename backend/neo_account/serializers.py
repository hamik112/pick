from rest_framework import serializers
from .models import NeoAccount


class NeoAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeoAccount
        fields = '__all__'
