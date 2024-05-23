from api.application.ports.robotPort import IRobotUseCase
from api.domain.repositories.IRobotRepository import IRobotRepository
from api.domain.entities.robot import Robot


class RobotUseCase(IRobotUseCase):
    robotRepository: IRobotRepository

    def __init__(self, robotRepository: IRobotRepository) -> None:
        self.robotRepository = robotRepository

    def get_all_robots_by_groups(self, groups: list[str]) -> list[Robot]:
        return self.robotRepository.findAllByGroups(groups)

    def get_robot_by_id(self, robotId: str) -> Robot:
        return self.robotRepository.findById(robotId)
