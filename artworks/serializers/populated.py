from .common import ArtworkSerializer
from members.serializers.simplified import SimpleMemberSerializer
from members.serializers.shipping import SellerSerializer

from artwork_images.serializers.common import ArtworkImageSerializer


class PopulatedArtworkSerializer(ArtworkSerializer):
    artist = SellerSerializer()
    artworks_images = ArtworkImageSerializer(many=True, read_only=True)

