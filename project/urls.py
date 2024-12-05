from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/members/', include('members.urls')),
    path('api/artworks/', include('artworks.urls')),
    path('api/images/', include('artwork_images.urls')),
    path('api/galleries/', include('galleries.urls')),
    path('api/orders/', include('orders.urls'))
]
