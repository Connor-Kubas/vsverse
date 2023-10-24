from django.contrib import admin
from .models import Affiliations, Cards, Decks, Expansions
# Register your models here.
admin.site.register(Affiliations)
admin.site.register(Cards)
admin.site.register(Decks)
admin.site.register(Expansions)