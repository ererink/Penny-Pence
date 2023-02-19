from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import AuctionItem
from .serializers import AuctionItemSerializer

class AuctionItemViewSet(viewsets.ModelViewSet):
    serializer_class = AuctionItemSerializer
    
    def get_queryset(self):
        queryset = AuctionItem.objects.all()
        item_id = self.request.query_params.get('item_id', None)
        if item_id:
            queryset = queryset.filter(item_id=item_id)
        queryset = queryset.order_by('price')
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.buyer or instance.is_expired():
            return Response({'detail': 'This auction item is no longer available.'}, status=status.HTTP_400_BAD_REQUEST)
        if instance.seller == request.user:
            return Response({'detail': 'You cannot buy your own auction item.'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.money < instance.price:
            return Response({'detail': 'You do not have enough money.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.buy(request.user)
        return Response({'detail': 'Auction item has been purchased.'}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.buyer:
            return Response({'detail': 'This auction item has already been sold.'}, status=status.HTTP_400_BAD_REQUEST)
        if instance.seller != request.user:
            return Response({'detail': 'You cannot delete this auction item.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response({'detail': 'Auction item has been deleted.'}, status=status.HTTP_204_NO_CONTENT)