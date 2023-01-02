from django.contrib import admin

from apps.stock import models
from apps.stock import forms


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Category Admin """
    form = forms.CategoryForm
    search_fields = ('pk', 'name',)
    list_display = ('name', 'active', 'created_at', 'updated_at')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    """ Product Admin """
    form = forms.ProductForm
    search_fields = ('pk', 'name', 'category__name', 'category_id')
    list_display = ('name', 'category', 'active', 'created_at', 'updated_at')
    list_filter = ('category',)
