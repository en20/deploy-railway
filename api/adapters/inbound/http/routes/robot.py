from api.adapters.outbound.database.repositories.RobotRepository import RobotRepository
from api.application.usecases.tokenUseCase import TokenUseCase
from api.application.usecases.robotUseCase import RobotUseCase
from api.adapters.inbound.http.controllers.robotController import RobotController


class RobotRouter:
    controller: RobotController

    def __init__(self) -> None:
        robotRepo = RobotRepository()
        robotUseCase = RobotUseCase(robotRepo)
        tokenUseCase = TokenUseCase()
        self.controller = RobotController(tokenUseCase, robotUseCase)

    def get_router(self):
        return self.controller.get_router()
