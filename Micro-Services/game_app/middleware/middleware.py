import jwt
from django.http import JsonResponse
from game_app import settings
import logging

logger = logging.getLogger(__name__)

def jwt_decode(token):
    logger.info("hello")
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info("Middleware called")
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if authorization_header:
            try:
                prefix, token = authorization_header.split(' ')
                if prefix.lower() != 'bearer':
                    raise ValueError('Invalid token prefix')
                
                payload = jwt_decode(token)
                request.user_id = payload.get('user_id')
            except jwt.ExpiredSignatureError:
                logger.error(f"Unexpected error: 1")
                return JsonResponse({'error': 'Token has expired'}, status=401)
            except jwt.InvalidTokenError:
                logger.error(token)
                logger.error(f"Unexpected error: 2")
                return JsonResponse({'error': 'Invalid token2'}, status=401)
            except ValueError as e:
                logger.error(f"Unexpected error: 3")
                return JsonResponse({'error': str(e)}, status=401)

        response = self.get_response(request)
        return response
