from django.shortcuts import render
from .models import User

# Create your views here.
def login(request):
    print('applesauce')
    return render(request, 'login.html', context={})

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    user = User.objects.filter(user_name=username).first()

    request.session['user_id'] = str(user.id)
    request.session['user_name'] = str(user.user_name)

    return render(request, 'index.html')

def sign_up(request):
    return render(request, 'sign-up.html', context={})

def logout(request):
    print('logged out successfully')
    request.session.clear()

    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')