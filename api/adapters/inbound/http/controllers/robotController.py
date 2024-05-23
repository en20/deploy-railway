from ninja import Router
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from api.adapters.inbound.http.dtos.Auth import Error
from api.adapters.inbound.http.dtos.Robot import RobotResponse, RobotsResponse
from api.application.ports.tokenPort import ITokenUseCase
from api.application.ports.robotPort import IRobotUseCase


class RobotController:
    tokenUseCase: ITokenUseCase
    robotUseCase: IRobotUseCase

    def __init__(
        self, tokenUseCase: ITokenUseCase, robotUseCase: IRobotUseCase
    ) -> None:
        self.tokenUseCase = tokenUseCase
        self.robotUseCase = robotUseCase

    def get_router(self):
        router = Router()

        @router.get("/", response=RobotsResponse)
        def robots(request: HttpRequest, response: HttpResponse):
            access_token = request.auth

            payload = self.tokenUseCase.decode_token(access_token)

            all_bots = self.robotUseCase.get_all_robots_by_groups(payload["groups"])

            if all_bots is None:
                return {
                    "message": "There are no robots avaliable",
                    "robots": [],
                }

            return {
                "message": "Bots fetched successfully",
                "robots": list(all_bots),
            }

        @router.get("/{robot_id}", response={200: RobotResponse, 404: Error})
        def robot(request, robot_id):
            try:
                robot = self.robotUseCase.get_robot_by_id(robot_id)
                return {"message": "Robot fetched successfully", "robot": robot}

            except ObjectDoesNotExist:
                return 404, {"error": "This robot does not exist"}

        return router
