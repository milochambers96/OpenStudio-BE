from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers.common import MemberSerializer
from galleries.models import Gallery
import jwt

Member = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        member_to_create = MemberSerializer(data=request.data)

        if member_to_create.is_valid():
            new_member_instance = member_to_create.save()
            if new_member_instance.user_type == 'collector': 
                Gallery.objects.create(curator=new_member_instance)

            return Response({"message": "Registration Successful. Welcome to the studio."}, status=status.HTTP_201_CREATED)
        
        return Response(member_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            member_to_login = Member.objects.get(email=email)
        except Member.DoesNotExist:
            raise PermissionDenied(detail="Invalid Credentials")
        if not member_to_login.check_password(password):
            raise PermissionDenied(detail="Invalid Credentials")
        
        if member_to_login.user_type == 'collector':
            user_gallery = Gallery.objects.get(curator=member_to_login)

        dt = datetime.now() + timedelta(days=14)
        token = jwt.encode({'sub': member_to_login.id, 'exp': int(dt.timestamp())}, settings.SECRET_KEY, algorithm='HS256')
        if member_to_login.user_type == 'collector':
            return Response ({
                "token": token, 
                "gallery_id": user_gallery.id,
                "message": f"Welcome back {member_to_login.first_name} {member_to_login.last_name}."
                })
        else:
            return Response ({
                "token": token, 
                "message": f"Welcome back {member_to_login.first_name} {member_to_login.last_name}."
        })

class MemberIdView(APIView):
    
    def get(self, request): 
        try:
            current_member = request.user
            if current_member.is_authenticated:
                member_data = MemberSerializer(current_member).data
                return Response(member_data, status=status.HTTP_200_OK)
            else: 
                return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            print(error)
            return Response(
                {"message": "There was an error, please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        