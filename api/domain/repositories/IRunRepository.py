from api.domain.entities.run import Run
from abc import ABC, abstractmethod
from api.adapters.outbound.database.models.run import Run as RunSchema
from api.adapters.outbound.database.models.robot import Robot as RobotSchema


# Interface for Run repository
class IRunRepository(ABC):
    @abstractmethod
    def create(self, task: str, robot: RobotSchema) -> Run:
        pass

    @abstractmethod
    def rawCreate(self, task: str, robot: RobotSchema) -> RunSchema:
        pass

    @abstractmethod
    def update(self, id: str, task: str, robot: RobotSchema, status: str) -> bool:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    def findById(self, id: str) -> Run:
        pass

    @abstractmethod
    def findAll(self, skip, limit) -> list[Run]:
        pass

    @abstractmethod
    def getRobotRuns(self, robotId) -> list[Run]:
        pass

    @abstractmethod
    def countRobotRuns(self, robotId) -> list[Run]:
        pass
