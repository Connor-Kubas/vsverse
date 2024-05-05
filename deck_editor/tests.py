from django.test import TestCase
from django.urls import reverse
from core.models import Decks

# Create your tests here.
class EditorTests(TestCase):
    def test_increment_card_works(self):
        # create a deck
        deck_name = 'deck name test'
        deck_object = Decks(title=deck_name)
        # deck_object.user_id = '6a203065-ae0c-4e4b-a409-d163e73dee47'
        deck_object.save()

        url = reverse('increment', kwargs={"card": 0, "deck": 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
