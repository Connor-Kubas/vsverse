from core.models import DeckCards
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

def increment_card_quantity(request, deck, card):
    try:
        deck_card = DeckCards.objects.get(card_id=card, deck_id=deck)
        deck_card.quantity += 1
    except ObjectDoesNotExist:
        deck_card = DeckCards(card_id=card, deck_id=deck, quantity=1)

    deck_card.save()

    return HttpResponse(str(deck_card.quantity))

def decrement_card_quantity(request, deck, card):
    print()

# restful: decks/{deck}/cards/{card}/increment