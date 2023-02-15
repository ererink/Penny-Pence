from rest_framework import serializers

from .models import User
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'nickname',
            'profile_img',
            'email',
            # 추가 예정
        )

class UserInfo(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = '__all__'