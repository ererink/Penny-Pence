from django.shortcuts import render, get_object_or_404
from .models import GameDate, Ranking, Sector, News
from .serializers import GameDateSerializer, RankingSerializer, SectorSerializer, NewsSerializer, User_PositionSerializer
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
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
    def user_ranking(self, request, pk=None):
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

# 매수 클릭
class User_PositionsViewSet(viewsets.ModelViewSet):
    queryset = User_Positions.objects.all()
    serializer_class = User_PositionSerializer

    # 주식 매수 처리를 위한 엔드포인트
    @action(detail=False, methods=['post'])
    def buy_stock(self, request):
        # 유저
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)

        position_id = request.data.get('position')
        volume = request.data.get('volume')
        if not all([user, position_id, volume]):
            return Response({'error': '필수 입력 항목을 모두 제공해주세요.'}, status=400)

        # 해당 섹터와 날짜에 대한 사용자의 기존 포지션을 가져옴
        buy_stock = User_Positions.objects.filter(user=user, position_id=position_id, day=user.days).first()
        sector = Sector.objects.get(id=position_id)
        # date = GameDate.objects.get(pk=user.days)

        # 매수 비용을 계산
        total = buy_stock.position.sector_price * volume
        
        # 총매수금액 / 매수할때 유저의 현금을 감소시켜줌
        user.money -= buy_stock.total
        user.save()
        
        # User의 현재 돈 / 프론트 출력용
        available_balance = user.money
        
        # 유저의 포지션을 끌고옴
        # 만약 사용자가 해당 섹터에 대한 포지션을 이미 가지고 있다면, 포지션을 업데이트
        if buy_stock:
            buy_stock.total += total # total은 총 매수금액
            buy_stock.volume += volume # volume은 매수주식수
            buy_stock.save()
        else:
            # 그렇지 않다면, 유저를 위한 새로운 포지션을 생성
            buy_stock = User_Positions.objects.create(user=user, position=buy_stock, day=user.days, total=total, volume=volume)
        
        # Response에 매수 메시지와 사용자의 현재 잔액을 함께 보내줌
        return Response({'success': True, 'message': f'{sector.sector_name} {volume}주를 ${total:.2f}에 매수했습니다.', 'available_balance': available_balance}, status=200)

# 자동매도 및 랭킹등록
def sell_user_position():
    User = get_user_model()

    users_positions = User_Positions.objects.all()
    
    # 매수 목록이 있는 사람들 중에서
    for user_position in users_positions:
        # 유저중에서 매수유저라면
        if User.objects.get(pk=user_position.user.pk):
            # 매수유저일자와 유저일자가 있다면
            if User.objects.get(game_date=users_positions.day):
                user_update = User.objects.get(pk=user_position.user.pk)
                # 총 매수금액에 퍼센티지 곱하기
                user_update.money += (user_position.total * user_position.position.percentage) 
                # 랭킹등록
                ranking = Ranking.objects.get(game_date=users_positions.day, user=user_update.pk)
                ranking.money = user_update.money
                ranking.save()
                # 매도하면서 유저의 데이 증가
                user_update.days += 1
                user_update.save()
            else:
                pass

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



# Create your views here.
class TestView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response("Swagger 연동 테스트")