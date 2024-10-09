from .common import ArtworkSerializer
from members.serializers.simplified import SimpleMemberSerializer
from artwork_images.serializers.common import ArtworkImageSerializer

class PopulatedArtworkSerializer(ArtworkSerializer):
    artist = SimpleMemberSerializer()
    artworks_images = ArtworkImageSerializer(many=True)

