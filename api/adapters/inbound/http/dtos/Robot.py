from ninja import Schema
from api.domain.entities.robot import Robot


class RobotsResponse(Schema):
    message: str
    robots: list[Robot]


class RobotResponse(Schema):
    message: str
    robot: Robot
