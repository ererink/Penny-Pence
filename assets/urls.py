from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RankingViewSet, NewsViewSet
from . import views


ranking_list = RankingViewSet.as_view({
    'get': 'list'
})

urlpatterns = [
    path('news/', views.create_news),
    path('ranking/', ranking_list),
    path('sector/', views.sector),

    # DB 저장용[사용안하는 주소]
    # path('game/', views.date_create),
    # path('data_input/', views.save_sector)
]

