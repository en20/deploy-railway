from abc import ABC, abstractmethod
from typing import Any
from api.domain.entities.run import Run


class ITaskUseCase(ABC):
    @abstractmethod
    def map_robot_to_execution(self, robot, *args) -> Run:
        pass

    @abstractmethod
    def execute_url_robot(self, robot: str, data: dict[str, Any], file: str) -> Run:
        pass

    @abstractmethod
    def execute_test_robot(self, robot: str, data: dict[str, Any], file: str) -> Run:
        pass

    @abstractmethod
    def execute_sipec_robot(self, robot: str, data: dict[str, Any]) -> Run:
        pass
