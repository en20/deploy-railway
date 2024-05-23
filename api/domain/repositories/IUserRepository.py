from api.domain.entities.user import User
from abc import ABC, abstractmethod
from api.adapters.outbound.database.models.user import User as UserSchema


# Interface for User repository
class IUserRepository(ABC):

    @abstractmethod
    def create(self, name: str, email: str, password: str) -> User:
        pass

    @abstractmethod
    def rawCreate(self, name: str, email: str, password: str) -> UserSchema:
        pass

    @abstractmethod
    def update(self, id, name: str, email: str, password: str) -> bool:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    def findById(self, id: str) -> User:
        pass

    @abstractmethod
    def findByEmail(self, email: str) -> User:
        pass

    @abstractmethod
    def findAll(self, skip, limit) -> list[User]:
        pass
