from rest_framework import serializers
from ..models import Member

class BuyerSerializer(serializers.ModelSerializer):
     class Meta:
          model = Member
          fields = ['id', 'username', 'address', 'postcode']


class SellerSerializer(serializers.ModelSerializer):
     class Meta:
          model = Member
          fields = ['id', 'username', 'address', 'postcode', 'first_name', 'last_name', 'bio' ]




