from django.shortcuts import render
from core.models import Decks
from core.models import DeckCards
from core.models import Data

def deck(request, deck_id, display_method="stack"):
    deck_cards = DeckCards.objects.filter(deck_id=deck_id).order_by('card__cost')
    deck = Decks.objects.filter(id=deck_id)  

    card_ids_and_quantities = deck_cards.values_list('card_id', 'quantity')

    # add uuid attribute to the card.

    # for deck_card in deck_cards:
    #     deck_card.card.

    for card, (_, quantity) in zip(deck_cards, card_ids_and_quantities):
        card.quantity = quantity

    context = {
        'deck_cards': deck_cards,
        'deck': deck,
        'deck_id': deck_id,
        'display_method': display_method,
    }

    return render(request, 'deck.html', context)

# def getUUIDFromCard(card):
#     # print(card)
#     data = Data.objects.filter(title=card.title, version=card.version)

#     return data.uuid