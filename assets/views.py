from django.shortcuts import render
from .models import GameDate, Ranking, Sector, News
from .serializers import GameDateSerializer, RankingSerializer, SectorSerializer, NewsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
      
# Create your views here.
# class GameDateViewSet(viewsets.ModelViewSet): # CRUD 기능 포함
#     queryset = GameDate.objects.all() # 40일치
#     serializer_class = GameDateSerializer 

@api_view(['POST'])
def date_create(request):
    create_date = request.data
    serializer = GameDateSerializer(data=create_date)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RankingViewSet(viewsets.ModelViewSet):
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer

@api_view(['POST'])
def sector(request):
    sector_data = request.data
    serializer = SectorSerializer(data=sector_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# def create_news(request):
#     serializer = NewsSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

