# Generated by Django 4.2.7 on 2024-04-29 01:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_decks_main_card_alter_decks_id_alter_decks_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="decks",
            name="user_id",
            field=models.CharField(max_length=36),
        ),
    ]