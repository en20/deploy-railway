from abc import ABC, abstractmethod
from api.domain.entities.log import Log


class ILogUseCase(ABC):
    @abstractmethod
    def list_logs(self, run_id) -> list[Log]:
        pass

    @abstractmethod
    def count_logs(self, run_id) -> int:
        pass
