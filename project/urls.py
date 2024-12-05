from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def root_route(request):
    return JsonResponse({
        "message": "Welcome to OpenStudio API",
        "endpoints": {
            "members": "/api/members/",
            "artworks": "/api/artworks/",
            "images": "/api/images/",
            "galleries": "/api/galleries/",
            "orders": "/api/orders/"
        }
    })

urlpatterns = [
    path('', root_route), 
    path('api/admin/', admin.site.urls),
    path('api/members/', include('members.urls')),
    path('api/artworks/', include('artworks.urls')),
    path('api/images/', include('artwork_images.urls')),
    path('api/galleries/', include('galleries.urls')),
    path('api/orders/', include('orders.urls'))
]
