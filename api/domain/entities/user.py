from typing import Annotated
from pydantic import BaseModel, Field


# User Entity
class User(BaseModel):
    id: str
    name: str
    email: str
    password: Annotated[str, Field(exclude=True)]
    created_at: str
    groups: list[str]

    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        password: str,
        created_at: str,
        groups: list[str],
    ) -> None:
        super().__init__(
            id=id,
            name=name,
            email=email,
            password=password,
            created_at=created_at,
            groups=groups,
        )

    def __str__(self) -> str:
        return f"{self.name}"
