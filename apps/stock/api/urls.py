from django.urls import path, include
from rest_framework_nested import routers

from . import viewsets

router = routers.DefaultRouter()

router.register('categories', viewsets.CategoryViewSet)
router.register('products', viewsets.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
