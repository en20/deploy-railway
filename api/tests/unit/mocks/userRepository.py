from api.domain.repositories.IUserRepository import IUserRepository
from api.domain.entities.user import User
from api.adapters.outbound.database.models.utils import id_generator
from api.adapters.outbound.database.models.user import User as UserSchema


class MockUserRepository(IUserRepository):
    database: list[User] = []

    def create(self, name: str, email: str, password: str) -> User:
        user = User(id_generator(), name, email, password, "now", ["group1"])
        self.database.append(user)
        return user

    def rawCreate(self, name: str, email: str, password: str) -> UserSchema:
        pass

    def update(self, id, name: str, email: str, password: str) -> bool:
        for i in range(len(self.database)):
            current_user = self.database[i]
            if current_user.id == id:
                self.database[i] = User(
                    current_user.id,
                    name,
                    email,
                    password,
                    current_user.created_at,
                    current_user.groups,
                )
                return True
        return False

    def delete(self, id) -> bool:
        for i in range(len(self.database)):
            if self.database[i].id == id:
                self.database.pop(i)
                return True
        return False

    def findById(self, id) -> User:
        for i in range(len(self.database)):
            if self.database[i].id == id:
                return self.database[i]
        return None

    def findByEmail(self, email: str) -> User:
        for i in range(len(self.database)):
            if self.database[i].email == email:
                return self.database[i]
        return None

    def findAll(self, skip, limit) -> list[User]:
        return self.database
