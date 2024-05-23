from ninja import Router, Body, File
from ninja.files import UploadedFile
from django.http import HttpRequest
from api.application.ports.taskPort import ITaskUseCase
from api.application.ports.robotPort import IRobotUseCase
from api.adapters.inbound.http.dtos.Auth import Error
from api.adapters.inbound.http.dtos.Task import (
    TaskResponse,
    UrlBotData,
    TestBotData,
    SipecBotData,
)
from api.adapters.inbound.http.utils.Task import validate_request
from typing import Any, Optional


class TaskController:
    taskUseCase: ITaskUseCase
    robotUseCase: IRobotUseCase

    def __init__(
        self,
        taskUseCase: ITaskUseCase,
        robotUseCase: IRobotUseCase,
    ) -> None:
        self.taskUseCase = taskUseCase
        self.robotUseCase = robotUseCase

    def get_router(self):
        router = Router()

        @router.post(
            "/{robot_id}/execute", response={200: TaskResponse, 400: Error, 404: Error}
        )
        @validate_request(key="data", schemas=[UrlBotData, TestBotData, SipecBotData])
        def execute_task(
            request: HttpRequest,
            robot_id: str,
            data: dict[str, Any] = Body(...),
            file: Optional[UploadedFile] = File(None),
        ):
            robot = self.robotUseCase.get_robot_by_id(robot_id)

            if not robot:
                return 404, {"error": "Esse robo nao existe"}

            if not file:
                run = self.taskUseCase.map_robot_to_execution(
                    data["robot_name"], robot, data
                )

                return 200, {"message": "Tarefa iniciada com successo", "run": run.id}

            run = self.taskUseCase.map_robot_to_execution(
                data["robot_name"], robot, data, file
            )

            return 200, {"message": "Tarefa iniciada com successo", "run": run.id}

        return router
