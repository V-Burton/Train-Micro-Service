import jwt
from django.http import JsonResponse
from game_app import settings

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if authorization_header:
            try:
                prefix, token = authorization_header.split(' ')
                if prefix.lower() != 'bearer':
                    raise ValueError('Invalid token prefix')
                
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                request.user_id = payload.get('user_id')
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token2'}, status=401)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=401)

        return self.get_response(request)
    def get_token(request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if authorization_header:
            try:
                prefix, token = authorization_header.split(' ')
                if prefix.lower() == 'bearer':
                    return token
                
            except ValueError:
                pass
        return request.GET.get('token')