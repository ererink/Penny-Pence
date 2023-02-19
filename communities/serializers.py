from rest_framework import serializers
from .models import Question, Comment, Like, Article
from accounts.serializers import CustomUserDetailsSerializer
class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer()
    like_count = serializers.SerializerMethodField()
    # replies_count = serializers.SerializerMethodField() # 나중에 서버가 과부하 걸리면 댓글과 대댓글 따로 출력하기 위함.

    class Meta:
        model = Comment
        fields = '__all__'

    def get_like_count(self, obj):
        return obj.likes.count()
    
    # def get_replies_count(self, obj): # 나중에 서버가 과부하 걸리면 댓글과 대댓글 따로 출력하기 위함.
    #     return obj.replies.count()
    

class QuestionSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer()
    comments = CommentSerializer(many=True, read_only=True) # 위에 replies_count 와 get_replies_count 함수를 사용할 시 이 부분은 주석처리

    class Meta:
        model = Question
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'