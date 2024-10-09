from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import ArtworkImage
from artworks.models import Artwork
from .serializers.common import ArtworkImageSerializer


class ArtworkImageListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_artwork(self, pk):
        try:
            return Artwork.objects.get(pk=pk)
        except Artwork.DoesNotExist:
            raise NotFound(detail="Artwork not found.")
    
    def get(self, request, pk):
        artwork = self.get_artwork(pk=pk)
        images = ArtworkImage.objects.filter(artwork=artwork)
        serialized_images = ArtworkImageSerializer(images, many=True)
        return Response(serialized_images.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        artwork = self.get_artwork(pk=pk)
        image_url = request.data.get('image_url')

        if not image_url:
            return Response ({"detail": "Image URL is requried. Please uplaod again."}, status=status.HTTP_400_BAD_REQUEST)

        new_image = ArtworkImage.objects.create(artwork=artwork, image_url=image_url)
        serialized_image = ArtworkImageSerializer(new_image)
        return Response (serialized_image.data, status=status.HTTP_201_CREATED)

class ArtworkImageDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_image(self, pk):
        try:
            return ArtworkImage.objects.get(pk=pk)
        except ArtworkImage.DoesNotExist:
            raise NotFound(detail="Image not found.")

    def delete(self, request, pk):
        image_to_delete = self.get_image(pk=pk)
        image_to_delete.delete()
        return Response({"message": "Image successfully removed."}, status=status.HTTP_204_NO_CONTENT)
