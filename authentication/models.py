from django.db import models
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128) 

    class Meta:
        managed = False
        db_table = 'user'