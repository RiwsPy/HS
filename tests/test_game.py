from base.entity import Entity, Card
from base.enums import CardName, Race
from django.test import TestCase
from json import load
from card.models import Card as DbCard

class TestGame(TestCase):
    def setUp(self):
        with open('tests/HStat_mock.json', 'r') as file:
            data = load(file)
        for card in data:
            DbCard.objects.create(**card)

    def test_game_test(self):
        self.assertEqual(1, 1)

    def test_game_type_ban(self):
        g = Card(CardName.DEFAULT_GAME, types_ban=['BEAST'])
        self.assertEqual(g.type_ban, Race('BEAST').hex)
        self.assertEqual(
            len(g.craftable_cards.filter(synergy='BEAST')),
            0
        )
