from django import views
from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', include('dj_rest_auth.registration.urls')),
    # 카카오 소셜 로그인
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
    
    # 유저 정보 확인
    path('user_info/',views.UserViewSet.as_view({'get': 'list'})),
]
