from pydantic import BaseModel


class Log(BaseModel):
    id: str
    run: str
    content: str
    level: str
    executed_at: str

    def __init__(
        self, id: str, run: str, content: str, level: str, executed_at: str
    ) -> None:
        super().__init__(
            id=id, run=run, content=content, level=level, executed_at=executed_at
        )

    def __str__(self) -> str:
        return f"{self.run}"
