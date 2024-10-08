from django.urls import path
from .views import RegisterView, LoginView, MemberIdView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', MemberIdView.as_view(), name='member-details')
]



