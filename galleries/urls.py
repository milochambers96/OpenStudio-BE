from django.urls import path
from .views import GalleriesListView, UserGalleryView, GalleryArtworkListView, GalleryArtworkManagerView

urlpatterns = [
    path('all/', GalleriesListView.as_view(), name='admin-galleries-list-view'),
    
    path('my-gallery/', UserGalleryView.as_view(), name='user-gallery-view'),  
    path('<int:pk>/artworks/', GalleryArtworkListView.as_view(), name='gallery-artwork-list'),
    path('<int:gallery_pk>/curate/', GalleryArtworkManagerView.as_view(), name='gallery-artwork-manager'),  # Updated for consistency and removed artwork_pk
]

