from django.shortcuts import render
from .models import GameDate, Ranking, Sector, News
from .serializers import GameDateSerializer, RankingSerializer, SectorSerializer, NewsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .sector_percentage import it_sector
from collections import deque
# Create your views here.

# 게임일자
class GameDateViewSet(viewsets.ModelViewSet): # CRUD 기능 포함
    queryset = GameDate.objects.all() # 40일치
    serializer_class = GameDateSerializer 

@api_view(['POST'])
def date_create(request):
    create_date = request.data
    serializer = GameDateSerializer(data=create_date)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

# def save_sector(request):
#     day_percentage = it_sector()
    
#     for i in range(1, 40):
#         day = GameDate.objects.get(id=i)
#         percentage = day_percentage.popleft()
#         sector = Sector.objects.create(
#             game_date = day,
#             sector_name = "IT",
#             content = "IT산업",
#             percentage = percentage
#         )
#         sector.save()
# save_sector()


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

# @api_view(['POST'])
# def create_news(request):
#     serializer = NewsSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
