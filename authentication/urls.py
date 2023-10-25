from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('login-user', views.login_user, name='login-user'),

    path('logout', views.logout, name="logout"),

    path('sign-up', views.sign_up, name="sign-up"),
    path('sign-up-user', views.sign_up_user, name="sign-up-user"),

    path('profile', views.profile, name="profile"),
]