# playtest/views.py
from core.models import Data

from django.shortcuts import render

def show(request):

    card = Data.objects.first()

    context = {
        'card': card
    }

    return render(request, 'playtest/templates/index.html', context)