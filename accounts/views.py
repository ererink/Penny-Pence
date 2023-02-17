from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
import env
import requests
from json.decoder import JSONDecodeError
from accounts.models import User
from allauth.socialaccount.models import SocialAccount
from django.http import JsonResponse
from rest_framework import status
from json.decoder import JSONDecodeError
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.decorators import api_view
from accounts.serializers import UserInfo
from rest_framework.permissions import IsAuthenticated

from rest_framework import serializers
from rest_framework import authentication, viewsets

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
BASE_URL = 'http://localhost:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback/'


# 카카오 로그인
def kakao_login(request):
    rest_api_key = env.KAKAO_REST_API_KEY
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code")

def kakao_callback(request):
    rest_api_key = env.KAKAO_REST_API_KEY
    code = request.GET.get('code')
    redirect_uri = KAKAO_CALLBACK_URI
    # redirect_uri = "https://master.d3n2xysrd0lvj9.amplifyapp.com/oauth/callback/kakao"
    
    # Access Token Request
    token_req = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}")
    token_req_json = token_req.json()       # json으로 변환
    error = token_req_json.get('error')     # 에러 부분 파싱
    
    if error is not None:
        raise JSONDecodeError(error)
    
    access_token = token_req_json.get("access_token")

    # Email Request
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    kakao_account = profile_json.get('kakao_account')
    
    # print(kakao_account) 
    # => 이메일, 프로필 사진, 배경 사진 url 가져올 수 있음
    email = kakao_account.get('email')
    profile = kakao_account.get('profile')
    nickname = profile.get('nickname')
    profile_img = profile.get('profile_image_url')
    print(profile)
    print(nickname)
    print(profile_img)
    
    # Signup or Login Request
    try:
        user = User.objects.get(email=email)               
        social_user = SocialAccount.objects.get(user=user)
        
        # if social_user is None:
        #     return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {'access_token': access_token, 'code': code}
        
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        
        accept_json = accept.json()
        
        # 사용자 정보 저장
        User.objects.filter(email=email).update(nickname=nickname, profile_img=profile_img)

        return JsonResponse(accept_json)
    
    # 가입된 유저가 아닐 시 가입
    except User.DoesNotExist:
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        
        # 사용자의 pk, email, first name, last name과 Access Token, Refresh token 가져오기
        accept_json = accept.json()
        
        # 사용자 카카오 정보 저장 (이름, 프로필 사진)
        User.objects.filter(email=email).update(nickname=nickname, profile_img=profile_img)
                
        return JsonResponse(accept_json)

class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
    
    
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]      # 인증된 사용자만 회원 정보 수정
    
    # 유저 정보 출력
    def get(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        serializers = UserInfo(user)
        return Response(serializers.data)
    
    # 유저 정보 수정
    def put(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        if user.pk != user_pk:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        else: 
            serializers = UserInfo(user, data=request.data)
            
            if serializers.is_valid(raise_exception=True):              
                serializers.save()
                return Response(serializers.data)
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)