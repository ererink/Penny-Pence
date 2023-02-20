from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import AuctionItem
from .serializers import AuctionItemSerializer
from rest_framework.exceptions import ValidationError

class AuctionItemViewSet(viewsets.ModelViewSet):
    serializer_class = AuctionItemSerializer
    
    def get_queryset(self):
        queryset = AuctionItem.objects.all()
        item_id = self.request.query_params.get('item_id', None)
        if item_id:
            queryset = queryset.filter(item_id=item_id, buyer=None)
        queryset = queryset.order_by('price')
        return queryset
    
    def create(self, request, *args, **kwargs):
        seller = request.user
        item_id = request.data.get('item')
        if not seller.inventory.filter(pk=item_id).exists():
            raise ValidationError("Seller inventory does not contain the specified item")
        seller.inventory.remove(item_id)
        seller.save()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # if instance.buyer or instance.is_expired(): # 나중에 판매기한을 설정하고 돌려주는 로직을 짤 때 사용
        if instance.buyer:
            return Response({'detail': 'This auction item has already been sold.'}, status=status.HTTP_400_BAD_REQUEST)
        if instance.seller == request.user:
            return Response({'detail': 'You cannot buy your own auction item.'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.money < instance.price:
            return Response({'detail': 'You do not have enough money.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.buy(request.user)
        return Response({'detail': 'Auction item has been purchased.'}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.seller != request.user:
            return Response({'detail': 'You cannot delete this auction item.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response({'detail': 'Auction item has been deleted.'}, status=status.HTTP_204_NO_CONTENT)