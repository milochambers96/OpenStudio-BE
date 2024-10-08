from .common import ArtworkSerializer, ArtworkImageSerializer
from members.serializers.simplified import SimpleMemberSerializer

class PopulatedArtworkSerializer(ArtworkSerializer):
    artist = SimpleMemberSerializer()
    artworks_images = ArtworkImageSerializer(many=True)

