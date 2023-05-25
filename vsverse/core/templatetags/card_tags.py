from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def card(file):
    context = {'file': file}
    return render_to_string('card_image_template.html', context)

@register.simple_tag
def search(deck):
    context = {'deck': deck[0]}

    return render_to_string('search-template.html', context)

@register.simple_tag
def display_method(method, deck):
    context = {'deck': deck}
    if method == 'row':
        return render_to_string('row-template.html', context)
    elif method == 'table':
        return render_to_string('table-template.html', context)
    elif method == 'stack':
        return render_to_string('stack-template.html', context)
    else:
        return ''

# Returns the quantity of a given card type in a deck.
@register.filter
def quantity(deck, card_type):
    deck_card_list = list(deck)

    deck_cards = [card for card in deck_card_list]

    cards = [card.card for card in deck_cards]

    return sum(1 for card in cards if card.type == card_type)

@register.simple_tag
def card_template(card):

    context = {}

    return ('card_template.html', context)
