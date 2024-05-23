from abc import ABC, abstractmethod
from api.domain.entities.run import Run
from api.domain.entities.robot import Robot


class IRunUseCase(ABC):
    @abstractmethod
    def createRun(self, robot: Robot, task: str) -> Run:
        pass

    @abstractmethod
    def getRobotRuns(self, robot, skip, limit) -> list[Run]:
        pass

    @abstractmethod
    def getRunById(self, runId) -> Run:
        pass

    @abstractmethod
    def countRobotRuns(self, robot) -> int:
        pass

    @abstractmethod
    def updateRunStatus(self, run: Run, status: str) -> bool:
        pass
