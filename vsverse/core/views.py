from django.shortcuts import render
from django.http import HttpResponse
from .models import Cards
from .models import Decks
from .models import CardImages
# Create your views here.
def index(request):
    return render(request, 'index.html')

def deck(request):
    deck_id = 1

    deck = CardImages.objects.filter(card_id__in=Decks.objects.filter(deck_id=deck_id).values('card_id'))

    context = {'deck': deck}



    return render(request, 'deck.html', context)