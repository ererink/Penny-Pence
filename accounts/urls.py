from django.urls import path
from . import views
from django import views

app_name = "accounts"

urlpatterns = [
    # 카카오 소셜 로그인
    path("login/kakao", views.kakao_login, name="kakao_login"),
    path("kakao/callback", views.kakao_callback, name="kakao_callback"),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
]
