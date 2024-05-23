# Generated by Django 5.0.3 on 2024-04-26 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_log"),
    ]

    operations = [
        migrations.CreateModel(
            name="Usuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=200)),
                ("email", models.CharField(max_length=200)),
                ("telefone", models.CharField(max_length=200)),
            ],
        ),
    ]
