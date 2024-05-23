from abc import ABC, abstractmethod
from api.domain.entities.robot import Robot


class IRobotUseCase(ABC):
    @abstractmethod
    def get_all_robots_by_groups(self, groups: list[str]) -> list[Robot]:
        pass

    @abstractmethod
    def get_robot_by_id(self, robotId: str) -> Robot:
        pass
