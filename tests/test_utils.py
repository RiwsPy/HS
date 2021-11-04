from utils import *
from game import Game
from enums import CardName
import pytest
from entity import Entity
from db_card import CARD_DB
from sequence import Sequence


player_name = 'rivvers'
hero_name = CARD_DB[CardName.DEFAULT_HERO]
g = Game()


@pytest.fixture()
def reinit_game(monkeypatch):
    def mock_choose_one_of_them(self, lst, pr):
        return hero_name
    monkeypatch.setattr(Entity, 'choose_one_of_them', mock_choose_one_of_them)

    g.party_begin(player_name, 'notoum')


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

def test_card_list_filter(reinit_game):
    db = Card_list()
    crd1 = g.create_card(41245) # chasseur rochecave
    db.append(crd1)
    crd2 = g.create_card(1281) # hyène charognarde
    db.append(crd2)
    assert db.filter(BATTLECRY=True) == [crd1]

def test_card_list_exclude(reinit_game):
    db = Card_list()
    crd1 = g.create_card(41245) # chasseur rochecave
    db.append(crd1)
    crd2 = g.create_card(1281) # hyène charognarde
    db.append(crd2)
    crd3 = g.create_card(2016) # Blondisseur dent-de-métal
    db.append(crd3)
    assert db.exclude(level=2, race='MURLOC') == [crd2]

def test_(reinit_game):
    crd1 = g.create_card(70114) # Esprit combatif
    print(crd1.race)
    assert 0 == 1
