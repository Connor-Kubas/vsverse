from django import template
from django.template.loader import render_to_string
from ..models import CardImages
from ..models import Data
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

register = template.Library()

@register.simple_tag
def card(card, width=294, height=410):

    print(card.title + card.version)
    if (hasattr(card, 'uuid')): # Data object
        file = card.uuid + '.jpg'
    else:                       # Card object
        data = Data.objects.filter(title=card.title, version=card.version, type=card.type).exclude(type='Planet')[:1].get()
        # data = get_data_from_card(card)
        print(data)
        file = data.uuid + '.jpg'
    
    context = {
        'file': file,
        'width': width,
        'height': height,
    }

    return render_to_string('card_image_template.html', context)

def get_data_from_card(card):
    data = None
    threshold = 50  # Adjust the threshold as needed

    potential_data = Data.objects.all()
    potential_titles = [potential.title for potential in potential_data]
    potential_versions = [potential.version for potential in potential_data]

    # Find the closest match for the card title
    best_title_match = process.extractOne(card.title, potential_titles)

    if best_title_match and best_title_match[1] >= threshold:
        # Retrieve the data object with the closest match title
        matched_title = best_title_match[0]

        # Filter potential data based on matched title
        filtered_data = potential_data.filter(title=matched_title)

        # Find the closest match for the card version within the filtered data
        best_version_match = process.extractOne(card.version, potential_versions)

        if best_version_match and best_version_match[1] >= threshold:
            # Retrieve the data object with the closest match version
            matched_version = best_version_match[0]

            # Retrieve the data object with the matched title and version
            data = filtered_data.get(version=matched_version)

    return data

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
    elif method == 'grid':
        return render_to_string('grid-template.html', context)
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
def card_template(card, width, height):
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
        'width': width,
        'height': height,
    }

    return render_to_string('card-template.html', context)
