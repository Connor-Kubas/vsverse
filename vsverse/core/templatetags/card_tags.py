# card_tags.py

from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def card(file):
    context = {'file': file}
    return render_to_string('card_template.html', context)
