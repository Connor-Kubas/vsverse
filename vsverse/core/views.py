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

    decks = Decks.objects.all()

    context = {'decks': decks}

    return render(request, 'index.html', context)

def deck(request, deck_id):
    deck_cards = DeckCards.objects.filter(deck_id=deck_id)

    card_ids_and_quantities = deck_cards.values_list('card_id', 'quantity')

    for card, (_, quantity) in zip(deck_cards, card_ids_and_quantities):
        card.quantity = quantity

    context = {'deck': deck_cards}

    return render(request, 'deck.html', context)

def partial_search(request, deck_id):
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
              'cards': cards,
              'deck_id': deck_id,
          }
      )
    return render(request, 'partial_search.html')

def view_deck(request):
    # if request.method == "GET":
    # else:
        
    return render(request, 'edit_modal.html')

def increment_quantity(request, deck_id, card_id):
    try:
        deck_card = DeckCards.objects.get(card_id=card_id, deck_id=deck_id)
        deck_card.quantity += 1
    except DeckCards.DoesNotExist:
        deck_card = DeckCards(card_id=card_id, deck_id = deck_id, quantity=1)
    deck_card.save()

    return HttpResponse(str(deck_card.quantity))

def decrement_quantity(request, deck_id, card_id):
    print(deck_id)
    print(card_id)
    deck_card = DeckCards.objects.get(card_id=card_id, deck_id=deck_id)
    deck_card.quantity -= 1
    if deck_card.quantity > 0:
        deck_card.save()
    else:
        deck_card.delete()

    return HttpResponse(str(deck_card.quantity))

def add_table_row(request, deck_id, card_id):
    try:
        deck_card = DeckCards.objects.get(card_id=card_id, deck_id=deck_id)
        deck_card.quantity += 1
    except DeckCards.DoesNotExist:
        deck_card = DeckCards(card_id=card_id, deck_id = deck_id, quantity=1)
    deck_card.save()
    template_name = 'partials/add-table-row.html'
    context = {
        'deck_card': deck_card,
        'deck_id': deck_id,
    }
    return render(request, template_name, context)

def edit_deck(request):

    decks = Decks.objects.all()
    context = {'decks': decks}

    return render(request, 'partials/edit-deck-modal.html', context)

def create_deck(request):
    return render(request, 'partials/create-deck-modal.html')