from django.urls import reverse, reverse_lazy
from rest_framework.test import APITestCase
from json import load, dumps
from card.models import Card

class TestdbfId(APITestCase):
    #url = reverse('cards')
    url = reverse_lazy('cards-list')

    def test_get_card(self):
        with open('card/mock_HStat.json', 'r') as file:
            data = load(file)
        for card in data:
            Card.objects.create(**card)
        minion = Card.objects.get(pk=976)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        for key, value in response.json()['results'][0].items():
            if key not in ('date_created', 'date_updated'):
                self.assertEqual(getattr(minion, key, None), value)

    def test_create(self):
        category_count = Card.objects.count()
        response = self.client.post(self.url, data={'name': 'Nouveau minion'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Card.objects.count(), category_count)
