from ninja import NinjaAPI
from api.adapters.inbound.http.utils.Auth import InvalidToken, InvalidCookie, AuthBearer
from django.urls import path

from api.adapters.inbound.http.controllers.authController import AuthController
from api.application.usecases.userUseCase import UserUseCase
from api.application.usecases.tokenUseCase import TokenUseCase
from api.tests.unit.mocks.userRepository import MockUserRepository

from api.application.usecases.robotUseCase import RobotUseCase
from api.adapters.inbound.http.controllers.robotController import RobotController
from api.tests.unit.mocks.robotRepository import MockRobotRepository
from api.tests.unit.mocks.mockController import MockController

api = NinjaAPI(csrf=False, urls_namespace="test-api")


@api.exception_handler(InvalidToken)
def handle_token_exception(request, exc):
    return api.create_response(request, {"error": exc.message}, status=401)


@api.exception_handler(InvalidCookie)
def handle_cookie_exception(request, exc):
    return api.create_response(request, {"error": exc.message}, status=401)


tokenUseCase = TokenUseCase()
mockRepository = MockUserRepository()
authController = AuthController(tokenUseCase, UserUseCase(mockRepository))

mockRobotRepository = MockRobotRepository()
robotUseCase = RobotUseCase(mockRobotRepository)
robotController = RobotController(tokenUseCase, robotUseCase)

mockController = MockController()

api.add_router("/robot/", robotController.get_router(), auth=AuthBearer())
api.add_router("/auth/", authController.get_routes())
api.add_router("/test/", mockController.get_router())

urlpatterns = [path("api/", api.urls)]
