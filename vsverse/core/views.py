from django.shortcuts import render
from django.http import HttpResponse
from .models import Cards
from .models import Decks
from .models import CardImages
from .models import DeckCards
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request, 'index.html')

def deck(request):
    deck_id = request.GET.get('deck_id')

    deck_cards = DeckCards.objects.filter(deck_id=deck_id)

    card_ids_and_quantities = deck_cards.values_list('card_id', 'quantity')

    # cards = Cards.objects.filter(id__in=[card_id for card_id, _ in card_ids_and_quantities])

    for card, (_, quantity) in zip(deck_cards, card_ids_and_quantities):
        card.quantity = quantity

    context = {'deck': deck_cards}

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

def view_deck(request):
    # if request.method == "GET":
    # else:
        
    return render(request, 'edit_modal.html')

def increment_quantity(request, deck_id, card_id):
    deck_card = DeckCards.objects.get(card_id=card_id, deck_id=deck_id)
    print(deck_id)
    deck_card.quantity += 1
    deck_card.save()
    return HttpResponse(str(deck_card.quantity))

def decrement_quantity(request, deck_id, card_id):
    deck_card = DeckCards.objects.get(card_id=card_id, deck_id=deck_id)
    if deck_card.quantity > 0:
        deck_card.quantity -= 1
        deck_card.save()
    return HttpResponse(str(deck_card.quantity))