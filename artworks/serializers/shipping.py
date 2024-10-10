from rest_framework import serializers
from ..models import Artwork

class ArtworkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = [ 'id', 'title', 'width', 'depth', 'height', 'weight']



    