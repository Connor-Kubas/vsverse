# playtest/views.py

from django.shortcuts import render

def show(request):
    return render(request, 'index.html', context={})