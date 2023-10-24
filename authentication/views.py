from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'login.html', context={})

def sign_up(request):
    return render(request, 'sign-up.html', context={})