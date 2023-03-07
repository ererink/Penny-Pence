from django.urls import path, include
from rest_framework import routers
from .views import AuctionItemViewSet

router = routers.DefaultRouter()
router.register('', AuctionItemViewSet, basename='trade')

urlpatterns = [
    path('', include(router.urls)),
]