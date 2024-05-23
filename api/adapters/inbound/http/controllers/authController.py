from ninja import Router
from django.http import HttpRequest, HttpResponse
from api.application.ports.tokenPort import ITokenUseCase
from api.application.ports.userPort import IUserUseCase
from api.adapters.inbound.http.dtos.Auth import (
    LoginRequestBody,
    DecodeResponse,
    AccessResponse,
    Error,
    CsrfResponse,
)
from api.adapters.inbound.http.utils.Auth import cookieAuth, AuthBearer
from django.middleware.csrf import get_token


class AuthController:
    tokenUseCase: ITokenUseCase
    userUseCase: IUserUseCase

    def __init__(self, tokenUseCase: ITokenUseCase, userUseCase: IUserUseCase):
        self.tokenUseCase = tokenUseCase
        self.userUseCase = userUseCase

    def get_routes(self):
        router = Router()

        @router.get("/csrf", response=CsrfResponse)
        def get_csrf(request: HttpRequest, response: HttpResponse):
            response.set_cookie("csrftoken", get_token(request))

            return {"message": "csrf token set successfully"}

        @router.post("/login", response={200: AccessResponse, 400: Error})
        def login(
            request: HttpRequest, response: HttpResponse, credentials: LoginRequestBody
        ):
            user = self.userUseCase.get_user_by_email(credentials.email)

            if not user:
                return 400, {"error": "Email invalido"}

            if user.password != credentials.password:
                return 400, {"error": "Senha incorreta"}

            access_token = self.tokenUseCase.generate_token(
                user.id, user.email, user.groups, "access_token"
            )
            refresh_token = self.tokenUseCase.generate_token(
                user.id, user.email, user.groups, "refresh_token"
            )

            response.set_cookie("refresh_token", refresh_token, httponly=True)

            return {
                "message": "logged in successfully",
                "access_token": access_token,
            }

        @router.get(
            "/decode", auth=AuthBearer(), response={200: DecodeResponse, 401: Error}
        )
        def decode(request: HttpRequest, response: HttpResponse):
            access_token = request.auth

            payload = self.tokenUseCase.decode_token(access_token)

            return {
                "message": "Token decoded successfully",
                "user": payload["user"],
                "email": payload["email"],
                "groups": payload["groups"],
            }

        @router.get(
            "/refresh", auth=cookieAuth, response={200: AccessResponse, 401: Error}
        )
        def refresh(request):
            refresh_token = request.auth

            payload = self.tokenUseCase.decode_token(refresh_token)

            access_token = self.tokenUseCase.generate_token(
                payload["user"], payload["email"], payload["groups"], "access_token"
            )

            return {
                "message": "Token refreshed successfully",
                "access_token": access_token,
            }

        return router
