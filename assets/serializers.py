from .models import GameDate, Ranking, Sector, News
from rest_framework import serializers

class GameDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameDate
        fields = '__all__'

class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranking
        fields = '__all__'

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = (
            'game_date',
            'sector_name',
            'content',
            'price',
            )

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

