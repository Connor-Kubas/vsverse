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
    cards = Cards.objects.filter(id__in=deck).order_by('cost')
    card_images = [card.card_image for card in cards]

    context = {'deck': card_images}

    return render(request, 'deck.html', context)

def search(request, data):
    search = request.GET.get('data')
    context = {'data': search}
    print(data)
    print(request.GET)
    # print(data)
    return render(request, 'deck.html', context)
    # print(request, data)

def partial_search(request):
    if request.htmx:
    #   print(request.GET.get('q'))
      search = request.GET.get('q')

      if search:
          cards = Cards.objects.filter(title__icontains=search)
          print(cards)
      else:
          cards = Cards.objects.none()

      return render(
          request=request,
          template_name='partial_results.html',
          context={
              'cards': cards
          }
      )
    return render(request, 'partial_search.html')