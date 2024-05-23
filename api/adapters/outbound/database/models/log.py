from django.db import models
from api.adapters.outbound.database.models.utils import id_generator, format_date_string
from api.adapters.outbound.database.models.run import Run


class LogLevel(models.TextChoices):
    INFO = "INFO", "info"
    WARNING = "WARNING", "warning"
    ERROR = "ERROR", "error"


class Log(models.Model):
    id = models.CharField(
        max_length=16, primary_key=True, default=id_generator, editable=False
    )
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    level = models.CharField(
        max_length=12, choices=LogLevel.choices, default=LogLevel.INFO
    )
    executed_at = models.DateTimeField("executed_at", auto_now_add=True)

    def __str__(self):
        return f"{self.run.robot.name} - {self.content} - {format_date_string(self.executed_at)}"
