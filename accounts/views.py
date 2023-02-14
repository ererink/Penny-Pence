from django.shortcuts import render, redirect
import os
import requests
from json.decoder import JSONDecodeError
from accounts.models import User

# Create your views here.
BASE_URL = 'https://pennypence-backend.shop/'
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback/'


# 카카오 로그인
def kakao_login(request):
    rest_api_key = os.getenv("KAKAO_REST_API_KEY")
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )

def kakao_callback(request):
    rest_api_key = os.getenv("KAKAO_REST_API_KEY")
    code = request.GET.get("code")
    redirect_uri = "https://master.d3n2xysrd0lvj9.amplifyapp.com/oauth/callback/kakao"
    
    # Access Token Request
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    
    if error is not None:
        raise JSONDecodeError(error)
    
    access_token = token_req_json.get("access_token")

    # Email Request
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    profile_json = profile_request.json()
    kakao_account = profile_json.get('kakao_account')
    
    email = kakao_account.get('email')

    user = User.objects.get(email=email)
