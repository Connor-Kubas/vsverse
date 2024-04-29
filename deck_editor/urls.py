from django.urls import path, include
# from . import views
from . import views
# import view_directory.DisplayView as DisplayView

urlpatterns = [
    path('deck/<int:deck_id>/', views.DisplayView.deck, name='deck'),
    path('deck/<int:deck_id>/cards/<int:deck_card>/increment', views.ModifyDeckView.increment_card_quantity, name="increment"),
    path('deck/<int:deck_id>/cards/<int:deck_card>/decrement', views.ModifyDeckView.decrement_card_quantity, name="decrement"),
]