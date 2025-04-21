# playtest/views.py
from core.models import Data
from core.models import DeckCards
from core.models import Cards
from django.db.models import Q

from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder

def show(request, deck_id):

    deck_cards = DeckCards.objects.filter(deck_id=deck_id)

    card_ids = deck_cards.values_list('card_id', flat=True)

    cards = Cards.objects.filter(id__in=card_ids)

    # data = Data.objects.filter(title=card.title, version=card.version, type=card.type).exclude(type='Planet')[:1].get()

    data = []
    # for card in cards:
    #     data_object = Data.objects.filter(title=card.title, version=card.version, type=card.type).exclude(type='Planet')[:1]
    #     # print(data_object.values()[0])
        
    #     data.append(data_object.values()[0])

    # This adds the correct amount of cards according to the quantity in the deck.
    for deck_card in deck_cards:
        data_object = Data.objects.filter(title=deck_card.card.title, version=deck_card.card.version, type=deck_card.card.type).exclude(type='Planet')[:1]
        t = data_object.values()[0]
        for i in range(deck_card.quantity):
            # This adds a unique identifier to each card.
            t['identifier'] = str(i) + t['uuid']
            data.append(t)

    card_json = json.dumps(data)

    context = {
        'cards': data,
        'uuid_list': data,
        'card_json': card_json
    }

    return render(request, 'playtest/templates/index.html', context)

# def show(request, deck_id):
#     deck_cards = DeckCards.objects.filter(deck_id=deck_id)

#     uuids = {}
#     for deck_card, i in deck_cards
#         uuids[i] = 

#     return 