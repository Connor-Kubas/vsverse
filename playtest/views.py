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
    for card in cards:
        data_object = Data.objects.filter(title=card.title, version=card.version, type=card.type).exclude(type='Planet')[:1]
        # print(data_object.values()[0])
        data.append(data_object.values()[0])
    # print(data)
    card_json = json.dumps(data)

    context = {
        'cards': data,
        'card_json': card_json
    }

    return render(request, 'playtest/templates/index.html', context)