from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('deck/', views.deck, name='deck'),
    # path('deck/<str:deck_id>', views.deck, name='deck'),
    # path('deck/search/<str:data>', views.search, name="data"),
    # path('/deck/search/<str:data>', views.search, name="data"),
    path('search/', views.search, name='search'),
    path('partial-search/', views.partial_search, name='partial_search'),
    path('view_deck', views.view_deck, name="view_deck"),
    path('increment_quantity/<int:card_id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:card_id>/', views.decrement_quantity, name='decrement_quantity'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)