from api.adapters.outbound.database.models.robot import Robot as RobotSchema
from api.domain.repositories.IRobotRepository import IRobotRepository
from django.core.exceptions import ObjectDoesNotExist
from api.domain.entities.robot import Robot
from api.adapters.outbound.database.models.group import Group as GroupSchema


class RobotRepository(IRobotRepository):
    def create(
        self, name: str, description: str, section_name: str, group: GroupSchema
    ) -> Robot:
        return self.schemaToRobot(
            RobotSchema.objects.create(
                name=name,
                description=description,
                section_name=section_name,
                group=group,
            )
        )

    def rawCreate(
        self, name: str, description: str, section_name: str, group: GroupSchema
    ) -> RobotSchema:
        return RobotSchema.objects.create(
            name=name,
            description=description,
            section_name=section_name,
            group=group,
        )

    def update(
        self,
        id: str,
        name: str,
        description: str,
        section_name: str,
        group: GroupSchema,
    ) -> bool:
        try:
            RobotSchema.objects.filter(id=id).update(
                name=name,
                description=description,
                section_name=section_name,
                group=group,
            )
            return True
        except ObjectDoesNotExist:
            return False

    def delete(self, id) -> bool:
        try:
            RobotSchema.objects.filter(id=id).delete()
            return True
        except ObjectDoesNotExist:
            return False

    def findById(self, id) -> Robot:
        return self.schemaToRobot(RobotSchema.objects.get(id=id))

    def findAll(self, skip, limit) -> list[Robot]:
        return list(map(self.schemaToRobot, RobotSchema.objects.all()[skip:limit]))

    def findAllByGroups(self, groups: list[str]) -> list[Robot]:
        return list(
            map(
                self.schemaToRobot,
                filter(
                    lambda robot: robot.group.id in groups, RobotSchema.objects.all()
                ),
            )
        )

    def schemaToRobot(self, schema: RobotSchema) -> Robot:
        return Robot(
            schema.id,
            schema.name,
            schema.description,
            schema.section_name,
            schema.group.id,
            str(schema.created_at),
        )

    def robotToSchema(self, robot: Robot) -> RobotSchema:
        try:
            return RobotSchema.objects.get(id=robot.id)
        except ObjectDoesNotExist:
            return None
