from django import views
from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', include('dj_rest_auth.registration.urls')),
    # 카카오 소셜 로그인
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
    
    # 프로필 페이지
    path('<int:user_pk>/profile/', views.UserProfile.as_view(), name='user_profile'),
    
    # 팔로우
    path('<int:user_id>/follow/', views.Follow.as_view(), name='follow_user'),

    # 학교 검색
    path('search_school/', views.SearchSchool.as_view(), name='search_school'),
    
    # 닉네임 중복확인
    path('<int:user_id>/uniquecheck/nickname', views.NicknameUniqueCheck.as_view(), name='uniquecheck_nickname'),
    
    # 프로필 이미지 수정
    path('<int:user_id>/update_image/', views.ProfileImageUpdater.as_view(), name='update_image'),

    # 유저 정보 확인
    path('user_info/',views.UserViewSet.as_view({'get': 'list'})),
    
]