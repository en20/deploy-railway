from ninja.security import HttpBearer, APIKeyCookie
from api.application.usecases.tokenUseCase import TokenUseCase


class InvalidToken(Exception):
    def __init__(self, message):
        self.message = message


class InvalidCookie(Exception):
    def __init__(self, message):
        self.message = message


class CookieKey(APIKeyCookie):
    param_name = "refresh_token"

    def authenticate(self, request, key):
        if not key:
            raise InvalidCookie("cookie not found")

        valid, message = TokenUseCase().verify_token(key, self.param_name)
        if not valid:
            raise InvalidCookie(message)

        return key


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        valid, message = TokenUseCase().verify_token(token, "access_token")

        if not valid:
            raise InvalidToken(message)

        return token


cookieAuth = CookieKey()
