from rest_framework import serializers
from .models import Question, Comment, Like, Article
from accounts.serializers import CustomUserDetailsSerializer
from django.contrib.contenttypes.models import ContentType


def get_filtered_comments(instance, field_name):
    data = {}
    content_type = ContentType.objects.get_for_model(instance)
    comments = Comment.objects.filter(content_type=content_type, object_id=instance.id, parent=None)
    comment_data = CommentSerializer(comments, many=True).data
    data[field_name] = comment_data
    return data

class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer()
    like_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_replies_count(self, obj):
        return obj.replies.count()
    

class QuestionSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer()
    comments = CommentSerializer(many=True, read_only=True) # 위에 replies_count 와 get_replies_count 함수를 사용할 시 이 부분은 주석처리

    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(get_filtered_comments(instance, 'comments'))
        return data

class ArticleSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(get_filtered_comments(instance, 'comments'))
        return data

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'