from pydantic import BaseModel


class Run(BaseModel):
    id: str
    robot: str
    task: str
    status: str
    started_at: str

    def __init__(
        self, id: str, robot: str, task: str, status: str, started_at: str
    ) -> None:
        super().__init__(
            id=id, robot=robot, task=task, status=status, started_at=started_at
        )

    def __str__(self) -> str:
        return f"{self.robot}"
