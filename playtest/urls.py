from django.urls import path, include
from . import views

urlpatterns = [
    # path('playtest', views.show, name='show'),
    path('playtest/<int:deck_id>/', views.show, name='show'),
]