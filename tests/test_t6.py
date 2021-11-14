import pytest
from entity import Card
from enums import CardName, ADAPT_ENCHANTMENT
from db_card import CARD_DB
from sequence import Sequence
from game import Game


player_name = 'p1_name'
hero_name = CARD_DB[CardName.DEFAULT_HERO]
g = Card(CardName.DEFAULT_GAME, is_test=True)

@pytest.fixture()
def reinit_game(monkeypatch):
    #TODO: génère bug dès qu'une carte utilise cette méthode... !
    def mock_choose_champion(*args, **kwargs):
        return hero_name
    monkeypatch.setattr(Game, 'choose_champion', mock_choose_champion)

    g.party_begin(player_name, 'p2_name')

def test_amalgadon(reinit_game):
    p1 = g.players[0]
    with Sequence('TURN', g):
        aml = p1.hand.create_card_in(61444)
        aml.play()
        aml2 = p1.hand.create_card_in(61444)
        aml2.play()

        assert len(aml.entities) == 0
        assert len(aml2.entities) == 1
        assert aml2.entities[0].dbfId in ADAPT_ENCHANTMENT
