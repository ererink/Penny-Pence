from django.urls import path, include
from rest_framework import routers
from .views import QuestionViewSet, CommentViewSet, LikeViewSet, ArticleViewSet

router = routers.DefaultRouter()
router.register('question', QuestionViewSet)
router.register('article', ArticleViewSet)
router.register('comments', CommentViewSet)
router.register('likes', LikeViewSet, basename='like')

urlpatterns = [
    path('', include(router.urls)),
]