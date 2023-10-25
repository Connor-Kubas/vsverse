from django.shortcuts import render

# Create your views here.
def login(request):
    print('applesauce')
    return render(request, 'login.html', context={})

def login_user(request):
    print('eeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    return render(request, 'index.html')

def sign_up(request):
    return render(request, 'sign-up.html', context={})