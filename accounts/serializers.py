from rest_framework import serializers

from .models import User
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework.validators import UniqueValidator

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'nickname',
            'profile_img',
            'edited_img',
            'email',
            'money',
            'inventory',
            'school',
            'position',
            'followers',
            'following',
        )
        read_only_fields = ('email', 'money', 'inventory', 'school', 'followers', 'following')

class KakaoLoginSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    profile_img = serializers.URLField()
    access_token = serializers.CharField()

class SchoolSerializer(serializers.Serializer):
    school_name = serializers.CharField(required=False)

 # 프로필 이미지 업데이트
class ProfileImageSerializer(serializers.ModelSerializer):
    edited_img = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = ('edited_img',)

# 닉네임 중복 검사
class NicknameUniqueCheckSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=True, min_length=1, max_length=30, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('nickname',)
        
          
class UserInfo(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)
    school_name = serializers.CharField(source='school', required=False)
    edited_img = serializers.ImageField(max_length=None, use_url=True, required=False)
    inventory = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('email', 'password', 'school', 'followers', 'inventory')

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.profile_img = validated_data.get('profile_img', instance.profile_img)
        instance.school = validated_data.get('school', instance.school)
        instance.edited_img = validated_data.get('edited_img', instance.edited_img)
        instance.inventory = validated_data.get('inventory', instance.inventory)
        instance.save()

        return instance