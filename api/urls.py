from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, api_root

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include(router.urls)),
]
