from django.db import models
from api.adapters.outbound.database.models.utils import id_generator


class Group(models.Model):
    id = models.CharField(
        max_length=16, primary_key=True, default=id_generator, editable=False
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField("created_at", auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
