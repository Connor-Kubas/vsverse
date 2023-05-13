from django.shortcuts import render
from django.http import HttpResponse
from .models import Cards
from .models import Decks
from .models import CardImages
from django.db.models import F
# Create your views here.
def index(request):
    return render(request, 'index.html')

def deck(request):
    deck_id = 1
    # deck = CardImages.objects.filter(card_id__in=Decks.objects.filter(deck_id=deck_id).values('card_id'))

    # card = Cards.objects.get(id=74)
    deck = Decks.objects.filter(deck_id=deck_id).values_list('card_id', flat=True)
    cards = Cards.objects.filter(id__in=deck)
    card_images = [card.card_image for card in cards]

    context = {'deck': card_images}

    return render(request, 'deck.html', context)