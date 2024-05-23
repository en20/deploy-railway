from api.adapters.outbound.database.models.group import Group as GroupSchema
from api.domain.repositories.IGroupRepository import IGroupRepository
from django.core.exceptions import ObjectDoesNotExist
from api.domain.entities.group import Group


class GroupRepository(IGroupRepository):
    def create(self, name: str, description: str) -> Group:
        return self.schemaToGroup(
            GroupSchema.objects.create(
                name=name,
                description=description,
            )
        )

    def rawCreate(self, name: str, description: str) -> GroupSchema:
        return GroupSchema.objects.create(
            name=name,
            description=description,
        )

    def update(self, id, name: str, description: str) -> bool:
        try:
            GroupSchema.objects.filter(id=id).update(
                name=name,
                description=description,
            )
            return True
        except ObjectDoesNotExist:

            return False

    def delete(self, id) -> bool:
        try:
            GroupSchema.objects.filter(id=id).delete()
            return True
        except ObjectDoesNotExist:
            return False

    def findById(self, id) -> Group:
        return self.schemaToGroup(GroupSchema.objects.get(id=id))

    def findAll(self, skip, limit) -> list[Group]:
        return list(map(self.schemaToGroup, GroupSchema.objects.all()[skip:limit]))

    def schemaToGroup(self, schema: GroupSchema) -> Group:
        return Group(schema.id, schema.name, schema.description, str(schema.created_at))

    def groupToSchema(self, group: Group) -> GroupSchema:
        try:
            return GroupSchema.objects.get(id=group.id)
        except ObjectDoesNotExist:
            return None
