from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GameDateViewSet, RankingViewSet, SectorViewSet, NewsViewSet
from . import views

# news 리스트 보여주기
news_list = NewsViewSet.as_view({
    'get': 'list',
    # 'post': 'create'
})

# sector 리스트 보여주기
sector_list = SectorViewSet.as_view({
    'get': 'list',
})

# ranking 리스트 보여주기
ranking_list = RankingViewSet.as_view({
    'get': 'list'
})

# GameDate 게임 일차 -> 나중에 int로 바꿔야할지 고민해보기
GameDate = GameDateViewSet.as_view({
    'get': 'list'
})

urlpatterns = [
    path('news/', news_list),
    path('sector/', sector_list),
    path('ranking/', ranking_list),
    path('gamedate/', GameDate),
]

