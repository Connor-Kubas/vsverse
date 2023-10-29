# playtest/views.py
from core.models import Data

from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder

def show(request):

    cards = Data.objects.all()

    cards = cards[:5]

    card_json = json.dumps(list(cards.values()))

    print(card_json)

    # print(cards)

    context = {
        'cards': cards,
        'card_json': card_json
    }

    return render(request, 'playtest/templates/index.html', context)