from rest_framework import serializers
from ..models import Member

class SimpleMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'username']