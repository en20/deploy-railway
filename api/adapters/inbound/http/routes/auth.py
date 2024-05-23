from api.adapters.inbound.http.controllers.authController import AuthController
from api.adapters.outbound.database.repositories.UserRepository import UserRepository
from api.application.usecases.userUseCase import UserUseCase
from api.application.usecases.tokenUseCase import TokenUseCase


class AuthRouter:
    controller: AuthController

    def __init__(self) -> None:
        tokenUseCase = TokenUseCase()
        repository = UserRepository()
        userUseCase = UserUseCase(repository)
        self.controller = AuthController(tokenUseCase, userUseCase)

    def get_router(self):
        return self.controller.get_routes()
