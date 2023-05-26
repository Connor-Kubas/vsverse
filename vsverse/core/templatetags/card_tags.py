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

@register.inclusion_tag('card-template.html')
def card_template(card):
    # image_name = ''

    range_name = ''
    flight_name = ''

    if card.range == '1' and card.visible == 'Visible':
        range_name = 'visible_range'
    elif card.range == '1' and card.visible != 'Visible':
        range_name = 'concealed_range'

    if card.flight == '1' and card.visible == 'Visible':
        flight_name = 'visible_flight'
    elif card.flight == '1' and card.visible != 'Visible':
        flight_name = 'concealed_flight'

    if card.visible == 'Visible' and card.type == 'Character':
        print('character')
        image_name = 'new_character'
    elif card.visible == 'Concealed':
        image_name = 'new_character_concealed'
    elif card.visible == 'Concealed—Optional':
        image_name = 'new_character_concealed_optional'
    elif card.type == 'Equipment':
        image_name = 'equipment'
    elif card.type == 'Plot Twist':
        image_name = 'plot_twist'
    elif card.type == 'Location':
        image_name = 'new_location'
    else:
        image_name = 'new_character'

    if card.attack is None:
        card.attack = ''
        card.defense = ''

    context = {
        'card': card,
        'image_name': image_name,
        'range_name': range_name,
        'flight_name': flight_name,
    }

    return context
