# Generated by Django 4.2.1 on 2023-05-11 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='decks',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='decks',
            name='deck_card_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='decks',
            name='id',
        ),
    ]