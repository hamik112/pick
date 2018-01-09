from rest_framework import viewsets
from .models import PixelMapping
from .serializers import PixelMappingSerializer


class PixelMappingViewSet(viewsets.ModelViewSet):
    queryset = PixelMapping.objects.all()
    serializer_class = PixelMappingSerializer
