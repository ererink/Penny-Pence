from django.db import models
# from back.settings import AUTH_USER_MODEL

# Create your models here.
class GameDate(models.Model):
    game_date = models.IntegerField()

class Ranking(models.Model):
    game_date = models.ForeignKey(GameDate, on_delete=models.CASCADE) # 일차
    money = models.IntegerField() #자산
    # user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE) # 닉네임 끌고오기
    
class Sector(models.Model):
    sector_name = models.CharField(max_length=20) # title
    content = models.CharField(max_length=100) # content
    price = models.IntegerField() # 주가

class News(models.Model):
    title = models.CharField(max_length=100) # 제목
    content = models.TextField() # 내용
    game_date = models.ForeignKey(GameDate, on_delete=models.CASCADE) # 일자
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE) # 종목


