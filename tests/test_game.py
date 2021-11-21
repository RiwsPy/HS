from base.entity import Entity, Card
from base.enums import CardName, Race
from django.test import TestCase
from json import load
from card.models import Card

class TestGame(TestCase):
    def setUp(self):
        with open('tests/HStat_mock.json', 'r') as file:
            data = load(file)
        for card in data:
            Card.objects.create(**card)

    def test_game_test(self):
        self.assertEqual(1, 1)

    """
    def test_game_type_ban(self):
        g = Card(CardName.DEFAULT_GAME, type_ban=Race('BEAST').hex)
        self.assertEqual(g.type_ban, Race('BEAST').hex)
        self.assertEqual(
            len(g.craftable_cards.exclude(synergy='BEAST')),
            len(g.craftable_cards)
        )
    """