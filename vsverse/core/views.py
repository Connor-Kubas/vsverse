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
    # deck = CardImages.objects.filter(card_id__in=Decks.objects.filter(deck_id=deck_id).values('card_id'))

    deck_cards = DeckCards.objects.filter(deck_id=deck_id)

    # Get the card_ids and quantities from the DeckCards objects
    card_ids_and_quantities = deck_cards.values_list('card_id', 'quantity')

    # Retrieve the Cards objects for the card_ids
    cards = Cards.objects.filter(id__in=[card_id for card_id, _ in card_ids_and_quantities])

    # Assign the quantities to the respective Cards objects
    for card, (_, quantity) in zip(cards, card_ids_and_quantities):
        card.quantity = quantity

    context = {'deck': cards}

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

def increment_quantity(request, card_id):
    deck_card = DeckCards.objects.get(card_id=card_id)
    print(deck_card)
    deck_card.quantity += 1
    deck_card.save()
    return HttpResponse(str(deck_card.quantity))

def decrement_quantity(request, card_id):
    deck_card = get_object_or_404(DeckCards, card_id=card_id)
    if deck_card.quantity > 0:
        deck_card.quantity -= 1
        deck_card.save()
    return HttpResponse(str(deck_card.quantity))