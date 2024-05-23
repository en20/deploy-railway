from api.application.ports.taskPort import ITaskUseCase
from api.application.ports.runPort import IRunUseCase
from api.domain.entities.run import Run
from api.domain.entities.robot import Robot
from typing import Any
from django.utils import timezone
from api.adapters.outbound.celery.tasks.access_url import access_url
from api.adapters.outbound.celery.tasks.mock_bot import execute_mock_bot
from api.adapters.outbound.celery.tasks.sipec_bot import execute_sipec_bot


class TaskUseCase(ITaskUseCase):
    runUseCase: IRunUseCase
    robot_to_execution: dict[str, Any]

    def __init__(self, runUseCase: IRunUseCase) -> None:
        self.runUseCase = runUseCase
        self.robot_to_execution = {
            "url_robot": self.execute_url_robot,
            "test_robot": self.execute_test_robot,
            "sipec_robot": self.execute_sipec_robot,
        }

    def map_robot_to_execution(self, robot, *args) -> Run:
        return self.robot_to_execution[robot](*args)

    def save_file(self, file) -> str:
        file_path = f"upload-{file.name}-{timezone.now()}.csv"

        with open(file_path, "wb") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        return file_path

    def execute_url_robot(self, robot: Robot, data: dict[str, Any]) -> Run:
        run = self.runUseCase.createRun(robot, f"Acessar {data['url']}")
        access_url.apply_async(args=[run.id, data["url"]])
        return run

    def execute_test_robot(self, robot: Robot, data: dict[str, Any], file) -> Run:
        file_path = self.save_file(file)
        run = self.runUseCase.createRun(
            robot, "Cadastrar novos usuários no django admin"
        )

        execute_mock_bot.apply_async(
            args=[file_path, run.id, data["name"], data["password"]]
        )

        return run

    def execute_sipec_robot(self, robot: Robot, data: dict[str, Any], file) -> Run:
        file_path = self.save_file(file)

        run = self.runUseCase.createRun(
            robot, "Cadastrar necessidades dos servidores no SIPEC"
        )

        execute_sipec_bot.apply_async(
            args=[
                file_path,
                run.id,
                data["cpf"],
                data["password"],
                data["year"],
                data["sector"],
            ]
        )

        return run
