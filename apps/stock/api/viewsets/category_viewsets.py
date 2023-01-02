from rest_framework.viewsets import ModelViewSet

from core.viewsets import FieldRequestViewsetMixin
from .. import serializers


class CategoryViewSet(FieldRequestViewsetMixin, ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = serializers.CategorySerializer.Meta.model.objects.get_queryset()
