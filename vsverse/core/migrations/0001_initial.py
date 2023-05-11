# Generated by Django 4.2.1 on 2023-05-11 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliations',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('affiliation', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'affiliations',
            },
        ),
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('version', models.CharField(blank=True, max_length=100, null=True)),
                ('power', models.CharField(blank=True, max_length=1000, null=True)),
                ('type', models.CharField(blank=True, max_length=10, null=True)),
                ('cost', models.IntegerField(blank=True, null=True)),
                ('attack', models.IntegerField(blank=True, null=True)),
                ('defense', models.IntegerField(blank=True, null=True)),
                ('affiliation', models.CharField(blank=True, max_length=40, null=True)),
                ('mutant', models.CharField(blank=True, max_length=30, null=True)),
                ('flight', models.CharField(blank=True, max_length=10, null=True)),
                ('range', models.CharField(blank=True, max_length=10, null=True)),
                ('visible', models.CharField(blank=True, max_length=20, null=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'cards',
            },
        ),
        migrations.CreateModel(
            name='Expansions',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('abbreviation', models.CharField(blank=True, max_length=3, null=True)),
                ('expansion', models.CharField(blank=True, max_length=50, null=True)),
                ('year_date', models.CharField(blank=True, max_length=25, null=True)),
                ('number_of_cards', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'expansions',
            },
        ),
        migrations.CreateModel(
            name='Decks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deck_id', models.IntegerField(blank=True, null=True)),
                ('card_id', models.IntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'decks',
                'unique_together': {('deck_id', 'card_id')},
            },
        ),
    ]