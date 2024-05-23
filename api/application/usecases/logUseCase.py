from api.application.ports.logPort import ILogUseCase
from api.domain.entities.log import Log
from api.domain.repositories.ILogRepository import ILogRepository


class LogUseCase(ILogUseCase):
    logRepository: ILogRepository

    def __init__(self, logRepository: ILogRepository) -> None:
        self.logRepository = logRepository

    def list_logs(self, run_id) -> list[Log]:
        return self.logRepository.get_logs_by_run_id(run_id)

    def count_logs(self, run_id) -> int:
        return self.logRepository.count_logs_by_run_id(run_id)
