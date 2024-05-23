from api.adapters.outbound.database.repositories.LogRepository import LogRepository
from api.adapters.outbound.database.repositories.RunRepository import RunRepository
from api.adapters.outbound.database.repositories.RobotRepository import RobotRepository
from api.application.usecases.logUseCase import LogUseCase
from api.application.usecases.runUseCase import RunUseCase
from api.adapters.inbound.http.controllers.logController import LogController


class LogRouter:
    controller: LogController

    def __init__(self) -> None:
        logRepo = LogRepository()
        runRepo = RunRepository()
        robotRepository = RobotRepository()
        logUseCase = LogUseCase(logRepo)
        runUseCase = RunUseCase(runRepo, robotRepository)
        self.controller = LogController(logUseCase, runUseCase)

    def get_router(self):
        return self.controller.get_router()
