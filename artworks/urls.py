from django.urls import path
from .views import ArtworkListView, ArtworkDetailView


urlpatterns = [
    path('', ArtworkListView.as_view(), name='artwork-list'),
    path('<int:pk>/', ArtworkDetailView.as_view(), name='artwork-detail'),
]

