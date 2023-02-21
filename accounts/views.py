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
from accounts.serializers import UserInfo, SchoolSerializer, KakaoLoginSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework import serializers
from rest_framework import authentication, viewsets

from Neis_API import Region, School

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
    
    '''
    print(token_req_json)
    
    {'access_token': '...', 
    'token_type': 'bearer', 'refresh_token': '...', 
    'expires_in': 00000, 'scope': 'age_range birthday account_email profile_image gender profile_nickname', 
    'refresh_token_expires_in': 0000000}
    '''
    error = token_req_json.get('error')     # 에러 부분 파싱
    
    if error is not None:
        raise JSONDecodeError(error)
    
    access_token = token_req_json.get("access_token")
    refresh_token = token_req_json.get("refresh_token")

    # Email Request
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    kakao_account = profile_json.get('kakao_account')
    # print(kakao_account) 
    
    # 이메일, 프로필 사진, 배경 사진 url 가져오기
    email = kakao_account.get('email')
    profile = kakao_account.get('profile')
    nickname = profile.get('nickname')
    profile_img = profile.get('profile_image_url')
    # print(profile)
    # print(nickname)
    # print(profile_img)
    
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
        # print(accept_json)

        # 사용자 정보 저장
        User.objects.filter(email=email).update(nickname=nickname, profile_img=profile_img)

        data = {
            'nickname': nickname,
            'profile_img': profile_img,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'accept_json': accept_json,             
        }
        print(data)
        serializer = KakaoLoginSerializer(data)
        
        return JsonResponse(serializer.data)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        
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
        
        data = {
            'nickname': nickname,
            'profile_img': profile_img,
            'access_token': access_token,
            'refresh_token': refresh_token,            
        }
        print(data)
        serializer = KakaoLoginSerializer(data)

        return JsonResponse(serializer.data)
        # return Response(serializer.data, status=status.HTTP_200_OK)


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

class Follow(APIView):
    serializer_class = UserSerializer

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        if request.user == user:
            return Response({"detail": "자신을 팔로우할 수 없아요!"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user in user.followers.all():
            return Response({"detail": "이미 친구예요"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.followers.add(request.user)
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

class Unfollow(APIView):
    serializer_class = UserSerializer

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        if not request.user.following.filter(id=user_id).exists():
            return Response({"detail": "친구가 아니예요"}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.following.remove(user)
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchSchool(APIView):
    serializer_class = SchoolSerializer
        
    def get(self, request):
        api_key = env.NEIS_API_KEY
        query = request.GET.get('query')    # 검색어 입력
        if not query:
            return Response({'error': '검색어가 없어요'}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(f'https://open.neis.go.kr/hub/schoolInfo?KEY={api_key}&Type=json&pIndex=1&pSize=100&SCHUL_NM=한내초등학교')
        data = response.json()
        # print(data)
        '''
        data 출력 형태
        {'schoolInfo': [{'head': [{'list_total_count': 1}, {'RESULT': {'CODE': 'INFO-000', 'MESSAGE': '정상 처리되었습니다.'}}]}, 
        {'row': [{'ATPT_OFCDC_SC_CODE': 'B10', 'ATPT_OFCDC_SC_NM': '서울특별시교육청', 'SD_SCHUL_CODE': '7021098', 'SCHUL_NM': '서울신내초등학교', 'ENG_SCHUL_NM': 'SEOUL SINNE ELEMENTARY SCHOOL', 'SCHUL_KND_SC_NM': '초등학교', 'LCTN_SC_NM': '서울특별시', 'JU_ORG_NM': '서울특별시동부교육지원청', 'FOND_SC_NM': '공립', 'ORG_RDNZC': '02071 ', 'ORG_RDNMA': '서울특별시 중랑구 용마산로125나길 22', 'ORG_RDNDA': '(신내동/신내초등학교)', 'ORG_TELNO': '02-2207-0501', 'HMPG_ADRES': 'http://www.sinne.es.kr', 'COEDU_SC_NM': '남여공학', 'ORG_FAXNO': '02-2207-0504', 'HS_SC_NM': None, 'INDST_SPECL_CCCCL_EXST_YN': 'N', 'HS_GNRL_BUSNS_SC_NM': '일반계', 'SPCLY_PURPS_HS_ORD_NM': None, 'ENE_BFE_SEHF_SC_NM': '전기', 'DGHT_SC_NM': '주간', 'FOND_YMD': '19940105', 'FOAS_MEMRD': '19940506', 'LOAD_DTM': '20230219'}]}]}
        '''
        
        school_name = data['schoolInfo'][1]['row'][0]['SCHUL_NM']
        # print(school_name)
        
        if not school_name:
            return Response({'message': '검색어를 찾을 수 없어요!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            serializer = self.serializer_class([{'school_name': school_name}], many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # 유저 모델에 저장
    def post(self, request):
        user = get_object_or_404(User, id=request.user.id)
        school_name = request.data.get('school_name')
        
        # 학교 이름 저장
        user.school = school_name
        user.save()

        serializer = UserInfo(user)
        return Response(serializer.data)
