import jwt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from ..models import Users
from ..serializers import LoginSerializer


@swagger_auto_schema(
    method='POST',
    request_body=LoginSerializer,
    responses={
        204: 'Flats updated successfully',
        401: 'Unauthorized',
        422: 'Invalid data',
    },
)
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    try:
        user = Users.objects.get(
            login=serializer.validated_data['login'],
            password=serializer.validated_data['password']
        )
    except Users.DoesNotExist:
        return Response({
            "error": {
                "code": 401,
                "message": "Unauthorized",
                "errors": {
                    "login": ["Login or password incorrect."]
                }
            }
        }, status=status.HTTP_401_UNAUTHORIZED)

    token = jwt.encode(
        {
            'user_id': user.id,
            'login': user.login
        },
        settings.SECRET_KEY,
        algorithm='HS256'
    )

    return Response({
        "data": {
            "token": token
        }
    })