from django.shortcuts import render
from django.http import HttpResponse
from .models import Cards
# Create your views here.
def index(request):
    return render(request, 'index.html')

def test(request):
    queryset = Cards.objects.all()
    context = {'data': queryset}

    return render(request, 'test.html', context)