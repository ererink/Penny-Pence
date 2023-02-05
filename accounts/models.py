from django.db import models
from back.settings import AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
   nickname = models.CharField(max_length=10, blank=True)
   refresh_token = models.TextField(blank=True)
   profile_img = models.TextField(blank=True) 
   