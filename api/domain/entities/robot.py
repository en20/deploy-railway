from pydantic import BaseModel


class Robot(BaseModel):
    id: str
    name: str
    description: str
    section_name: str
    group: str
    created_at: str

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        section_name: str,
        group: str,
        created_at: str,
    ) -> None:
        super().__init__(
            id=id,
            name=name,
            description=description,
            section_name=section_name,
            group=group,
            created_at=created_at,
        )

    def __str__(self) -> str:
        return f"{self.name}"
