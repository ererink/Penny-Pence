from rest_framework import serializers
from .models import Question, Comment, Like, Article

class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_like_count(self, obj):
        return obj.likes.count()
    

class QuestionSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'