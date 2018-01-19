from rest_framework import serializers
from .models import PickdataAccountTarget


class PickdataAccountTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickdataAccountTarget
        fields = '__all__'
