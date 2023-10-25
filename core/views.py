from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Cards
from .models import Decks
from .models import CardImages
from .models import DeckCards
from .models import Data
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Q
from django.db.models import Count

# Create your views here.
def index(request):

    decks = Decks.objects.all()

    context = {'decks': decks}

    return render(request, 'index.html', context)

def deck(request, deck_id, display_method="row"):
    deck_cards = DeckCards.objects.filter(deck_id=deck_id)
    deck = Decks.objects.filter(id=deck_id)  

    card_ids_and_quantities = deck_cards.values_list('card_id', 'quantity')

    for card, (_, quantity) in zip(deck_cards, card_ids_and_quantities):
        card.quantity = quantity

    context = {
        'deck_cards': deck_cards,
        'deck': deck,
        'deck_id': deck_id,
        'display_method': display_method,
    }

    return render(request, 'deck.html', context)

def partial_search(request, deck_id):
    if request.htmx:
      search = request.GET.get('q')

      if search:
          cards = Cards.objects.filter(title__icontains=search)
      else:
          cards = Cards.objects.none()

      return render(
          request=request,
          template_name='partial_results.html',
          context={
              'cards': cards,
              'deck_id': deck_id,
          }
      )

def view_deck(request):
    # if request.method == "GET":
    # else:
        
    return render(request, 'edit_modal.html')

def increment_quantity(request, deck_id, card_id):
    try:
        deck_card = DeckCards.objects.get(card_id=card_id, deck_id=deck_id)
        deck_card.quantity += 1
    except DeckCards.DoesNotExist:
        deck_card = DeckCards(card_id=card_id, deck_id = deck_id, quantity=1)
    deck_card.save()

    return HttpResponse(str(deck_card.quantity))

def decrement_quantity(request, deck_id, card_id):
    deck_card = DeckCards.objects.get(card_id=card_id, deck_id=deck_id)
    deck_card.quantity -= 1
    if deck_card.quantity > 0:
        deck_card.save()
    else:
        deck_card.delete()

    return HttpResponse(str(deck_card.quantity))

def add_table_row(request, deck_id, card_id):
    print('it made it here')
    try:
        deck_card = DeckCards.objects.get(card_id=card_id, deck_id=deck_id)
        deck_card.quantity += 1
    except DeckCards.DoesNotExist:
        deck_card = DeckCards(card_id=card_id, deck_id = deck_id, quantity=1)
    deck_card.save()
    template_name = 'partials/add-table-row.html'
    context = {
        'deck_card': deck_card,
        'deck_id': deck_id,
    }
    return render(request, template_name, context)

def edit_deck_modal(request):

    decks = Decks.objects.all()
    context = {'decks': decks}

    return render(request, 'partials/edit-deck-modal.html', context)

def create_deck_modal(request):
    return render(request, 'partials/create-deck-modal.html')

def create_deck(request):
    deck_name = request.POST.get('deck_name')
    deck = Decks(title=deck_name)
    deck.save()

    # return render(request, 'index.html')
    return redirect('index')

def advanced_search(request):
    cards = []

    context = {'cards': cards}

    return render(request, 'advanced-search.html', context)

def advanced_search_get(request):
    title = request.GET.get('title')
    version = request.GET.get('version')
    rules = request.GET.get('rules')
    cost = request.GET.get('cost')
    flight = request.GET.get('flight')
    range = request.GET.get('range')
    attack = request.GET.get('attack')
    defense = request.GET.get('defense')
    affiliation = request.GET.get('affiliation')

    cards = Data.objects.all()

    cards = cards.filter().exclude(type__icontains='planet')

    if title:
        cards = cards.filter(title__icontains=title)
    
    if version:
        cards = cards.filter(version__icontains=version)

    if rules:
        cards = cards.filter(rules__icontains=rules)

    if cost:
        cards = cards.filter(cost=cost)

    if flight:
        cards = cards.filter(flight=1)

    if range:
        cards = cards.filter(range=1)

    if attack:
        cards = cards.filter(attack=attack)

    if defense:
        cards = cards.filter(defense=defense)

    if affiliation:
        cards = cards.filter(affiliation__icontains=affiliation)

    # This is not currently working. It is removing too many instances.
    # cards = filter_duplicate_printings(cards)

    cards = cards[:100]

    plural_modifier = 's'

    if cards.count() == 1:
        plural_modifier = ''

    context = {
        'cards': cards,
        'results_quantity': cards.count(),
        'plural_modifier': plural_modifier
    }

    return render(request, 'advanced-search.html', context)

def card_template(request):
    card = Cards.objects.get(title="Lay Down With Dogs")
    context = {'card': card}

    return render(request, 'card-template.html', context)

def card_search(request):

    return render(request, 'partials/card-search.html')

def change_display_method(request, deck_id):
    display_method = request.GET.get('view-select')
    deck_cards = DeckCards.objects.filter(deck_id=deck_id)
    deck = Decks.objects.filter(id=deck_id)  

    card_ids_and_quantities = deck_cards.values_list('card_id', 'quantity')

    for card, (_, quantity) in zip(deck_cards, card_ids_and_quantities):
        card.quantity = quantity

    context = {
        'deck_cards': deck_cards,
        'deck': deck,
        'deck_id': deck_id,
        'display_method': display_method,
    }

    return render(request, 'deck.html', context)

