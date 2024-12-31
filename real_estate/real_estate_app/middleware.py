import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        exempt_urls = [
            '/login/',
            '/swagger/',
            '/swagger/swagger-ui-bundle.js',
            '/swagger/swagger-ui.css',
            '/swagger/swagger-ui-standalone-preset.js',
            '/swagger/schema.json',
            '/redoc/',
            '/static/',
        ]

        if any(request.path.startswith(url) for url in exempt_urls):
            return self.get_response(request)

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({
                "error": {
                    "code": 401,
                    "message": "Вы должны авторизоваться."
                }
            }, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = auth_header.replace("Bearer", "").strip()

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload.get('user_id')
        except (jwt.InvalidTokenError, IndexError):
            return JsonResponse({
                "error": {
                    "code": 401,
                    "message": f"Недействительный токен."
                }
            }, status=status.HTTP_401_UNAUTHORIZED)

        return self.get_response(request)
