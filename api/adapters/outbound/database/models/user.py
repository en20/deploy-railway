from django.db import models
from api.adapters.outbound.database.models.utils import id_generator
from api.adapters.outbound.database.models.group import Group


class User(models.Model):
    id = models.CharField(
        max_length=16, primary_key=True, default=id_generator, editable=False
    )
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    groups = models.ManyToManyField(Group)

    def __str__(self):
        return f"{self.name}"


# Only for test purposes
class Usuario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)

    def __str__(self):
        return self.nome
