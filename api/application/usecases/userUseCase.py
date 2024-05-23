from api.application.ports.userPort import IUserUseCase
from api.domain.repositories.IUserRepository import IUserRepository
from api.domain.entities.user import User


class UserUseCase(IUserUseCase):
    repository: IUserRepository

    def __init__(self, repository: IUserRepository) -> None:
        self.repository = repository

    def create_user(self, user: User) -> User:
        return self.repository.create(user)

    def get_user_by_id(self, id: str) -> User:
        return self.repository.findById(id)

    def get_user_by_email(self, email: str) -> User:
        return self.repository.findByEmail(email)
