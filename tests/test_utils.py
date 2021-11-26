from base.utils import *
from base.enums import CardName
import pytest
from base.entity import Card
from base.sequence import Sequence
from game import Game


player_name = 'p1_name'
g = Card(CardName.DEFAULT_GAME, is_test=True)
hero_name = g.all_cards[CardName.DEFAULT_HERO]


@pytest.fixture()
def reinit_game(monkeypatch):
    def mock_choose_champion(self, lst, pr):
        return hero_name
    monkeypatch.setattr(Game, 'choose_champion', mock_choose_champion)

    g.party_begin(player_name, 'p2_name')


def test_utils(reinit_game):
    player = g.players[0]
    with Sequence('TURN', g):
        assert g.no_bob is False
        card = player.bob.board.cards[0]
        assert my_zone(card) is player.bob.board
        assert controller(card) is player.bob
        assert game(card) is g

def test_card_list_filter(reinit_game):
    db = Card_list()
    crd1 = g.create_card(41245) # chasseur rochecave
    db.append(crd1)
    crd2 = g.create_card(1281) # hyène charognarde
    db.append(crd2)
    assert db.filter(level=1, race='MURLOC') == [crd1]
    assert db.filter(BATTLECRY=True) == [crd1]
    assert db.filter(level=2) == []

def test_card_list_exclude(reinit_game):
    db = Card_list()
    crd1 = g.create_card(41245) # chasseur rochecave
    db.append(crd1)
    crd2 = g.create_card(1281) # hyène charognarde
    db.append(crd2)
    crd3 = g.create_card(2016) # Blondisseur dent-de-métal
    db.append(crd3)
    assert db.exclude(level=2, race='MURLOC') == [crd2]
