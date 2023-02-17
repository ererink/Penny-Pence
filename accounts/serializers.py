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
            'money'
            # 추가 예정
        )
        read_only_fields = ('email', 'money', )

class UserInfo(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('email', 'password',)

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('username', instance.nickname)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.profile_img = validated_data.get('profile_img', instance.profile_img)
        instance.school = validated_data.get('school', instance.school)
        instance.save()

        return instance