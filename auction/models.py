from django.db import models
from django.utils import timezone
from django.conf import settings
from items.models import Item
# Create your models here.

def get_default_end_at():
    return timezone.now() + timezone.timedelta(days=7)

class AuctionItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE) # Item과 inventory가 작성되면 진행
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='buyer')
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField(default=get_default_end_at) # 나중에 판매 기한 설정하고 돌려주는 로직짤 때 사용

    # def is_expired(self):
    #     now = timezone.now()
    #     return now > self.end_at

    def delete(self, *args, **kwargs):
        if not self.buyer:
            seller = self.seller
            seller.inventory.add(self.item)
            seller.save()
        super().delete(*args, **kwargs)
        
    def buy(self, buyer):
        buyer.money -= self.price
        buyer.inventory.add(self.item)
        buyer.save()
        self.buyer = buyer
        self.save()
        seller = self.seller
        seller.money += int(self.price * 0.95)
        seller.save()

    def __str__(self):
        return f"{self.item} ({self.price}원, 판매자: {self.seller.username})"