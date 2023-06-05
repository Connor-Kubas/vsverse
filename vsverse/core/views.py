from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Cards
from .models import Decks
from .models import CardImages
from .models import DeckCards
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect

# Create your views here.
def index(request):

    decks = Decks.objects.all()

    context = {'decks': decks}

    return render(request, 'index.html', context)

def deck(request, deck_id, display_method="row"):
    deck_cards = DeckCards.objects.filter(deck_id=deck_id)
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

def partial_search(request, deck_id):
    if request.htmx:
      search = request.GET.get('q')

      if search:
          cards = Cards.objects.filter(title__icontains=search)
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
    deck_card = DeckCards.objects.get(card_id=card_id, deck_id=deck_id)
    deck_card.quantity -= 1
    if deck_card.quantity > 0:
        deck_card.save()
    else:
        deck_card.delete()

    return HttpResponse(str(deck_card.quantity))

def add_table_row(request, deck_id, card_id):
    print('it made it here')
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

def edit_deck_modal(request):

    decks = Decks.objects.all()
    context = {'decks': decks}

    return render(request, 'partials/edit-deck-modal.html', context)

def create_deck_modal(request):
    return render(request, 'partials/create-deck-modal.html')

def create_deck(request):
    deck_name = request.POST.get('deck_name')
    # deck = Decks
    # deck.title = deck_name
    # deck.save()
    deck = Decks(title=deck_name)
    deck.save()

    
    return render(request, 'index.html')

def advanced_search(request):
    cards = []

    context = {'cards': cards}

    return render(request, 'advanced-search.html', context)

def advanced_search_get(request):
    title = request.GET.get('title')
    version = request.GET.get('version')
    power = request.GET.get('power')
    cost = request.GET.get('cost')
    flight = request.GET.get('flight')
    range = request.GET.get('range')
    attack = request.GET.get('attack')
    defense = request.GET.get('defense')
    affiliation = request.GET.get('affiliation')

    cards = Cards.objects.all()

    if title:
        cards = cards.filter(title__icontains=title)
    
    if version:
        cards = cards.filter(version__icontains=version)

    if power:
        cards = cards.filter(power__icontains=power)

    if cost:
        cards = cards.filter(cost=cost)

    if flight:
        cards = cards.filter(flight='1')

    if range:
        cards = cards.filter(range='1')

    if attack:
        cards = cards.filter(attack=attack)

    if defense:
        cards = cards.filter(defense=defense)

    if affiliation:
        cards = cards.filter(affiliation__icontains=affiliation)

    context = {'cards': cards}

    return render(request, 'advanced-search.html', context)

def card_template(request):
    card = Cards.objects.get(title="Lay Down With Dogs")
    context = {'card': card}

    return render(request, 'card-template.html', context)

def card_search(request):

    return render(request, 'partials/card-search.html')

def change_display_method(request, deck_id):
    display_method = request.GET.get('view-select')
    deck_cards = DeckCards.objects.filter(deck_id=deck_id)
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

def deck_select(request):
    decks = Decks.objects.all()  

    context = {
        'decks': decks,
    }

    return render(request, 'deck-select.html', context)