from django.db import models
from api.adapters.outbound.database.models.utils import id_generator, format_date_string
from api.adapters.outbound.database.models.robot import Robot


class Status(models.TextChoices):
    PENDING = "PENDING", "pending"
    SUCCESS = "SUCCESS", "success"
    FAILURE = "FAILURE", "failure"


class Run(models.Model):
    id = models.CharField(
        max_length=16, primary_key=True, default=id_generator, editable=False
    )
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE)
    task = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    started_at = models.DateTimeField("started_at", auto_now_add=True)

    def __str__(self):
        return (
            f"{self.robot.name} - {self.task} - {format_date_string(self.started_at)}"
        )
