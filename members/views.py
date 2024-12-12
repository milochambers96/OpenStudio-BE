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

            return Response({
                "message": "Registration Successful. Welcome to the studio.",
            }, status=status.HTTP_201_CREATED)
        
        error_messages = []
        for field, errors in member_to_create.errors.items():
            for error in errors:
                error_messages.append(f"{field.replace('_', ' ').capitalize()}: {error}")
        
        return Response({
            "message": "Registration failed. Please correct the following errors:",
            "errors": error_messages
        }, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        error_messages = []
        if not email:
            error_messages.append("Email: This field is required.")
        if not password:
            error_messages.append("Password: This field is required.")

        if error_messages:
            return Response({
                "message": "Login failed. Please provide all required fields.",
                "errors": error_messages
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            member_to_login = Member.objects.get(email=email)
        except Member.DoesNotExist:
            return Response({
                "message": "Login failed. Please check your credentials.",
                "errors": ["Invalid email or password."]
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not member_to_login.check_password(password):
            return Response({
                "message": "Login failed. Please check your credentials.",
                "errors": ["Invalid email or password."]
            }, status=status.HTTP_401_UNAUTHORIZED)

        dt = datetime.now() + timedelta(days=14)
        token = jwt.encode({'sub': str(member_to_login.id), 'exp': int(dt.timestamp())}, settings.SECRET_KEY, algorithm='HS256')
        print(f"Generated token: {token}")

        if member_to_login.user_type == 'collector':
            user_gallery = Gallery.objects.get(curator=member_to_login)
            return Response({
                "token": token, 
                "gallery_id": user_gallery.id,
                "message": f"Welcome back {member_to_login.first_name} {member_to_login.last_name}."
            })
        else:
            return Response({
                "token": token, 
                "message": f"Welcome back {member_to_login.first_name} {member_to_login.last_name}."
            })
            
import logging

logger = logging.getLogger(__name__)

class MemberIdView(APIView):
    def get(self, request):
        logger.info(f"Received token: {request.headers.get('Authorization')}")
        try:
            current_member = request.user
            if current_member.is_authenticated:
                member_data = MemberSerializer(current_member).data
                return Response(member_data, status=status.HTTP_200_OK)
            else:
                logger.warning("User not authenticated")
                return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            logger.error(f"Error: {error}")
            return Response(
                {"message": "There was an error, please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )