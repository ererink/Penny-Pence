from django.db import models
from back.settings import AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser):
   email = models.EmailField(_('email address'), unique=True)
   nickname = models.CharField(max_length=8, blank=True)
   refresh_token = models.TextField(blank=True)
   profile_img = models.TextField(blank=True) 

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = []