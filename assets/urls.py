from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RankingViewSet, NewsViewSet
from . import views

# # news 리스트 보여주기
# news_list = NewsViewSet.as_view({
#     'get': 'list',
#     # 'post': 'create'
# })

# ranking 리스트 보여주기
ranking_list = RankingViewSet.as_view({
    'get': 'list'
})


urlpatterns = [
    # path('news/', news_list),
    path('ranking/', ranking_list),
    path('game/', views.date_create),
    path('sector/', views.sector),
    # path('data_input/', views.save_sector)
]

