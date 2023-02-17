# from django.db import models
# from django.utils import timezone
# from django.conf import settings
# # Create your models here.

# class AuctionItem(models.Model):
#     item = models.ForeignKey(Item, on_delete=models.CASCADE) # Item과 inventory가 작성되면 진행
#     seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
#     price = models.PositiveIntegerField()
#     created_at = models.DateTimeField(default=timezone.now)
#     end_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=7))

#     def is_expired(self):
#         now = timezone.now()
#         return now > self.end_at
    
#     def create(self, *args, **kwargs):
#         seller_inventory = self.seller.inventory
#         seller_inventory.items.remove(self.item)
#         seller_inventory.save()
#         super().save(*args, **kwargs)
    
#     def delete(self, *args, **kwargs):
#         if not self.buyer and self.end_at < timezone.now():
#             seller_inventory = self.seller.inventory
#             seller_inventory.items.add(self.item)
#             seller_inventory.save()
#         super().delete(*args, **kwargs)

#     def buy(self, buyer):
#         if self.is_expired():
#             raise ValueError("Auction item has already expired")
#         if buyer == self.seller:
#             raise ValueError("You cannot buy your own auction item")
        
#         if buyer.money >= self.price:
#             buyer.money -= self.price
#             buyer.inventory.items.add(self.item)
#             buyer.inventory.save()
#             self.buyer = buyer
#             self.save()
#             seller = self.seller
#             seller.money += int(self.price * 0.95)
#             seller.save()
#             return True
#         else:
#             return False
#     def __str__(self):
#         return f"{self.item} ({self.price}원, 판매자: {self.seller.username})"