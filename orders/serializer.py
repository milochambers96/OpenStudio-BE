from rest_framework import serializers
from .models import Order
from members.models import Member
from artworks.models import Artwork
from members.serializers.shipping import BuyerSerializer, SellerSerializer
from artworks.serializers.shipping import ArtworkOrderSerializer

class OrderSerializer(serializers.ModelSerializer):
    buyer = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), write_only=True)
    seller = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), write_only=True)
    artwork = serializers.PrimaryKeyRelatedField(queryset=Artwork.objects.all(), write_only=True)

    buyer_info = BuyerSerializer(source='buyer', read_only=True)
    seller_info = SellerSerializer(source='seller', read_only=True)
    artwork_info = ArtworkOrderSerializer(source='artwork', read_only=True)

    class Meta: 
        model = Order
        fields = '__all__'


    
