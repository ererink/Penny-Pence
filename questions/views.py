from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Question, Comment, Like
from .serializers import QuestionSerializer, CommentSerializer, LikeSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

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
        question = self.get_object()
        comments = Comment.objects.filter(question=question, parent=None).prefetch_related('likes', 'replies__likes')
        serializer = CommentSerializer(comments, many=True)
        data = serializer.data
        return Response(data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        question = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(question=question, user=user)
            like.delete()
            return Response({'detail': 'Question unliked.'})
        except Like.DoesNotExist:
            like = Like(question=question, user=user)
            like.save()
            return Response({'detail': 'Question liked.'})


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(comment=comment, user=user)
            like.delete()
            return Response({'detail': 'Comment unliked.'})
        except Like.DoesNotExist:
            like = Like(comment=comment, user=user)
            like.save()
            return Response({'detail': 'Comment liked.'})
        
    @action(detail=True, methods=['post'])
    def replies(self, request, pk=None):
        parent_comment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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