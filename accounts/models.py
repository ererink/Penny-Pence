from django.db import models
from back.settings import AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from items.models import Item
# from assets.models import GameDate, Sector, News
from assets.models import News
from .managers import CustomUserManager
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

class User(AbstractUser):
    # 기본정보
    email = models.EmailField(_('email address'), unique=True)
    nickname = models.CharField(max_length=8, blank=True)
    refresh_token = models.TextField(blank=True)
    profile_img = models.TextField(blank=True)                           # 카카오에서 받은 프로필 이미지 (URL) 
    edited_img = ProcessedImageField(upload_to='images/', blank=True,
                                 processors=[ResizeToFill(1200, 960)],
                                 format='JPEG',
                                 options={'quality': 80},
                                 null=True)                              # 수정한 프로필 이미지 (JPEG) 
    username = None

    # 부가정보
    money = models.IntegerField(default=100000, blank=True)                       # 자산 (임시로 blank=True 해놓음)
    school = models.CharField(max_length=10, blank=True)
    # sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    # 매수목록
    position = models.ManyToManyField('assets.Sector', through='User_Positions')
    # 아이템 
    inventory = models.ManyToManyField(Item, through='User_Items')
    # 뉴스 
    read_news = models.ManyToManyField('assets.News', through='User_News')
    # 일차
    days = models.ForeignKey('assets.GameDate', on_delete=models.CASCADE, default=1)
    # 기능
    followers = models.ManyToManyField('self', symmetrical=True, related_name='following')    # Ture: 양방향 관계, 일촌 개념
    following = models.ManyToManyField('self', symmetrical=True, related_name='following')    # symmetrical=True로 설정했기 때문에 following 필드가 자동으로 생성되지 않음


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# 매수목록 ManyToManyField 확장
class User_Positions(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   position = models.ForeignKey('assets.Sector', on_delete=models.CASCADE)
   day = models.ForeignKey('assets.GameDate', on_delete=models.CASCADE)
   total = models.IntegerField(default=0)       # 총 매수 금액
   volume = models.IntegerField(default=0)      # 매수수량

# 아이템목록(inventory) ManyToManyField 확장
class User_Items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

# 뉴스 읽음 여부 ManyToManyField 확장
class User_News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey('assets.News', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
