from django.urls import path, include
from rest_framework import routers
from .views import QuestionViewSet, CommentViewSet, LikeViewSet

router = routers.DefaultRouter()
router.register('', QuestionViewSet)
router.register('comments', CommentViewSet)
router.register('likes', LikeViewSet, basename='like')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:question_pk>/comment/', CommentViewSet.as_view({'post': 'create', 'put': 'update', 'delete':'destroy'})),
]