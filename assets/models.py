from django.db import models
from django.conf import settings

# Create your models here.
class GameDate(models.Model):
    game_date = models.IntegerField()

class Ranking(models.Model):
    game_date = models.ForeignKey(GameDate, on_delete=models.CASCADE) # 일차
    money = models.IntegerField() #자산
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 닉네임 끌고오기
    
class Sector(models.Model):
    game_date = models.ForeignKey(GameDate, on_delete=models.CASCADE) # 일자
    sector_name = models.CharField(max_length=20) # title
    content = models.CharField(max_length=100) # content
    percentage = models.DecimalField(max_digits = 5, decimal_places = 2) # 주가
    sector_price = models.IntegerField(default=5000)

class News(models.Model):
    title = models.CharField(max_length=100) # 제목
    content = models.TextField() # 내용
    game_date = models.ForeignKey(GameDate, on_delete=models.CASCADE) # 일자
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE) # 종목


