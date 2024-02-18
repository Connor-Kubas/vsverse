from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from ..models import Cards
from ..models import Decks
from ..models import CardImages
from ..models import DeckCards
from ..models import Data
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Q
from django.db.models import Count

def deck(request, deck_id, display_method="stack"):
    deck_cards = DeckCards.objects.filter(deck_id=deck_id).order_by('card__cost')
    deck = Decks.objects.filter(id=deck_id)  

    card_ids_and_quantities = deck_cards.values_list('card_id', 'quantity')

    for card, (_, quantity) in zip(deck_cards, card_ids_and_quantities):
        card.quantity = quantity

    context = {
        'deck_cards': deck_cards,
        'deck': deck,
        'deck_id': deck_id,
        'display_method': display_method,
    }

    return render(request, 'deck.html', context)