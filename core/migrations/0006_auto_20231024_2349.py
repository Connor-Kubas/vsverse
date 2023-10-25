from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_delete_user"),
    ]

    operations = [
        migrations.AddField(
            model_name='decks',
            name='user_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
