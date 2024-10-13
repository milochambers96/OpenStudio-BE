from django.urls import path
from .views import ArtworkListView, ArtworkDetailView, ArtworkCreateView


urlpatterns = [
    path('', ArtworkListView.as_view(), name='artwork-list'),
    path('<int:pk>/', ArtworkDetailView.as_view(), name='artwork-detail'),
    path('create/', ArtworkCreateView.as_view(), name='artwork-create'),


]

