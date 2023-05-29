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
    deck = Decks.objects.filter(id=deck_id)

    # for card in deck_cards:
    #     try:
    #         print(card.card.card_image.image_name)
    #     except:
    #         print('didnt work')
    

    card_ids_and_quantities = deck_cards.values_list('card_id', 'quantity')

    for card, (_, quantity) in zip(deck_cards, card_ids_and_quantities):
        card.quantity = quantity

    context = {
        'deck_cards': deck_cards,
        'deck': deck,
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
    # cards = Cards.objects.order_by('title')[:50]
    # query = 'select * from cards where title = "Muramasa Blade"'
    # cards = Cards.objects.raw(query)
    cards = []
    # deck_cards = DeckCards.objects.filter(deck_id=5)
    # cards = [card.card for card in deck_cards]
    # for card in cards:
    #     print(card.card)
    
    # cards = Cards.objects.raw('SELECT * FROM cards WHERE power LIKE CONCAT("%", %s, "%") ORDER BY cost ASC', ['Illuminati'])


    context = {'cards': cards}

    return render(request, 'advanced-search.html', context)

def advanced_search_get(request):


    title = request.GET.get('title')
    version = request.GET.get('version')

    cards = Cards.objects.all()

    if title:
        cards = cards.filter(title=title)
    
    if version:
        cards = cards.filter(version=version)


    context = {'cards': cards}

    return render(request, 'advanced-search.html', context)

def card_template(request):
    card = Cards.objects.get(title="Lay Down With Dogs")
    context = {'card': card}

    return render(request, 'card-template.html', context)

def card_search(request):

    return render(request, 'partials/card-search.html')