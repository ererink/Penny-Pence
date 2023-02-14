from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Question, Comment, Like
from .serializers import QuestionSerializer, CommentSerializer, LikeSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        question = self.get_object()
        comments = Comment.objects.filter(question=question)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        question = self.get_object()
        user = request.user
        like, created = Like.objects.get_or_create(user=user, question=question)
        serializer = LikeSerializer(like)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)