from rest_framework import serializers
from ..models import Member

class BuyerSerializer(serializers.ModelSerializer):
     class Meta:
          model = Member
          fields = ['id', 'username', 'collector_address', 'email']


class SellerSerializer(serializers.ModelSerializer):
     class Meta:
          model = Member
          fields = ['id', 'username', 'artist_address', 'email']




