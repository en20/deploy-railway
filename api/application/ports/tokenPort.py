from abc import ABC, abstractmethod


class ITokenUseCase(ABC):
    @abstractmethod
    def generate_token(
        self, userId: str, email: str, groups: list[str], token_type: str
    ) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str):
        pass

    @abstractmethod
    def verify_token(self, token: str, token_type: str) -> tuple[bool, str]:
        pass
