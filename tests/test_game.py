from base.enums import CardName
from game import Game
from django.test import TestCase
from json import load
from card.models import Card as DbCard

"""
class TestGame(TestCase):
    def setUp(self):
        with open('tests/HStat_mock.json', 'r') as file:
            data = load(file)
        for card in data:
            DbCard.objects.update_or_create(**card)

    def test_game_types_ban(self):
        g = Game(CardName.DEFAULT_GAME, types_ban=['BEAST'])
        assert g.types_ban == ['BEAST']
        assert len(g.all_cards.filter(synergy='BEAST')) == 0
"""