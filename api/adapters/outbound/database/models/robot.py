from django.db import models
from api.adapters.outbound.database.models.utils import id_generator
from api.adapters.outbound.database.models.group import Group


class Robot(models.Model):
    id = models.CharField(
        max_length=16, primary_key=True, default=id_generator, editable=False
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    section_name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField("created_at", auto_now_add=True)

    def __str__(self):
        return self.name
