from django.urls import path
from .views import ArtworkImageListView, ArtworkImageDetailView

urlpatterns = [
    path('artwork/<int:pk>/images/', ArtworkImageListView.as_view(), name='artwork-images-list'),
    path('image/<int:pk>/', ArtworkImageDetailView.as_view(), name='artwork-image-detail'),
]