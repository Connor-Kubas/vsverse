from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('deck/', views.deck, name='deck'),
    path('deck/search/<str:data>/', views.search),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)