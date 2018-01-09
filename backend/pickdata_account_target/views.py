from rest_framework import viewsets
from .models import PickdataAccountTarget
from .serializers import PickdataAccountTargetSerializer


class PickdataAccountTargetViewSet(viewsets.ModelViewSet):
    queryset = PickdataAccountTarget.objects.all()
    serializer_class = PickdataAccountTargetSerializer
