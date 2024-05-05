from django.shortcuts import render
from core.models import Decks
from core.models import DeckCards

def deck(request, deck_id, display_method="stack"):
    deck_cards = DeckCards.objects.filter(deck_id=deck_id).order_by('card__cost')
    deck = Decks.objects.get(id=deck_id)

    card_types = {}
    total_cards = 0

    non_character_count = 0
    character_count = 0

    for deck_card in deck_cards:
        quantity = deck_card.quantity
        total_cards += quantity
        
        non_character_count += deck_card.quantity if deck_card.card.type != 'Character' else 0
        character_count += deck_card.quantity if deck_card.card.type == 'Character' else 0
        card_type = deck_card.card.type
        card_types[card_type] = card_types.get(card_type, 0) + quantity

    context = {
        'deck_cards': deck_cards,
        'deck': deck,
        'deck_id': deck_id,
        'display_method': display_method,
        'total_cards': total_cards,
        'card_types': card_types,
        'character_count': character_count,
        'non_character_count': non_character_count,
    }

    return render(request, 'deck.html', context)
