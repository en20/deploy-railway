from ninja import Schema
from api.domain.entities.run import Run


class RunResponse(Schema):
    message: str
    runs: list[Run]


class RunCountResponse(Schema):
    message: str
    count: int
