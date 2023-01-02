from rest_framework import serializers

from core.serializers import FormSerializerMixin
from ... import forms
from .category_serializers import SimpleCategorySerializer


class ProductSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.ProductForm
        model = forms.ProductForm.Meta.model
        fields = (
            'pk',
            'name',
            'active',
            'created_at',
            'updated_at',
            'category',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        if 'category' in rep:
            rep['category'] = SimpleCategorySerializer(instance=instance.category).data

        return rep
