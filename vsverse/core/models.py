from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Affiliations(models.Model):
    id = models.IntegerField(primary_key=True)
    affiliation = models.CharField(max_length=25)

    class Meta:
        # managed = False
        db_table = 'affiliations'


class Cards(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=100, blank=True, null=True)
    power = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    attack = models.IntegerField(blank=True, null=True)
    defense = models.IntegerField(blank=True, null=True)
    affiliation = models.CharField(max_length=40, blank=True, null=True)
    mutant = models.CharField(max_length=30, blank=True, null=True)
    flight = models.CharField(max_length=10, blank=True, null=True)
    range = models.CharField(max_length=10, blank=True, null=True)
    visible = models.CharField(max_length=20, blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'cards'


class Decks(models.Model):
    deck_id = models.IntegerField(blank=True, null=True)
    card_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'decks'


class Expansions(models.Model):
    id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=3, blank=True, null=True)
    expansion = models.CharField(max_length=50, blank=True, null=True)
    year_date = models.CharField(max_length=25, blank=True, null=True)
    number_of_cards = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'expansions'

class CardImages(models.Model):
    # card_id = models.IntegerField()
    image_name = models.CharField(max_length=50)
    image_type = models.CharField(max_length=4)
    card = models.OneToOneField(Cards, on_delete=models.CASCADE, related_name='card_image')
    # card = models.OneToOneField()

    class Meta:
        db_table = 'card_images'

