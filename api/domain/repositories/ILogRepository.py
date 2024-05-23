from api.domain.entities.log import Log
from abc import ABC, abstractmethod
from api.adapters.outbound.database.models.log import Log as LogSchema
from api.adapters.outbound.database.models.run import Run as RunSchema


# Interface for Log repository
class ILogRepository(ABC):

    @abstractmethod
    def create(self, run: RunSchema, content: str, level: str) -> Log:
        pass

    @abstractmethod
    def rawCreate(self, run: RunSchema, content: str, level: str) -> LogSchema:
        pass

    @abstractmethod
    def update(self, id: str, run: RunSchema, content: str, level: str) -> bool:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    def findById(self, id: str) -> Log:
        pass

    @abstractmethod
    def findAll(self, skip, limit) -> list[Log]:
        pass

    @abstractmethod
    def get_logs_by_run_id(self, run_id) -> list[Log]:
        pass

    @abstractmethod
    def count_logs_by_run_id(self, run_id) -> int:
        pass
