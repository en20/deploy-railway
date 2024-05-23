from ninja import Router
from django.http import HttpRequest
from api.application.ports.logPort import ILogUseCase
from api.application.ports.runPort import IRunUseCase
from api.adapters.inbound.http.dtos.Log import LogCountResponse, LogResponse
from api.adapters.inbound.http.dtos.Run import RunResponse
from api.adapters.inbound.http.dtos.Auth import Error


DEFAULT_SKIP = 0
DEFAULT_LIMIT = 0


class LogController:
    logUseCase: ILogUseCase
    runUseCase: IRunUseCase

    def __init__(self, logUseCase: ILogUseCase, runUseCase: IRunUseCase):
        self.logUseCase = logUseCase
        self.runUseCase = runUseCase

    def get_router(self):
        router = Router()

        @router.get(
            "/{robot_id}/runs/{run_id}/logs",
            response={200: LogResponse, 400: Error, 404: Error},
        )
        def get_logs(
            request: HttpRequest,
            robot_id,
            run_id,
            skip: int = DEFAULT_SKIP,
            limit: int = DEFAULT_LIMIT,
        ):
            run = self.runUseCase.getRunById(run_id)

            if run is None:
                return 404, {"error": "this run does not exist"}

            logs = self.logUseCase.list_logs(run_id)

            return {
                "message": "Logs fetched successfully",
                "run": run,
                "logs": logs,
            }

        @router.get(
            "/{robot_id}/runs/{run_id}/logs/count",
            response={200: LogCountResponse, 400: Error, 404: Error},
        )
        def logs_count(
            request: HttpRequest,
            robot_id,
            run_id,
            skip: int = DEFAULT_SKIP,
            limit: int = DEFAULT_LIMIT,
        ):
            run = self.runUseCase.getRunById(run_id)

            if run is None:
                return 404, {"error": "This run does not exist"}

            logs_count = self.logUseCase.count_logs(run_id)

            return {"message": "Logs count fetched successfully", "count": logs_count}

        return router
