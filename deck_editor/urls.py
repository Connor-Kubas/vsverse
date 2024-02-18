from django.urls import path, include
# from . import views
from . import views
# import view_directory.DisplayView as DisplayView

urlpatterns = [
    path('deck/<int:deck_id>/', views.DisplayView.deck, name='deck'),
]