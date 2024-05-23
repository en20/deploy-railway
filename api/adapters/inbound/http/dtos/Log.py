from ninja import Schema
from api.domain.entities.run import Run
from api.domain.entities.log import Log


class LogResponse(Schema):
    message: str
    run: Run
    logs: list[Log]


class LogCountResponse(Schema):
    message: str
    count: int
