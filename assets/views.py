from django.shortcuts import render, get_object_or_404
from .models import GameDate, Ranking, Sector, News
from .serializers import GameDateSerializer, RankingSerializer, SectorSerializer, NewsSerializer
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .sector_percentage import *

# accounts 앱
from django.contrib.auth import get_user_model
from accounts.models import User_Positions

# 스케줄러
import schedule
import time

# 게임일자
class GameDateViewSet(viewsets.ModelViewSet): # CRUD 기능 포함
    queryset = GameDate.objects.all() # 40일치
    serializer_class = GameDateSerializer 

## 게임 날짜 DB삽입용 함수
def date_create(request):
    for i in range(1,41):
        GameDate.objects.create(
            game_date = i
        ).save()

# 랭킹 리스트 출력
class RankingViewSet(viewsets.ViewSet):
    # 인증된 사용자만 접근 가능하도록
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def get_ranking_by_game_date(self, request, pk=None):
        # game_date_id 에 해당하는 게임 날짜 데이터를 가져옴
        game_date = get_object_or_404(GameDate, pk=pk)
        ranking_user = request.user

        # 해당 유저의 랭킹 데이터 가져오기
        user_ranking = Ranking.objects.filter(game_date=game_date, user=ranking_user).first()
        user_serializer = RankingSerializer(user_ranking) if user_ranking else None

        # 상위 5명의 랭킹 데이터 가져오기
        rankings = Ranking.objects.filter(game_date=game_date).order_by('-money')[:5]
        ranking_serializer = RankingSerializer(rankings, many=True)

        # Response를 통해 직렬화된 데이터 반환
        data = {
            'user_ranking': user_serializer.data,
            'ranking': ranking_serializer.data,
        }

        return Response(data)

# 자동 랭킹등록
def update_ranking():
    User = get_user_model()
    for user in User.objects.all():
        money = user.money
        # user 필드명이랑 일치시킬 것, 
        # 자동 매도 후 유저의 하루 이전 게임일자에 저장하도록 변경해야 함
        game_date = user.game_date 
        ranking = Ranking.objects.get(game_date=game_date, user=user)
        ranking.money = money
        ranking.save()

# 자동매도
def sell_user_position():
    User = get_user_model()
    users = User.objects.all()

    users_positions = User_Positions.objects.all()
    
    # 매수 목록이 있는 사람들 중에서
    for user_position in users_positions:
        # 매수 유저와 유저가 일치하고
        if User.objects.get(pk=user_position.pk):
            # 매수유저일자와 유저일자가 있다면
            if User.objects.get(game_date=users_positions.day):
                user_update = User.objects.get(pk=user_position.pk)
                user_update.money *= user_position.position.percentage # 퍼센티지
                # 유저의 데이 테이블도 += 1
                user_update.save()
        else:
            print("error")

# 오전 5시55분에 자동매도 실행
# schedule.every(1).day.at('05:55').do(sell_user_position)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
#     break

# # 오전 6시에 자동 랭킹등록
# schedule.every(1).day.at("06:00").do(update_ranking)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
#     break

# 산업
@api_view(['POST'])
def sector(request):
    sector_data = request.data
    serializer = SectorSerializer(data=sector_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## 산업 정보 및 주가 DB삽입용 함수
def save_sector(request):
    day_percentage = automobile_sector()
    
    for i in range(1, 41):
        day = GameDate.objects.get(game_date=i)
        percentage = day_percentage.popleft()
        print(percentage)
        Sector.objects.create(
            game_date = day,
            sector_name = "자동차",
            content = "자동차 산업",
            percentage = percentage
        ).save()

# 뉴스
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    # 뉴스 리스트
    def list(self, request, *args, **kwargs):
        game_date = request.query_params.get('game_date')
        queryset = self.filter_queryset(self.get_queryset())

        if game_date is not None:
            queryset = queryset.filter(game_date=game_date)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    # detail 페이지
    def retrieve(self, request, pk=None):
        queryset = News.objects.all()
        news = get_object_or_404(queryset, pk=pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

# 직접입력 test 코드
@api_view(['POST'])
def create_news(request):
    serializer = NewsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## 뉴스 DB 저장
# def input_news():
    
#     for i in range(1, 41):
#         day = GameDate.objects.get(game_date=i)
#         sector = Sector.objects.get(sector_name="IT")
#         News.objects.create(
#             title = title,
#             content = content,
#             game_date = day,
#             sector = sector,
#         )