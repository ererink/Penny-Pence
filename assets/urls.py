from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RankingViewSet, NewsViewSet, User_PositionsViewSet
from . import views
# Swagger API
from assets.views import TestView


router = DefaultRouter()
router.register('news', NewsViewSet)
router.register('ranking', RankingViewSet, basename='ranking')
router.register('positions', User_PositionsViewSet, basename='positions')

urlpatterns = [
    path('', include(router.urls)),
    # path('ranking/<int:pk>/', RankingViewSet.as_view({'get': 'get_ranking_by_game_date'}), name='ranking-game-date')
    path('v1/test/', TestView.as_view(), name='test'),
    
    # DB 저장용[사용안하는 주소]
    # path('game/', views.date_create),
    # path('data_input/', views.save_sector)
]

