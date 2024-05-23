from api.adapters.outbound.database.models.user import User as UserSchema
from api.domain.entities.user import User
from api.domain.repositories.IUserRepository import IUserRepository
from django.core.exceptions import ObjectDoesNotExist


# Concrete implementation for User Repository
class UserRepository(IUserRepository):
    def create(self, name: str, email: str, password: str) -> User:
        return self.schemaToUser(
            UserSchema.objects.create(
                name=name,
                email=email,
                password=password,
            )
        )

    def rawCreate(self, name: str, email: str, password: str) -> UserSchema:
        return UserSchema.objects.create(
            name=name,
            email=email,
            password=password,
        )

    def update(self, id, name: str, email: str, password: str) -> bool:
        try:
            UserSchema.objects.filter(id=id).update(
                name=name,
                email=email,
                password=password,
            )
            return True
        except ObjectDoesNotExist:
            return False

    def delete(self, id) -> bool:
        try:
            UserSchema.objects.filter(id=id).delete()
            return True
        except ObjectDoesNotExist:
            return False

    def findById(self, id) -> User:
        try:
            return self.schemaToUser(UserSchema.objects.get(id=id))
        except ObjectDoesNotExist:
            return None

    def findByEmail(self, email: str) -> User:
        try:
            return self.schemaToUser(UserSchema.objects.get(email=email))
        except ObjectDoesNotExist:
            return None

    def findAll(self, skip, limit) -> list[User]:
        return list(map(self.schemaToUser, UserSchema.objects.all()[skip:limit]))

    def schemaToUser(self, schema: UserSchema) -> User:
        return User(
            schema.id,
            schema.name,
            schema.email,
            schema.password,
            str(schema.created_at),
            [group.id for group in schema.groups.all()],
        )

    def userToSchema(self, user: User) -> UserSchema:
        try:
            return UserSchema.objects.get(id=user.id)
        except ObjectDoesNotExist:
            return None
