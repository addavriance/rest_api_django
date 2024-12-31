from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.http import Http404

from rest_framework.views import exception_handler
from rest_framework.serializers import ValidationError as DRFValidationError

from .exceptions import NotFoundError, ValidationError


def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = NotFoundError()
    elif isinstance(exc, DRFValidationError):
        exc = ValidationError(exc.detail)

    return exception_handler(exc, context)


def in_range(x: int, r: tuple[int | float, int | float]) -> bool:
    return r[0] <= x <= r[1]


def generate_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_DELTA),
        'iat': datetime.utcnow()
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
