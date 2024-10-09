from rest_framework import serializers
from ..models import Artwork

class SimpleArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = ['title', 'artist']