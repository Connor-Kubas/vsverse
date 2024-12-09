from django.shortcuts import render
from core.models import Decks
from core.models import DeckCards

from collections import defaultdict

def deck(request, deck_id, display_method="stack"):
    deck_cards = DeckCards.objects.filter(deck_id=deck_id).order_by('card__cost')
    deck = Decks.objects.get(id=deck_id)

    card_types = {}
    total_cards = 0

    non_character_count = 0
    character_count = 0

    # 1 -> 4
    # 2 -> 6, etc
    character_cost_counts = {}
    # character_cost_counts = defaultdict(int, int)
    # for i in range(0, 15):
    #     character_cost_counts[i] = 0

    for deck_card in deck_cards:
        quantity = deck_card.quantity
        total_cards += quantity
        
        if (deck_card.card.type == 'Character'):
            if (character_cost_counts.get(deck_card.card.cost)):
                character_cost_counts[deck_card.card.cost] += deck_card.quantity
            else:
                character_cost_counts[deck_card.card.cost] = deck_card.quantity

        non_character_count += deck_card.quantity if deck_card.card.type != 'Character' else 0
        character_count += deck_card.quantity if deck_card.card.type == 'Character' else 0
        card_type = deck_card.card.type
        card_types[card_type] = card_types.get(card_type, 0) + quantity

    # print(character_cost_counts.items())
    # for key, value in character_cost_counts.items():
    #     print(key, value)

    context = {
        'deck_cards': deck_cards,
        'deck': deck,
        'deck_id': deck_id,
        'display_method': display_method,
        'total_cards': total_cards,
        'card_types': card_types,
        'character_count': character_count,
        'non_character_count': non_character_count,
        'character_cost_counts': character_cost_counts,
    }

    return render(request, 'deck.html', context)
