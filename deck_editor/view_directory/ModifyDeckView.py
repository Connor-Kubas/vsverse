from core.models import DeckCards
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# It might be nice to be able to just type in the quantity you want.

def increment_card_quantity(request,deck_id, deck_card: DeckCards):
    deck_card = modify_card_quantity(deck_card, 1)

    return HttpResponse(str(deck_card.quantity))

def decrement_card_quantity(request, deck_id, deck_card):
    deck_card = modify_card_quantity(deck_card, -1)

    return HttpResponse(str(deck_card.quantity))

def modify_card_quantity(deck_card, value):
    deck_card = DeckCards.objects.get(id=deck_card)
    deck_card.quantity += value
    deck_card.save()

    return deck_card

# restful: decks/{deck}/cards/{card}/increment