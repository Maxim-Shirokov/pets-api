from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class ApiKeyAuthentication(TokenAuthentication):

    def authenticate(self, request):
        api_key_secret = request.headers.get('X-API-SECRET')
        if api_key_secret == settings.API_SECRET:
            return None
        raise exceptions.AuthenticationFailed('Unauthorized')