from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Question, Comment, Like, Article
from django.contrib.contenttypes.models import ContentType
from .serializers import QuestionSerializer, CommentSerializer, LikeSerializer, ArticleSerializer

class CommunityViewMixin:
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['like_count'] = instance.likes.count()
        return Response(data)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        instance = self.get_object()
        content_type = ContentType.objects.get_for_model(instance)
        comments = Comment.objects.filter(content_type=content_type, object_id=instance.id, parent=None).prefetch_related('likes', 'replies__likes')
        serializer = CommentSerializer(comments, many=True)
        data = serializer.data
        return Response(data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        content_type = ContentType.objects.get_for_model(instance)
        try:
            like = Like.objects.get(content_type=content_type, object_id=instance.id, user=user)
            like.delete()
            like_count = instance.likes.count()
            return Response({'detail': 'Unliked.', 'like_count': like_count})
        except Like.DoesNotExist:
            like = Like(content_object=instance, user=user)
            like.save()
            like_count = instance.likes.count()
            return Response({'detail': 'Liked.', 'like_count': like_count})
        
class QuestionViewSet(CommunityViewMixin, viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ArticleViewSet(CommunityViewMixin, viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        content_type = ContentType.objects.get_for_model(comment)
        try:
            like = Like.objects.get(content_type=content_type, object_id=comment.id, user=user)
            like.delete()
            like_count = comment.likes.count()
            return Response({'detail': 'Comment unliked.', 'like_count': like_count})
        except Like.DoesNotExist:
            like = Like(content_object=comment, user=user)
            like.save()
            like_count = comment.likes.count()
            return Response({'detail': 'Comment liked.', 'like_count': like_count})
        
    @action(detail=True, methods=['post'])
    def replies(self, request, pk=None):
        parent_comment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(self, request.data)
        serializer.save(user=self.request.user, parent=parent_comment)
        return Response(serializer.data)

class LikeViewSet(viewsets.ViewSet):
    serializer_class = LikeSerializer

    @action(detail=False, methods=['get'])
    def question_likes(self, request): 
        question_id = request.query_params.get('question_id', None)
        if not question_id:
            raise ValidationError("Question ID must be provided as a query parameter.")
        likes = Like.objects.filter(question_id=question_id)
        serializer = self.serializer_class(likes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def comment_likes(self, request):
        comment_id = request.query_params.get('comment_id', None)
        if not comment_id:
            raise ValidationError("Comment ID must be provided as a query parameter.")
        likes = Like.objects.filter(comment_id=comment_id)
        serializer = self.serializer_class(likes, many=True)
        return Response(serializer.data)