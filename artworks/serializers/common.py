from rest_framework import serializers
from ..models import Artwork, ArtworkImage

class ArtworkSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Artwork
        fields = '__all__'


class ArtworkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkImage
        fields = ['id', 'image']

