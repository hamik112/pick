from rest_framework import viewsets
from .models import AccountPixelMapping
from .serializers import AccountPixelMappingSerializer


class AccountPixelMappingViewSet(viewsets.ModelViewSet):
    queryset = AccountPixelMapping.objects.all()
    serializer_class = AccountPixelMappingSerializer