def deck_select(request):
    decks = Decks.objects.filter(user_id=request.session['user_id'])  
    b64_image = '/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCADSAPADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDj7V3X+1JVUuvnfKO8mO/0FaUQZo03jJYZ4/kKztIaM6cr7ZN07uqkNgDJ6c1o2jvJAu8bSMhV9R714uM1hGS9D7TKqjhUnCXXUnVGKk7sf0+vrUqBWU9OP4f6ikVdpwCSpHX39vSpVXjkAAHBA7/59a8ts9iWgKu4AgkqfvN/iP8ACpkyMcZ7Ljrj/PrTVXJKklR/Ce4/Gllnhso/MuZBEo4Ynv8AUVHLzO3U56s1BXew4KoO0EAE49s003MEMrQvKvmKN2wHLEeo/wAKzP7Q1GfzUtLItFjcshOCV9jVvSdIhttt44JuJR91hlY/8DWroxhG9R/ccMsTKckqa07j/wC1oTO6QQzXDLjLLwMHvj2q2TqEirMiJs2/Kg4Y1iXp1KbU5PJsjBBAcPKn3mz39xS4u7i5VLyW5jJIYLGDtXHAPtWzw8ElKKS/E5PrEm2pG4x1NIX/ANHieQ8KF4GapNrU8V8LaeyKSBOcfxt/dU9KSW51vS2nnW1ae1jXJ3MNzfT1qR4NX1C1t2eOJDIMyRkZKH/ZPas4U6a96duX1FUrT2i3c07W4iuVYQ5Dx/fQjBWpggDFiuQTwaitNPmhm3SyB2SMIrAYOPRvWr3l8nnK9vX8PSvNr8im1Td0dFOc3C89yvtBXoeDnHrTtoDdML/nrVhUIU9Mjn/9frT/ACsEdsjNYe0RbmVNqEYwcA849aQqAOhGePrVoRDHHbkkjilMRYgAgk8gnqKXtAUyo6DgY4ApuAzD5RuJ69qtOgI3cbejACmGLHBz6jB5/OqU0PmRWIGSRkdsY6UhX5iPQduhqwyk/wD1qjZT09R261ald2LTKxjX58Z2D86huZorSDzJmCqOAe7H/Z96tyBYonldgI0BLt/CB6exrh9T1RtTu0FuXMjny7dAM4B7mu3C0XVeuwp1VHqOv9SnvrxbYI7O3CQocn6uRW3pmjx6VbGEKpmkO6UjufQH/GpdK0iLRbZg3/H0wzLLjOPYGmy6pGufLhkHGELDG8/TvXTKbqP2VFafmZc8adqtVjpbi2iwssojJ4IxwPr/APWqssTXM9tcSQSraNJzKOCR/sf/AF6iuGttOluHukkvJ5YQYoIjlkGfvH0x6VI1td394Lpr+5SyiUCG3zjnHp/WvSpUKWGi6lV69jy6uKxGMl7KjGy7mjaXmlw6rNZ6WPOu7eMzyrcj/WMQR09hz+FVLbxJdw2N1JbySyTXEYidMbWZQc71HoelBsYvtRnO83RH+sBwV9s96b5CK7zH55G5MjdvYDtVvNaaTUIhHIalSSlUmYlmmbOyhwrboTMUK85Hp71o25XapRwQeSp4ZKbbWiPb2qzB8pEMFW2k+wNRWqm3uf34QGYEbjJyPQFe31rBWq0prqtTvnzUMVSlsno/uNMrg+oPWpFXrg/N6ZxkemaEDEHKjcn6/wCNNuboWsRYqhdx8iNwM+vtXlRTm+VHrVKsYRcmJdXcdr+7Ks8xwqRKuQD7+lRwaVJNezXF8yTDbgKeQKlsLJordLia481gS4OMHHoT/EKtT31vaRxPJKm2XOwIeOP5VpJ+zahS36s85y505VtEWY41jhSJBhF6Ljj8u1SEFF3uyxk/K25sZH9awv7ZvZwVtbSRSD85IyWB6Y9aP+EfmvroQXtxJ5SjzN/bd2GO1R9WXxVZW/EiWI0Uacbmv/aVuoUecMK23fj5VPpntUkupwGORIbpDIyEK4+6W+veqSeHNPVAjfaCmcuhk4J9SKlk8ORSZ+zMkXGI4SvyZ9frUpYO6956GM6lezbigRNRudLNtLtllY5aX+FF9B71sJBtSOMHKouOnWufjubvTJp5rvMdxGuDbY3CYeqj1rdt9TtpnjjkjeBpV3xsTlcehPY+1TjMNUhZ09YvXQzo4mE+lmWViKqCeT6en41IkSlTwcH2/pU4QZ6nHp2pyRkLjJz+v5148pNM2dRkSRAKOeR0z2/GlEZAOMflVkR5GcZX/PanGP5gRnjng81nzGbqFUxlfmI596QxDYCDn2q2Ux0HXpmk8sLhSR74o5gVQpMnQ9+/P+c0nkjJYBSAMnPAA/pVzygT0GOwrP1fSI9XsTazTzQc5LRHBP19a1pyTklJ2Q/aNLQrG6sSxCXdu3qS44+tOCiYBomjkDfLuVuF964XxH4Wn8PWP2yDF3ZlsMyrhkrG0rxDcadFd28S4S6HzOWyE+npXtwy6NWnz0p3RTrpWtuaninX3lu5dPt/lt4ThsHPmMPX1rnNN1C+sdVWe2aNXk+Uh1zsB649KgmhzMXSRwQeQR196ZYyTNqkTuEKg7QP79e9RoRhT5Io56k7SSn3O2stavbiK8sppEkDAmKVTjB9D71csGur2dJSiLHEAC78gAdceh965KJYkjvWjYtKx+cIcKPp9K7zSbILotqJHWTKfOV/iHo1c1adLCRvHf8AISp1K1TX4Oi8inpNrDDFdTRBwHlPlyNyzr9KvygiTLctt9eg+vep2TcMD5SORg/dHp71FIcYG0YPtx/9Y14tWs6s+dnr4ekqUVCL2ICBIpyAMevf6elRMpGfl/HH+c1YK8kEE7fz/wDr0xgSQM4B5B/z0pKV9TrjMpRqQqqpbeAAOPT19KwdRu4I9YQDG0yDzZoxu2+vPetC+1MGS5tYGJmU7ZGH8A9j3rBnwoNrbrvaRME+nv8AWvYwsHFuT6nn41xqpJP4Xf8A4Br3niCeKZzb20bxR4DPu5x9O1a1xA2oRWt4sSu4TJUnAUn371yFtdFoPsK27LcKhBkPf3PrXY+H2V9Bt1XJKZVg3Qms6/8As6VSnujPSvBQndqX4FW20W7jZlab5Txw+Rj2rXstIs7PLeWZA3KeZzt/CrKKAoHHy8AjqKm2ZjO/gd+cA151bFzqb/gXDDU6eyFBbAOFBI6g4H/1qeiH7u4sRzwOR+FAQHAIZT6d8fSpY0XIAAwOmD1NcMpdS27LQcik7So+vPWrKxhjt7jkE0InGRw3f2qwiAAEngc+/wCFc052MJytsYGt2d6sU1+s0T/ZxuHmceWvT8al8M2dtPo8Q8mV44zlZXbPm98gU7xbcta+H8KpzcSCPOMgD3rY0a2uLbSraC62GQKCdnQfT2r0ateUcCnLu0jy3Z13bsWgo6rjB/SpFTt6frUioM4Hrk1KI88gcCvClNrc2ciARZpRFjntVgJ+BJpSoVTjJOfzpczIciAxgrjqeopPKGBkc4qaeSC1he4uJkihjGZJHOFA/wAayLfxLp91E0toJJIU4aSUbQf931rSFGrUjzRWglO7si8YyAAKa6NjAPHpnH61hweNbGUubm0kihV9omT5gPrXQ288N3bJcW0izQP9105yfetamHq0X76sVz2dnoVWjDZQYdj1V1yD9R/WuD8W+BZr65+16HHbwgr+8t2bAY+or0XYOwwe/v8ASmNGOTtDHpWuFx1XDz5qb/yHueA6nYatou1b+yljLDhscH2z6Vlec9kzSGPErDAx0QHrX0NeWdveWzQXUPnQsNpD8lfoe1eU+KvCa6BOl1aq0unSnDF+ie2a+oy/Nadd8k1aRnOk5dTkrW7uxazQwwjYV7+9dHaWeuW1pDe6fI1xbMB+9jfOD3BHtWSrKrKwIGP9UV5B9vet/wAKa2dIuBbXLsLO6fgDgRP6fSu3EOTptxjfyN4QcGlKTJR4zvIAqXenFnQ4LfdJ+gro9Nvxqdj9q+zSQMzYCSen9a1ZVQ8+VGT1DMgP5etRsCegHTp0/KvnqlelU+GHK/U9GnGad73RWA2nbj5s888fn2pjoPmwct2O3+n9amYKoyCcdDjqD71G45C457DP8jWaZ1QZw2q/Pqd9HGq2+0jzJGP3+Khjmswiwox3Ac9ct9DWr4g0b7TGbuEEzo375D/GPX8KxFuoLdSUAd16KgzkfX1r6GjKM6aaOKacZtPRK/8ASGTNJDO04UgP39K67wnNNPYzuFH2bzP3RI5YVxV5HcTqZGEhaP59i9h/tV0fh3Wls5Egk3Pp0h+VlH+rb/Cli6TqULJanPCvy1Wr6HaoBjgYDfxHpmplDZzIeg9KxD4p0KO6Ft9uWVmbA2g4BrZguop8bJMspwyuDwfb1FfOVKNSKu42Or20G7J6liOPJAIyDzgGp0Tqc9PbpUcY4PBPNW0X7vWuKTZE5Dol24ONwPANWVQbGzlVHLN/dpsaZJByPUj+Gue13xFFDu0u2LBpCEuJgRxGeu33+tFGjOtPlir9/I461XlVxsME/ijVJP8ASgLa1bkIMxyEdge9dmsQCosYJXaAOPSsazt9G8M6CJ45BDpwAZ5c5Mh9vU/Sudm8Y39/cSSxy/ZLD7sVuuPOf/aPbFdtanVxbtTVoR0VzkpRk5WgryZ6CISBwvOOMkU5UIyOa8rl8YyvKUjPKKMtzhjTpfHOsNEsEUv2dtwIZRlm9qy/seo2rSOr6libXserbWA5HOO9LtyQMqM8ZPQVwGl/EOaG+2aykM2nk4F1b/eQ/wC0Paupv/Euitot5Pa6rA7mFhEf7zY4xXPPLsRTnFNXucc1OLs00zjfEetnU9XKqc2NoStrDJx58o4Ln1APrXLG7M1xPuBkwQTsO1Se/AqitxLPE0k0oL2x3Kqnrn7wq2ZFMySgCJHXoOua+njRjSjyLY9/A4aFKKl1ZXtXKvO3kO8YfJQHpx3FafhnXn8MX0CeaXsLhtslux4Uk9V/OsyOREjuZBcMcPtOB147Vn6l8ttBDIy7VIkWVeo9K1dNVE4SWjHioRnR1d7I+hXiz3z0wW64qF0wMYz6VDoTCbw3p0jMXdoBuc9TVwhNvANfEThyTlFdGeHGT6lF05zwGzg1UvLOLUIJrSZA0coK4PY+taTAE4AOPWq0ijDAZ3diaqnNxaaepspXVjxFtNTT9QvtPnjO+N8RSY6ehqpLYzrumOXI4lQ9NvrXbePbeaHX7K5i2ot5GUdzjAYdK5uZGmB/ehXQ8gdDjqDX2uHrSqU41O6PRw6jVoNPdFvQPFhtYks9UZnsTkQXH932au1J3qpXDAjIYdxXls0az7jACbXHzoe/uK0/DevtpF0LG9lLabI3yS5z5Ten8qxxeBVRc9Na9jGMnQkoy2/r8DvWUbRnGCeD7/1qFshjluR3IxxU5I24ADDG7PaonAGC2Crd+/4V4y0O+MupSRlYFWGdx4AHFcrrOiNYPJqFmCbdjmSFRkqfUe1dUoBDEhhkc89B/UVYj4O7KhSuCv8ADj2Hau2jXlRldDxNJVF5rqeboXltJ7iOYKbZNxIPDD0NSWBS4052CgIflyo4z15/+tWnq2nLcma20qFSZSX8rGCx781lQvcaVL5NxbvDkbBE44/A19BOcZQSjueLhpN4iTqbbDxD5JVRADG43ZBHyH1FbFlq0sH7ppJJ5Y18yB+hI/ut61SIgKxBTvyNoReMVWyxhQxMGMT4w33gPWuZv2i949Kph4JNfieo6FqkGr6bHdw/fORIo/hbvUGreLtD0CdYby4L3Jxvhi5Kg9zXl2g+I7vw7quoLa28lxHOjfuAOAcfex7VF4Wu9LfxJ9q18s3mEsjjkK/v7VyU8kjKq3L4eh4VbGuK5U9UegXfxKsJ7F4LC3vEeQYW4KcY/wBniqOi6x4GWxmstQuGEsxJebYQV9evOa6E3Vr5CrD9maPORjGwn/ZHY1g6tpWmanv+02nzKM70P7wfU/xfSvWpZFH2fJTvG/mcc8S27tmNqviSLX9fS3hlxpdniO0gJwpA/jb34pzosV05mkB3Lkgn5T7isK88KRxvm2vBg/6vcfvn0x2/GqsZ1DR3aW42zRJ8rKWztFa1spqUoe7sj0cuzWlS9yceu50pnYTKV+6YwobHU56USCaSNy5UBTuwKiM8M9iswOQyhgB2NKzNLHthI3snrkYryEpdj7JOnZ2le+pR1W+NrJa3KjeknyOD0Ip/kYjjxHsDPuVVP8qikgjvraBWJc274cDjJFBvkeWNGidAGzkjoBXXbRKJ405JylUqbSWnr1G2dvfafGuuXNo76VcSNEtw3Oxgcc1pq6Iqop80I2/cem0+lei/CVINX8IaxoeoRJcWUU2RC/Uhuc+xrgvGegT+B9e+xhnn06cFrWY/wqf4c+tb1aHNHmR42CzB0ajpVGUkk3iRdyAySgouPvisfVLxpIbiO3gJCEGVlOVjGf51raJo+oeJ9Wi0uwYINhMk5HEad+fWun+JGn6b4a8J6bomlqsRluA0rkfPKMcknuM1VDDXXPIePzOTSoQd2dxovibRIPDujwyahH9oa3A2LyQfepJfF+li7jto23SOOoYba8T061a3t2k+QFsBSg61fCtAG+VG3cnnmvnamVYf2ra6nfh8olKmpyZ6i3jfRRKILt3tHZsK7cr+lbnyvB5sMiyREZMiNxt9c9K8Bu720Rz9qV5JQPlgU5/OtfRvDvie/wBLaJ9Rm03S5juWDcST9B6UTyKFRJwfL66nDjOXDytB3Ox+JVktx4Oa5jJxbzKyOhyK85NzBJElxlmOAHTrn8a3bjw7qmk6RdW1jrAuIJxtmgmBOfcH1riLe9msJjbyglUG1xjGPQ16+Gy6ph6PJJ3Sehnh8dGE2pLRm1IX+/Eu2Jh85P8ACPaqtzDEB5WP3JGc9w1aVlpN/dRF4ZI2ttu4HcCT7YoGlpZxlZpMvncqn+E+9elhMBVqSVlZG2MzGkqb1u2dL4L1QaloIikkJntGKSA/3fWtxtuc4+X39a4HQ75dO1tLkSIILg+VMg6E+uK9DIO4gjcAOSa+bznAvCYpx6PVHTlmJ9tRTXQyg4FuWIJVVLYHVj6D0qGbUYvsEjKkh3JggjBz6e9Ts2yBmWNnfGNirkn8O/1qCxla/u286F4UtyPISUY/En19qnDQhZ1Jp2R042pNyVGm1eRb0q3+z23+rxLjd85yVH1/pVm90+21O0a3uRuVuUfHKt7VJIS3zt8pHXtn8P61NhV3SFgqf3y3C/jXDOtOVTnT1LVOMI8h5jqOnXOjXrwXDbpZOLeYcK49/es+WeJNsbv5bxnJYHrXeeINV025sm094muJDxv242H/AGTXKXXw61cWUNxAUnMo+aIthk/xr3sPiIygnX91nm16tWGkNSh4W1KC18UDU9Ql2wKCjf7WfX2qp4jTTP7ZmfSpTJZyHf0+6fQV0dp8LtcuE33M9tb5OCuQeK6Sx+EWmJalL+/lluW4UxjAH+NdNTNsJSXLza+R47w9epJto8ohvLq3z5czAEYwelaYbX7qFNjSbY+RtPArvrv4MIQfsGrsCONsiZ5rLuvhb4wsiYLW4S4ifA3LNtx+Fb4bO8LPR1P0MamGnHocU1pqatI8sp3HksXqqfMB2ly2TjG7INeraT8FLuXB1vVgid4ohuJ/Go/HfwrttF0g6toDSmGEDz4HO84/vA1nLOsJUqqjCbu/uIjSktWjgtMinaJlbdycAjofate0tRDLtRjuX5W9hV7w/NFqHw9uraOHF5YT+cJMclTxzURAjtdyHcRyWHes8XpKyPrckiq1PmmtYjcj7R5axHzjx7EetUJywlMHMjjIHP3vb2xWhkKsrE4uNuRnt6VEnmKyJJAMyEEyD+H1JrGm+XU9HEwdR2/pL0JfB3i+TwrryakFle0ceTfRjkex+tX/ABr4vk8bX0AhhMOmWr5hSQfMzdifauMiuP7O1ieGUMYXY7kPQ88Gt0yOwjbEf7wZGT0A6cV2zquMbI+coYKFWq6stWtGjX8EeM7Twjq17b6ojJZXi8zxruKsPb0rE8Sa63ivxI1+4aOBDstoifup61QmTe43hSp+XC8tn69qb5FxCAXVd5Oc1Xtv3fKQ8HyV3UtdXN2KKMJuDHav3Tu4H1qnELnWbw2tgPkQZa4YYVfxrHvL7cjQwMFQjEjZ4J9qU6zNBYCyt5CkPGVHU/U1OGwicuao7HRj84bpqjQ0XU9N8PeE9L0pTNLJDfXh+ZizA7fwrcnu1jiLPJHGmMLh+n+FeDrfXKTebHcTJJ03Kx6U+SW9uVxJLcMmerMQprtjTpp9XY8J1XutGdn4q8T28yjT7S4yxf8AeSDofb6+9Z2q6TDqMUdysoiuBGAwz97FcvCkn2oJFD5svTywNxP0rq9O8M+K9SlGywMMePvTDbge1dEcbhqcWsRKyMpQqT+E5wf2hYty0sKg/wDLPpVyPWb6c+QVNxM/ChR976iu2t/hfezSK2r6qDGOSkQz+vaum0zwzpOhkGztt0/aWQ7jXi1s/wAPRbWHk2dtHLalX+Icz4U8HLp6x6lqgLXL/Olv2j9z6117MSTkgk/NxwKlfJySdxzzn+npURBwRjPct3/+vXy2IxVTEz56j/4B9LhqMKMFGCMeQboP9aI8dZC+CB3ANVbfUXtxdLcQszJyhB3l19etXkwVIkUOjcEY6fUdqhXRrDz/ADhE5lxtB8w4x/sjvXo0a9JUnSqInFYaq63tqb1tbUhk1Zsxy23KqN2Pvbvx/pVUR3uukfv/AN074CE7QAOxHrW9b2tvC0zJCib+ZM8qD/T8KmhtYUuZLofLM/UAfL9VHSsXiaUNKcde7I9hVbvOYyy0mys2/dwh5JByZOQD7UureKtJ8P4W+mLznBEMQywHp7VU8Sa9/wAI/o5uUGbidtkA6gH1PpTfCPgSCGSPXPEEgu9Ql/exR7twH1pUML7eDrYh6fmcmKxDpe5S3LEniXVfsgvrbwtcS2RO7zHyG2+uO9Qt8UtNhjydIvhzgKyEEtXoD3hLLhtueig/KPb/AOtVOaO2kkYtaxF+d2YxzTjhsPN2lT/E4pVKj+0cVH8XdHRgtxpl5Cw5OVziuk0b4heF9ZYRR6ksEz9EmG38Oaik07SZkEjWEThXO3d0z/WsvVfDmhagpNzYRR85DRYQqfqK6P7FwlVe6nF+plKdRdUekRR8K3ylG5Vl5BqZo0lR45VV45FKuD0IPH9a8Wgk8SeCJmm0m7N/pmdz2c5y4X1Br0rwp4y0nxbExs28q6QfvLWU4dfp6ivGx2T18J761XdE+159GePT6efBPxDvdLk+WxvUIQk8Mh6frVbynt5vs7MqxxHaT6nrW/8AHWJRrOkz8gmHG4dc1wtld3toiGeLzo5VDAt3X/Gvq6MpYrCRqHblOJjRxDhPZmndRfv/AJGPz4ZT9O1RWupLcalKkgZVUcA9TTo51nkGHkjJ5CFelZNgpn1qeRtzNGeKIwUou57FfFOFaEqe0nsWNUsvtVzI20ncByOtWbKwuobaMpKrOOMOOgq3aou65LPliwIJ7H2qSKI7JPMkZuckg44qZVWly9jooYOnKq6zWrvsQQWRgDTF4zKX3Adqj1hJJ9Ia9QbLUSbDIerHHQVdsrY3Uy21uPnzguTwi92JrJ8T65HfyQaZpsY/s60P7lR1JHUn15zW+Gpuc1KR5ubYtUaXsKT33/rzOcAwqsybQe3tT0EJ58xgo9uKtwyxySyT3uCFXARB/F6V6h4H+FMV1FDq+vjdBIN8FiOCV7EmunF4ilg6Xtaj07Hy8FKbOM8J+Bb/AMVTSNZS+TAP+W80fyH2Fdh/wpu7eJRca7hQOURM162kEFtapBbwRwQoMCNFwBUTAAfdB96+OxHEeJnNql7sTup4WNveOY8P+DdF8LQobeBZ7rHNxKufyrXlMjkhnOO3P+cVZl4UgAEenrVVs5/wryKlarWlzVJXPQpRUdEipKCoxkH6d/8AGqkpAGfTtirb7SxXt2+tVZCQoI4IPINXC530yo3JwSATyBio2IKjsO/uf6VJITu6cdQTUZPPTk9R1P5V0o6YmUmdgJHI7Z5/OrKj5Qxzk8f/AK6rxjCKDyG7dvxqdNw5Q5HQnvj29q65anVMnXtkE46f59KlQbySdp3dz0qGMkAKuMDoB0qaMqGOM4PXH9fasJGLOO+JVuz6Ja3a5Jik5zXT6R4s0m20DTRd6gkcwtxv7n6VleN4jL4PucrlkYHA6AZryy1k2gBguM5BPIxX1GTUoYigoS6M+XzOUqVe8ep9DWmqW1/apPZ3STx46oclfciqd7rdrZXltZvcIZZm+dAfmAPcV5PoeqPpGow3sWTGDtdBn7p6nFW7PQnm8eOkk7CMqblJGydy9cV6dTAKg1Z3RyLEcyL154o1fwpq93BPbm5sHl3KZBghe2CK39L8aaRrJVIbhobhhjZLgE+w9fxrQvVtb2ARXkKSQJgKjDt7H/GvM/Euh21re3H2RfLx8yL04+vrXRNcseZoIQnOTS33PR5pDuLYGF4Pp/wI/wBK5PVbG4t7mLV9Ina21CE7gUGAy+nuPrWfoPijzYUtNSm2zwjCTHqR/drXeTHHykE5K9UP1969Kjh4V6TTtZnLOo76nSafrOmfFbw1LourBLXXLZSUk6bmHcf4V5bDeT6XdvY3eyeKCQx+YO309quazBJa3S6pp5eGVeGYHA/CucQtK3LE7iSc9Sa8B4D6m5U4v3XsjooV5Rmpx3R1aXVstxIwvAQQNpYCobGzBurye2nR2k4Ug965osofpyvPNWkfEiyQExAjsehrJ0bXs9z2oZj7VrngtH08zVSe4tSXu7JpAMqzL3NNTW7NHcrG4jY8Bj0NFnrJt28u7BcNwG9TVuRdOF0stykSQiIsM87mHQYFQqalLlkjplinCh7SjU26NamLPqTuJhbsY0m4bDYwvpVOOU28DeWQob5S5HQVP5to8rzNFsQ/cjHU+9dT4I07w9dXjalr93vjgOYbCJCWkI9a7Zy9jC/Y+anOVWbk+o7wF4B1HxNqVve3Fu0OkxOHeVxjzsdlHrX0Q20DYqDy1AC/Qfyrm7TxlA8CJbeH9QjhVcqo2qqj2pkfjvQHDC5mmsivG2dCefw7V8Xmv1zFzvODUVsjpopQN9yMkD5hUEhOT29qWK4t7yETWtxFNEwyGjbOPw61FI3Hop49z718/KEk7NanZBp7EMnJwO3+eKqyHaOKsORtJHQevT8arOc45Jz09fw9q0gjqgiswwzevWqkjEjHHvmrTtjIwPqelUpTuI3AjI6mumB2U0RHOAecZ49agfuDye9TMT1PVfSoW6ngYbn/APXXTE6YozVHy4AKsMd6nBAAwPlI5HvUC8qDwcZA4qVGGcH72OfWuqR0yROrE4B+8B19B/WplIGNp4P6/wCH41ACDtIxzwOen+FSpyrAZJH3iev/ANesZIykiWRIp4ZIpkDxuNrqeQR7+v4V5p4z8JpoypqOn7nspGwyn/lmf6CvS48fLzu44x/nilmt4by3ltp0DQyjDjGQPfHrXRg8ZPDTun7vVHBjMPGtC3U8KW8mhZmViUxjcR29K6nQtT1S4VZYESSaMbUYsNyr6CqWs+Hbvw7fyJLF9o06Q/JIOg9ie1VNPtGhuxdQXPk7TnbnIr7aniYOmpp3X5HzUcJVc+SK1O1h1eSOZ49TVrdJPulh8uf61l3FwbyaWO6J3n5k/wBlfaopphqVty7zuoJCZ+6fassXxtybW7+V2IxJ12iufGYpYiPJTVj3cHg44OXPWle6+SIotEhvLWR1d0uo3OM/dYVNY3t1ZoILrcXRtqn0H1pouWttV8xifKkXY5B71duY0mwH5wcg172XQVSmqkPiW581jl7OtKHToWGxPGUYBkkHauSuYXgvHiHylWyDXUW++ONFPJUcmsvXof8AV3Q57OQK3zOg6lLnW6OahUcZFaCTzIwzIjKWwRjqaFtnW5ePG2Nh1I6fjWtoNvHc6OyDAcuSrU+K3ld5IXilMgPEfZvfNeDiMHWpqLirqSue7g6tKqrVHZo5+SylGSrB0PSo7a2uL25S1tYmlnJwFznH49q2G06d9QGnwSBn/wCWrjpGD2+td3oun2WiQBLSMByvzTMMkmnSw02ryRyV5U3JqBnaD8P7SBUn1qZpZM5+zp90ex9a7W2+w6VAghhhs0HQqoJxWXcana6VD515ciOPH3ScufoKz9H8Vabr16bOKCQyAZDSDORTqUHsyYyitDSude0V5Xtri4nIZwQ69G9varE+jwTqwjuH8thlUwMAfX0rzzxzeWq3v2TT3K+WMXPl9M+ldX4Qv7260EPfMCQdsRHQIOgNYKi72CNS5gaiuo+Dr5dRsJWgIbcpiz5b+zV6F4Q8c23iq3khkhFvqcYzJEo+R/dapXaRX1tJazgNE6EbT6+oPavPvAVyuk/EGOKQsVYvAPp2z6152bZdSq0HUtqlua0qjjNI9vkdRklsEeg6VVkYZxggnkf57VNI4DYBztOMGqsj4YjOR1wK+Fij2qaI5Wxzkk1UduQOCO3NTSMfXpz9KqvjaeMr1+tdMEdsERljvx+DEVE2Adh6dV9qcSBj1PHPWo5ANuw9uldCSN4oz9x+ZmOeTu9v8alTtg4PVST1qDdgZ6gnGP8APSpM4JDYyOhA6fhXXJHU0TpjcSR8p+9x3qdT8oXJyPu4OKrKQAM5APbsfxqYHLBwQSvHTp9axkjGSLAfI7YJw3oPwqRTjGAcqflPSoh8wAUgg8k+v0qRG5/TkZH5etYyMmSlYriJo540kgfho2Xgn6VyWt/DqK5Dy6LO0Ev3vszH5T9K6wfewSRx171PG4OB90j071dLFVaDvB/I5K1CM9zxqdL/AEm58jUrdrOUDAcD5WpssC30JUjYOvmHqa9qu7O01G0a3vYFniIwd3Vfoa8/8QeBZ9NDXmkbp7VeXgZssg9R6ivbwuZ062kvdl+BzXnFck9YnGXFuJ7PbETGIRnB6uRUVtrTRsqXUW7AxuHWr0jxvLlny6EeWFHBPoar3Nl5rM0qhZWONqj7v4V7uFxc6EvdZx43BqsuaJfivYLjmGbBb+E96W+Qy20igFhjiuYdJIJyozuU8NT47u5RhiUge5yK9uOaKcHGa3PAlh3GR0Ph2T/Qdp6I5Fbkt40EEjg/Oq4TjqTXEWOpPYSu23KMSSPetuLWYZ2gQMFDMCwNdGGxFKVJRe5MotSuaGniKyAtnYC5uW8yaTPT2FW9R8SWulxlImE0wXEaqc4+prEm0dLq/e4lvQsO7dtU4OPY1kzJDd6s6WsZSBRwSeTiuavN4eDfKvI2pR9pJRiSxRX3iPVMtJukblmPARfYd66ljaaJp5stHdDeyDbNcMeSvt6VzdxLcW0C3EDFABsO0cgVW0qKS6vfNLM20Z3E/ermwdWFRpNXbNMVSlRk0y7JaxxBIgWcu4eQt1PNei2ssMdpELTHlOoG1T0Pv6Vwcl1G9yyLgybfmJ/kPSoPt81of3crIe6A/er0atGknppY5ac5K6Z6DdX6WduZnCkR84xgE/1rzBNTdfECarGDuFwJNq8cA9Kt6p4gnu7YQOcsOpz0Fangzwbd6zdRX9yDBYQuH3MP9aR/SvGzSvRpQs3pY66MZVJKx7ElwLqCK4CbVmQSc87Se1QO+CeOT2p7SKRkKVXosY4AHtVeRsFs4z2r8ysm9D6unCw1m7k8dMgcflUMn3tvPy9s8/nSnjjOC3Xnp+NRFhgt7YPp+VbRidEUNP3QdwwxwP8APaomO0kHg+hOaewUDaOnX6f41CxUH5Rk+44P+FbRRvG5m8Y2lupySR1qZcYAJ6Hke1U0YHytoLfIME/09anViVOc57gD5vxHau2SOq10iySQASTkHgY4x7+lTqwPKkj19/oe9VdwJUH/AICf8PWpVIDbehzk/wD1/SsJIzki1vxhu3bA6VIGG4Bere9Vo2O3HqeKlUrtI5wOtYyRg0WUzxjkL3qRXPUjGex/pUCk4AyM9wOpH0p+QRkke2DkCsnEyaLkbgYx19zU6S/PjkqOjEcn2x6VRBwAOvvUiy/l7c1lKJhKCOK8Z+FriO9k1DSrXfBMMzxRjJU+q+9cfESjN5qOJl+VTIcN9DXtqzOgDhiM457n615r8QkX/hJY3CqhMIJCDgnPWvoMuxs6lqM9+5ytOm7rY5Sa3jckFcZPzKD0PtVS10XUrvzTaWVxcQxk5eNMgfWtOSTy5pThslMSDHPsa9Z8CWT6X4TgRh5cly5mbJ6E9veu7F476rS50rvojlxFBVJKyPC7myu7IL9qtJoWf7plXG6qxyhLZwwOCPSvpbULOw1qze01C0SeFuTjqv49q8d8b+B4fDKJd2t8klrI37uFv9YM/wA/rSwGbU8RLkfuyPPrYWVNXRxzzSOQGkOAPXrVjT0ZzKYwcKMH2qOO0eTdn5VHT3rU0+3aGGR2YGJvvY6//Xr1KtVyW9y8JhpOd3oh1os8/mecf3bcFR39/pU6BLfT5FjZQsf3ZF6GkcblDEtGnQSdNw+naqs17CAY40wB0C/MGp4XEzozbXU68Vhqc6ShN6rqZ8M7QlpVwd/DZ7UYknLSbTt7uasw2TXEq7Lad93ISNCcn0roNN8F6zrch82E2Fmh58zg/l3oljIQg/aTsjzPqsm/c1Mfwxor65r0Nng+XG2+Zxz8vvXu2EihS3iCrFEAqqvTA71k6HoNj4csTDaqGeT/AFk5PLGr7M2SQRu7kDNfHZljVi6nu/Cj3cFhPYx97cJXyp5+XsT1/KoWbnDHHHWhmYtyw/Ac/h60wkliBnHfjn8u1cMVY9FRGnaRtORjoSP6UxiB/h60rEhQCTkHvUbNyTx9PT3rVI1SGHLAAHB65/pTGCnnccDqO/8A9ekY59Sf5ionYbsnHTg9h+NapGsUYthI5sLdi3Plr268VdQgOucnPTHUVl6DMZNGgdiSQCox7VoqQV2nBGc4I4zXfWVps3o60ovyROmTlflOD1H3amXkqOTnt/ntUAHy7h97+LP3vw7YqReVGMFRyM9j/jXPJDaLCSfKG4IXgntUqnIHXkZHrVcMMruLHPXP3v8ACpc5TOQUB4B6VjJGMkWFb5c8deo6VLnBCnP4iq8bkHkdf4jUiyHZtGP8+lZNGMkWFbgA8VImegPA6/Sq4/2fTvTw5GMAlunHas3G5m0TJICoOfkLYHrXn/jbN34iKK23YoQsOa7TUL+LTdOnvZGBWMHaB13V5/G00s0ckpUzSHzHPXAr08spuLdQiFJVZ2eyMfaWuxncR5qIxbg4yPzr3JXKogXAQKFA9sfpXi12FNxK3zSMJVZSOgOa9aS7jisVuZ5khiKBi7njp0q83jKpGHKjldPlqSu/6uy9PcRWdrJczvtiiG5nPp6V4rr+qyeJtZkv5MiAHbHu/hUdxXTeI/EceuwHS7FmWzY5aUj7+PT2rk5AgQbyEROF44f8P89a3yvCewXPL4n+CMp0nNX6EWxAvUsp6Hpn/CnqzTSKlvE89w3CCJThfrXU+FPCZu1Go6mNtuT+7iPV6723itrRcW1tFDxjAUEge9aYrMqdKTjFczKVOUloczpHgC0VYbrWpHnuXXcbZDhR9a6aHTdMgRRDp1vGFPHy5p/mMBgKOP7x/lTRLg5xjPp1rwa2JrVXeTNY0V1LO5U6JFGR0KoBj9KilmZm3O5J6g+tRNICMFevHHao2HOA/AHUdaxs38RrGmkSmUljj72OT2qLdlhuwc00vkYKgkdGpnbGPc4/rVqJqoj2bAIwB61ESGGOcdj6Um/LlwTkd+9MJXOfX06VSRaiK7ABiR7ZqF8H5ec45x1xTmYgkHP171AzYUoAmM/h9a2UTWKFLBRuByvQY5z/AFqL5gWUADPOT2pT13FuoxnuajOHTAbDA1pGJtFWOb0N3SylhIA8uRhzz3rXViQuCN+Dxnn86x7DdBqOoQYwAVIHpmtBSCApAAXt2NehiF+8ZeD96imi2hBGRnZ9O9SxyfMQBgAcg9qqxvxgsQT09amRtq5YDI/L/wCtXNKJcl3LKuTgNjB+76n6elSZI9ipween+NVkbcMFRzyPb61KCuCQDleP/wBVYyRlKJZBIIycjqKkDBuehqvHnO1TkEduv408Pk57L6H+RrNoxkiyBt4JJx79f8Kk3nb97aPUfyxVYZOUPQ85x/OnhssGx7AE9PpWbiZuJheLnf7LYwgfuXfLc9651DGboOu7cI8MldL4si83SA4BJjkDKfQe9csrSS3EhwqsmAWz1r28HZ0FYeGkozafVojnWR4ZBEQnz8L3p80l7qr28eoSbYoVCrGp+Vvc1ULGTUGiik3SA7iF6YrTVlmVYUzk8Z9K6pPlS0+ZNKjTr1HOXR7dyOR0jV0bEcMZ5ZR1+lS+HdL/ALX1MLIuYIjvc/3h2H1qjeTbH8hwDbRA7mPIJ7A13HhWy+yaIrkZkuvnJx91ewrHE1XRouS3ZliJc8+RdDfydoVF2hRhB/dFAyexwfU96iPGOT8vJ7Z+lGR1b+L07fUV85YFFLRD93yEt1HX2+vrSBhuGD8pH5/4VFv6NkfL/nj0oJJ+TGATkk/1oUS7aEjOA24HGOKGxjgYPsefzqLzEJ3DOBximMxA2kd84quUEiUvxnrnjdj+lNJIY4ABx0zz+dNZ8/NuPTrmo8gfLjBA3E9jTsWkOYjAHY00tgnJxxSFgxGQRuHft/jUDHJAU/dP4H/CtEi0rjmPGByDxmo3YEEnqvH+fWh5MFsggN/nmoi4OGB+72/wrVI1irCEsuDt6jjn/OKiJwMlsYPzHHT8O9LIcZHGGOf/ANdRl9oJYkn9R9K0ijaJjL/yMN9/1yX+VW4+QoPIwaKK7sT8Zlln8BerJ+2e4xirMYBlQEDBHPvRRXIzpmI3FvIw4YOAD3FWYuZHHbbnFFFZyMpbCoT9jLZO7eBnvipsD7RKmPlEeQOwPrRRWb3MmMV2+yxNuO4nBOeTViLm4VTyAOhoopPYzZDqIB0K4J5Ow815xp5LISSSfM6miivUy/8AgS9Tkn8RdiRVd3VQHKnLAc0i8W4I4O0nIoortkb4bf5lZvmSxB5DTfMD3+teoH5IVC/KFjGAOMUUVwZn9k4qX8VjhyVzzlc80kZJiLEksMgHvRRXiI6kOwMqMDBGSKhyfJznndjNFFUUhZODgdMdKaxPlI2TuJAz3ooqkMGUebKMDAXIFRoTutjnlnwfcelFFUUhZeGu8cbD8v8As/So2GJLfHG5Mt7n3ooq1saRKzE7JDk5B4PpTio3quBgx5I9T60UVpHY0RXHNsrHru61HKBukGONpNFFaI1if//Z'
    context = {
        'decks': decks,
        'b64_image': b64_image
    }

    return render(request, 'deck-select.html', context)

def filter_duplicate_printings(cards):
    filtered_cards = cards.values('title', 'version').annotate(
        title_count=Count('title'),
        version_count=Count('version')
    ).filter(
        title_count__gt=1,
        version_count__gt=1
    ).order_by('title')

    card_titles = [item['title'] for item in filtered_cards]
    card_versions = [item['version'] for item in filtered_cards]

    filtered_cards = cards.exclude(title__in=card_titles, version__in=card_versions)

    duplicate_instances = cards.filter(
        title__in=card_titles,
        version__in=card_versions
    ).distinct()[:1]

    cards = filtered_cards.union(duplicate_instances)
    
    return cards