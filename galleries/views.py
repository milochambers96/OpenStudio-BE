from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Gallery, GalleryArtwork
from artworks.models import Artwork

from .serializers.common import GalleryArtworkSerializer, GallerySerializer

class GalleriesListView(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, _request):
        try: 
            galleries = Gallery.objects.all()
            serialized_galleries = GallerySerializer(galleries)
            return Response(serialized_galleries.data, status=status.HTTP_200_OK)
        except Gallery.DoesNotExist:
            raise PermissionDenied()

class UserGalleryView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            user_gallery = Gallery.objects.get(curator = request.user)
            serialized_gallery = GallerySerializer(user_gallery)
            return Response(serialized_gallery.data, status=status.HTTP_200_OK)
        except Gallery.DoesNotExist:
            raise NotFound(detail="Gallery not found for this user.")

def get_gallery(pk, curator):
        try: 
            return Gallery.objects.get(pk=pk, curator=curator)
        except Gallery.DoesNotExist: 
            raise NotFound(detail="Gallery not found or you do not have permission to access it.")

class GalleryArtworkListView(APIView):
    permission_classes = (IsAuthenticated, )
        
    def get(self, request, pk):
        
        user_gallery= get_gallery(pk=pk, curator=request.user)
        gallery_artworks = GalleryArtwork.objects.filter(gallery=user_gallery)
        serialized_artworks = GalleryArtworkSerializer(gallery_artworks, many=True)
        return Response(serialized_artworks.data, status=status.HTTP_200_OK)
    
class GalleryArtworkManagerView(APIView):  
    permission_classes = (IsAuthenticated,)

    def get_gallery(self, gallery_pk, curator): 
        try:
            return Gallery.objects.get(pk=gallery_pk, curator=curator)
        except Gallery.DoesNotExist:
            raise NotFound(detail="Gallery not found or you do not have permission to access it.")

    def post(self, request, gallery_pk):  
        user_gallery = self.get_gallery(gallery_pk, curator=request.user) 
        artwork_id = request.data.get('artwork')
        
        try: 
            artwork = Artwork.objects.get(pk=artwork_id)
        except Artwork.DoesNotExist:
            raise NotFound(detail="Artwork not found.")
        
        gallery_artwork, created = GalleryArtwork.objects.get_or_create(gallery=user_gallery, artwork=artwork)
        if created:
            return Response({"message": "Artwork added to the gallery!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Artwork is already in the gallery."}, status=status.HTTP_200_OK)

    def delete(self, request, gallery_pk):  
        user_gallery = self.get_gallery(gallery_pk, curator=request.user)  
        artwork_id = request.data.get('artwork')

        try: 
            artwork = Artwork.objects.get(pk=artwork_id)
        except Artwork.DoesNotExist:
            raise NotFound(detail="Artwork not found.")
        
        try:
            gallery_artwork = GalleryArtwork.objects.get(gallery=user_gallery, artwork=artwork)
            gallery_artwork.delete()
            return Response({"message": "Artwork removed from the gallery."}, status=status.HTTP_204_NO_CONTENT)
        except GalleryArtwork.DoesNotExist:
            raise NotFound(detail="This artwork is not in your gallery.")
