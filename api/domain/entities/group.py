from pydantic import BaseModel


# Group entity
class Group(BaseModel):
    id: str
    name: str
    description: str
    created_at: str

    def __init__(self, id: str, name: str, description: str, created_at: str) -> None:
        super().__init__(
            id=id, name=name, description=description, created_at=created_at
        )

    def __str__(self) -> str:
        return f"{self.name}"
