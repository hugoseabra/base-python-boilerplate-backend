from rest_framework import serializers

from core.serializers import FormSerializerMixin
from ... import forms


class SimpleCategorySerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.CategoryForm
        model = forms.CategoryForm.Meta.model
        fields = (
            'pk',
            'name',
            'active',
        )


class CategorySerializer(SimpleCategorySerializer):
    class Meta(SimpleCategorySerializer.Meta):
        fields = SimpleCategorySerializer.Meta.fields + (
            'created_at',
            'updated_at',
        )
