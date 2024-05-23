from ninja import NinjaAPI
from api.adapters.inbound.http.routes.run import RunRouter
from api.adapters.inbound.http.routes.auth import AuthRouter
from api.adapters.inbound.http.routes.log import LogRouter
from api.adapters.inbound.http.routes.robot import RobotRouter
from api.adapters.inbound.http.routes.task import TaskRouter
from api.adapters.inbound.http.utils.Auth import InvalidToken, InvalidCookie, AuthBearer

api = NinjaAPI()


@api.exception_handler(InvalidToken)
def handle_token_exception(request, exc):
    return api.create_response(request, {"error": exc.message}, status=401)


@api.exception_handler(InvalidCookie)
def handle_cookie_exception(request, exc):
    return api.create_response(request, {"error": exc.message}, status=401)


runRouter = RunRouter()
logRouter = LogRouter()
authRouter = AuthRouter()
robotRouter = RobotRouter()
taskRouter = TaskRouter()

api.add_router("/robots/", robotRouter.get_router(), auth=AuthBearer())
api.add_router("/robots/", runRouter.get_router(), auth=AuthBearer())
api.add_router("/robots/", logRouter.get_router(), auth=AuthBearer())
api.add_router("/robots/", taskRouter.get_router(), auth=AuthBearer())
api.add_router("/auth/", authRouter.get_router())
