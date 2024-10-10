from rest_framework import serializers
from ..models import Gallery, GalleryArtwork
from artworks.serializers.populated import PopulatedArtworkSerializer
from artworks.serializers.simplified import SimpleArtworkSerializer

class GalleryArtworkSerializer(serializers.ModelSerializer):
    artwork = PopulatedArtworkSerializer()

    class Meta:
        model = GalleryArtwork
        fields = ['gallery', 'artwork']

class GallerySerializer(serializers.ModelSerializer):
    artworks = PopulatedArtworkSerializer(many=True, read_only=True)

    class Meta: 
        model = Gallery
        fields = ['id', 'curator', 'artworks']






