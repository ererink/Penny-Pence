from django.shortcuts import render, get_object_or_404
from .models import GameDate, Ranking, Sector, News
from django.db.models import Sum
from .serializers import GameDateSerializer, RankingSerializer, SectorSerializer, NewsSerializer
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .sector_percentage import *

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
class RankingViewSet(viewsets.ViewSet):
    # 인증된 사용자만 접근 가능하도록
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def get_ranking_by_game_date(self, request, pk=None):
        # game_date_id 에 해당하는 게임 날짜 데이터를 가져옴
        game_date = get_object_or_404(GameDate, pk=pk)
        ranking_user = request.user

        # 이미 DB에 user가 저장되어 있다면 리스트 출력
        if Ranking.objects.filter(user_id=ranking_user.pk) and Ranking.objects.filter(game_date=game_date):
            rankings = Ranking.objects.filter(game_date=game_date).order_by('money')
        
        else:
            rankings = Ranking.objects.create(
                game_date = game_date,
                money = ranking_user.money,
                user_id = ranking_user.pk
                ).save()
        
        # Serializer를 통해 데이터 직렬화
        serializer = RankingSerializer(rankings, many=True)
        # Response를 통해 직렬화된 데이터 반환
        return Response(serializer.data)

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