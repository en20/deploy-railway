from api.domain.repositories.IRobotRepository import IRobotRepository
from api.domain.entities.robot import Robot
from api.adapters.outbound.database.models.utils import id_generator
from api.adapters.outbound.database.models.group import Group as GroupSchema
from api.adapters.outbound.database.models.robot import Robot as RobotSchema


class MockRobotRepository(IRobotRepository):
    database: list[Robot] = []

    def create(self, name: str, description: str, section_name: str) -> Robot:
        robot = Robot(id_generator(), name, description, section_name, "group1", "now")
        self.database.append(robot)
        return robot

    def rawCreate(
        self, name: str, description: str, section_name: str, group: GroupSchema
    ) -> RobotSchema:
        pass

    def update(
        self, id, name: str, description: str, section_name: str, group: str
    ) -> bool:
        for i in range(len(self.database)):
            current_robot = self.database[i]
            if current_robot.id == id:
                self.database[i] = Robot(
                    current_robot.id,
                    name,
                    description,
                    section_name,
                    current_robot.created_at,
                    current_robot.groups,
                )
                return True
        return False

    def delete(self, id) -> bool:
        for i in range(len(self.database)):
            if self.database[i].id == id:
                self.database.pop(i)
                return True
        return False

    def findById(self, id) -> Robot:
        for i in range(len(self.database)):
            if self.database[i].id == id:
                return self.database[i]
        return None

    def findAllByGroups(self, group: str) -> Robot:
        for i in range(len(self.database)):
            if self.database[i].group == group:
                return self.database[i]
        return None

    def findAll(self, skip, limit) -> list[Robot]:
        return self.database
