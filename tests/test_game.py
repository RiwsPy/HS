from base.entity import Entity, Card
from base.enums import CardName, GOLD_BY_TURN, Race
from django.test import TestCase

class TestGame(TestCase):
    def setUp(self):
        pass

    def test_game_type_ban(self):
        g = Card(CardName.DEFAULT_GAME, type_ban=Race('BEAST').hex)
        self.assertEqual(g.type_ban, Race('BEAST').hex)
        """
        self.assertEqual(
            len(g.craftable_cards.exclude(synergy='BEAST')),
            len(g.craftable_cards)
        )
        """
