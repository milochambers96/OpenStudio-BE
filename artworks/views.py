from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
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

        if artwork_to_update.artist.id != request.user.id:
            raise PermissionDenied(detail="You don't have permission to edit this artwork.")
        
        artwork_images = request.data.pop('artworks_images', [])
        
        updated_artwork = ArtworkSerializer(artwork_to_update, data=request.data, partial=True)

        if updated_artwork.is_valid():
            updated_artwork_instance = updated_artwork.save()

            if artwork_images:
                artwork_to_update.artworks_images.all().delete()
                
                for image_url in artwork_images:
                    ArtworkImage.objects.create(artwork=updated_artwork_instance, image_url=image_url)

            return Response(PopulatedArtworkSerializer(updated_artwork_instance).data, status=status.HTTP_202_ACCEPTED)
        
        return Response(updated_artwork.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        try:
            artwork_to_delete = self.get_artwork(pk=pk)

            if artwork_to_delete.artist.id != request.user.id:
                raise PermissionDenied(detail="You don't have permission to delete this artwork.")

            artwork_to_delete.artworks_images.all().delete() 
            artwork_to_delete.delete()

            return Response({"detail": "Artwork successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"detail": "An error occurred while deleting the artwork."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class ArtworkCreateView(APIView):
    def post(self, request):
        request.data["artist"] = request.user.id
        artwork_to_add = ArtworkSerializer(data=request.data)

        try:
            if artwork_to_add.is_valid():
                artwork_instance = artwork_to_add.save()
                image_urls = request.data.get('artworks_images', [])
                
                
                for image_url in image_urls:
                    ArtworkImage.objects.create(artwork=artwork_instance, image_url=image_url)
                
                updated_artwork = PopulatedArtworkSerializer(artwork_instance).data
                
                return Response(updated_artwork, status=status.HTTP_201_CREATED)
            else:
                return Response(artwork_to_add.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"detail": f"An error occurred while creating the artwork: {str(err)}"}, status=status.HTTP_400_BAD_REQUEST)
        
