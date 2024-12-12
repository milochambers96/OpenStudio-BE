import logging
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt 

Member = get_user_model()
logger = logging.getLogger(__name__)

class JWTAuthentication(BasicAuthentication):

    def authenticate(self, request):
        logger.debug("Starting JWT authentication process")
        header = request.headers.get("Authorization")

        if not header: 
            logger.debug("No Authorization header found")
            return None
        
        if not header.startswith("Bearer"):
            logger.warning("Authorization header does not start with 'Bearer'")
            raise PermissionDenied(detail="Invalid authorisation token")
        
        token = header.replace("Bearer ", "")
        logger.debug(f"Token extracted: {token[:10]}...") 

        try:
            logger.debug("Attempting to decode token")
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            logger.debug(f"Token decoded successfully. Payload: {payload}")

            member = Member.objects.get(pk=int(payload.get('sub')))
            logger.debug(f"Member found: {member.id}")

        except jwt.exceptions.ExpiredSignatureError:
            logger.warning("Token has expired")
            raise PermissionDenied(detail="Token has expired")

        except jwt.exceptions.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            raise PermissionDenied(detail="Invalid authorisation token")
        
        except Member.DoesNotExist:
            logger.warning(f"Member not found for sub: {payload.get('sub')}")
            raise PermissionDenied(detail="Member not found")
        
        logger.debug("Authentication successful")
        return (member, token)