from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Artwork
from artwork_images.models import ArtworkImage
from .serializers.common import ArtworkSerializer
# from artwork_images.serializers.common import ArtworkImageSerializer
from .serializers.populated import PopulatedArtworkSerializer

class ArtworkListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        artworks = Artwork.objects.all()
        serialized_artworks = PopulatedArtworkSerializer(artworks, many=True)
        return Response(serialized_artworks.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["artist"] = request.user.id
        artwork_to_add = ArtworkSerializer(data=request.data)

        try:
            if artwork_to_add.is_valid():
                artwork_instance = artwork_to_add.save()
                image_urls = request.data.get('artwork_images', [])
                
                # Create associated artwork images
                for image_url in image_urls:
                    ArtworkImage.objects.create(artwork=artwork_instance, image_url=image_url)
                
                return Response(PopulatedArtworkSerializer(artwork_instance).data, status=status.HTTP_201_CREATED)
            return Response(artwork_to_add.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as err:
            print("Error:", err)
            return Response({"detail": "An error occurred while creating the artwork."}, status=status.HTTP_400_BAD_REQUEST)


class ArtworkDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_artwork(self, pk):
        try:
            return Artwork.objects.get(pk=pk)
        except Artwork.DoesNotExist:
            raise NotFound(detail='Artwork not found.')

    def get(self, _request, pk):
        artwork = self.get_artwork(pk=pk)
        serialized_artwork = PopulatedArtworkSerializer(artwork)
        return Response(serialized_artwork.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        artwork_to_update = self.get_artwork(pk=pk)
        updated_artwork = ArtworkSerializer(artwork_to_update, data=request.data, partial=True)

        if updated_artwork.is_valid():
            updated_artwork_instance = updated_artwork.save()

            image_urls = request.data.get('artwork_images', [])  
            if image_urls:
                artwork_to_update.artworks_images.all().delete()
                for image_url in image_urls:
                    ArtworkImage.objects.create(artwork=updated_artwork_instance, image_url=image_url)
            return Response(PopulatedArtworkSerializer(updated_artwork_instance).data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_artwork.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, _request, pk):
        artwork_to_delete = self.get_artwork(pk=pk)

        artwork_to_delete.artworks_images.all().delete() 
        artwork_to_delete.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
