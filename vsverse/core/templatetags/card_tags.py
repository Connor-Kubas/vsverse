from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def card(file):
    context = {'file': file}
    return render_to_string('card_template.html', context)

@register.simple_tag
def search():
    # context = {'card': card}
    return render_to_string('partials/search-template.html')

@register.simple_tag
def display_method(method, deck):
    context = {'deck': deck}
    if method == 'row':
        return render_to_string('row-template.html', context)
    elif method == 'table':
        return render_to_string('table-template.html', context)
    else:
        return ''