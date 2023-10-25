# Generated by Django 4.2.1 on 2023-10-24 08:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("user_name", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=128)),
            ],
            options={
                "db_table": "user",
                "managed": False,
            },
        ),
    ]
