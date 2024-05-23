from api.adapters.inbound.http.controllers.taskController import TaskController
from api.adapters.outbound.database.repositories.RunRepository import RunRepository
from api.adapters.outbound.database.repositories.RobotRepository import RobotRepository
from api.application.usecases.taskUseCase import TaskUseCase
from api.application.usecases.runUseCase import RunUseCase
from api.application.usecases.robotUseCase import RobotUseCase


class TaskRouter:
    controller: TaskController

    def __init__(self) -> None:
        runRepository = RunRepository()
        robotRepository = RobotRepository()
        runUseCase = RunUseCase(runRepository, robotRepository)
        robotUseCase = RobotUseCase(robotRepository)
        taskUseCase = TaskUseCase(runUseCase)
        self.controller = TaskController(taskUseCase, robotUseCase)

    def get_router(self):
        return self.controller.get_router()
