from rest_framework.exceptions import APIException


class BaseAPIException(APIException):
    def __init__(self, code, message, errors=None):
        self.status_code = code
        self.detail = {
            'error': {
                'code': code,
                'message': message,
                'errors': errors or {}
            }
        }


class ValidationError(BaseAPIException):
    def __init__(self, errors):
        super().__init__(
            code=422,
            message='Validation error',
            errors=errors
        )


class NotFoundError(BaseAPIException):
    def __init__(self, resource='Resource'):
        super().__init__(
            code=404,
            message=f'{resource} not found',
            errors={'id': [f'{resource} with this ID does not exist']}
        )


class UnauthorizedError(BaseAPIException):
    def __init__(self):
        super().__init__(
            code=401,
            message='Unauthorized',
            errors={'token': ['Invalid or missing token']}
        )
        