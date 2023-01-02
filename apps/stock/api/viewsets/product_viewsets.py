from rest_framework.viewsets import ModelViewSet

from core.viewsets import FieldRequestViewsetMixin
from .. import serializers


class ProductViewSet(FieldRequestViewsetMixin, ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = serializers.ProductSerializer.Meta.model.objects.get_queryset()
    filterset_fields = ('category', 'active', 'category__active')
