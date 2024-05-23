from pydantic import BaseModel
from ninja import Schema


class UrlBotData(BaseModel):
    robot_name: str
    url: str


class TestBotData(BaseModel):
    robot_name: str
    name: str
    password: str


class SipecBotData(BaseModel):
    robot_name: str
    cpf: str
    password: str
    year: int
    sector: str


class TaskResponse(Schema):
    message: str
    run: str
