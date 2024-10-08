from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Artwork, ArtworkImage
from serializers.common import ArtworkSerializer, ArtworkImageSerializer
from .serializers.populated import PopulatedArtworkSerializer

class ArtworkListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        artworks = Artwork.objects.all()
        serialized_artworks = PopulatedArtworkSerializer(artworks, many=True)
        return Response(serialized_artworks.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data["artist"] = request.member.id
        artwork_to_add = ArtworkSerializer(data=request.data)

        try: 
            artwork_to_add.is_valid()
            artwork_to_add.save()
            image_urls = request.data.get('artworks_images', [])
            for image_url in image_urls:
                ArtworkImage.objects.create(artwork=artwork_to_add, image_url=image_url) 
            return Response(artwork_to_add, status=status.HTTP_201_CREATED)
        except Exception as err:
            print("Error")
            return Response(artwork_to_add.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)