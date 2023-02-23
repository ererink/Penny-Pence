from .models import GameDate, Ranking, Sector, News
from rest_framework import serializers

class GameDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameDate
        fields = '__all__'

class RankingSerializer(serializers.ModelSerializer):
    # serializer에서 보내줄 때 user의 nickname을 보내도록 설정
    user = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Ranking
        fields = ('user', 'money', 'game_date')

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = (
            'game_date',
            'sector_name',
            'content',
            'percentage',
            )

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

