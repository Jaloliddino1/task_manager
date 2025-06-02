from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from U2_rest.settings import SECRET_KEY
from accounts.models import User
from accounts.service import verify_token

SECRET_KEY = SECRET_KEY


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token_type, token = auth_header.split()
        except ValueError:
            raise AuthenticationFailed('Authorization header must be in the format: Bearer <token>')

        if token_type.lower() != 'bearer':
            raise AuthenticationFailed('Authorization header must start with Bearer')

        payload = verify_token(token, SECRET_KEY, type='access')

        if not isinstance(payload, dict):
            raise AuthenticationFailed(payload)

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, None)
