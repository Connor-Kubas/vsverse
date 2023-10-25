from django.shortcuts import render
from .models import User
import bcrypt
import uuid

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

#     if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
#     print("Password is correct!")
# else:
#     print("Password is incorrect.")

    return render(request, 'index.html')

def sign_up(request):
    return render(request, 'sign-up.html', context={})

def sign_up_user(request):

    username = request.POST['username']
    password = request.POST['password']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 

    user = User()

    user.id = str(uuid.uuid4())  
    user.user_name = username
    user.password = hashed_password

    request.session['user_id'] = str(user.id)
    request.session['user_name'] = user.user_name

    user.save()

    return render(request, 'index.html')

def logout(request):
    print('logged out successfully')
    request.session.clear()

    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')