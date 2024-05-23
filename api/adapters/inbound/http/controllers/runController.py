from ninja import Router
from django.http import HttpRequest
from api.application.ports.runPort import IRunUseCase
from api.adapters.inbound.http.dtos.Run import RunResponse, RunCountResponse


DEFAULT_SKIP = 0
DEFAULT_LIMIT = 0


class RunController:
    useCase: IRunUseCase

    def __init__(self, useCase: IRunUseCase) -> None:
        self.useCase = useCase

    def get_routes(self):
        router = Router()

        @router.get("/{robotId}/runs", response={200: RunResponse})
        def getRobotRuns(
            request: HttpRequest,
            robotId: str,
            skip: int = DEFAULT_SKIP,
            limit: int = DEFAULT_LIMIT,
        ):
            robot_runs = self.useCase.getRobotRuns(robotId, skip, limit)

            if len(robot_runs) == 0:
                return {
                    "message": "There are no executions avaliable",
                    "runs": [],
                }

            return {
                "message": "Executions fetched successfully",
                "runs": list(robot_runs),
            }

        @router.get("/{robotId}/runs/count", response={200: RunCountResponse})
        def countRobotRuns(request: HttpRequest, robotId: str):
            count = self.useCase.countRobotRuns(robotId)

            return {
                "message": "Execution count fetched successfully",
                "count": count,
            }

        return router
