from django.shortcuts import render
from .models import GameDate, Ranking, Sector, News
from .serializers import GameDateSerializer, RankingSerializer, SectorSerializer, NewsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .sector_percentage import *
from collections import deque
# Create your views here.

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


# 랭킹
class RankingViewSet(viewsets.ModelViewSet):
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer


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

    def list(self, request, *args, **kwargs):
        game_date = request.query_params.get('game_date')
        queryset = self.filter_queryset(self.get_queryset())

        if game_date is not None:
            queryset = queryset.filter(game_date=game_date)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_news(request):
    serializer = NewsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## 뉴스 DB 저장