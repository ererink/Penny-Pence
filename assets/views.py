from django.shortcuts import render
from .models import GameDate, Ranking, Sector, News
from .serializers import GameDateSerializer, RankingSerializer, SectorSerializer, NewsSerializer
from rest_framework import viewsets

# Create your views here.
class GameDateViewSet(viewsets.ModelViewSet): # CRUD 기능 포함
    queryset = GameDate.objects.all() # 40일치
    serializer_class = GameDateSerializer 

class RankingViewSet(viewsets.ModelViewSet):
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer