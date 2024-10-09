from rest_framework import serializers
from ..models import ArtworkImage
from artworks.serializers.simplified import SimpleArtworkSerializer

class ArtworkImageSerializer(serializers.ModelSerializer):
    artwork = SimpleArtworkSerializer()
    class Meta:
        model = ArtworkImage
        fields = ['id', 'image_url', 'artwork']
        