from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('login-user', views.login_user, name='login-user'),

    path('logout', views.logout, name="logout"),

    path('sign-up', views.sign_up, name="sign-up"),

    path('profile', views.profile, name="profile"),
]