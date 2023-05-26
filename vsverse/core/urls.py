from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('deck/<int:deck_id>/', views.deck, name='deck'),
    # path('deck/<str:deck_id>', views.deck, name='deck'),
    # path('deck/search/<str:data>', views.search, name="data"),
    # path('/deck/search/<str:data>', views.search, name="data"),
    path('partial-search/<int:deck_id>/', views.partial_search, name='partial_search'),
    path('view_deck', views.view_deck, name="view_deck"),
    path('increment_quantity/<int:deck_id>/<int:card_id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:deck_id>/<int:card_id>/', views.decrement_quantity, name='decrement_quantity'),

    path('add_table_row/<int:deck_id>/<int:card_id>/', views.add_table_row, name='add_table_row'),
    # path('add_from_search/<int:deck_id/<int:card_id>')

    path('edit-deck-modal', views.edit_deck_modal, name='edit-deck-modal'),
    path('create-deck-modal', views.create_deck_modal, name='create-deck-modal'),
    path('create_deck/', views.create_deck, name='create_deck'),

    path('advanced-search/', views.advanced_search, name="advanced-search"),
    path('card-template/', views.card_template, name="card-template"),

    path('card-search', views.card_search, name='card-search'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)