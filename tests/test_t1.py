import pytest
from entity import Entity, Card
from enums import CardName
from db_card import CARD_DB
from sequence import Sequence


player_name = 'p1_name'
hero_name = CARD_DB[CardName.DEFAULT_HERO]
g = Card(CardName.DEFAULT_GAME)

@pytest.fixture()
def reinit_game(monkeypatch):
    #TODO: génère bug dès qu'une carte utilise cette méthode... ! (battlecry ciblé..)
    def mock_choose_one_of_them(*args, **kwargs):
        return hero_name
    monkeypatch.setattr(Entity, 'choose_one_of_them', mock_choose_one_of_them)

    g.party_begin(player_name, 'p2_name')

def test_chat(reinit_game):
    crd = g.players[0].hand.create_card_in(40426) # Chat de gouttière
    assert g.players[0].hand.size == 1

    crd.play()
    assert g.players[0].hand.size == 0
    assert g.players[0].board.size == 2


def test_elemenplus(reinit_game):
    crd = g.players[0].hand.create_card_in(64038) # Element Plus
    assert g.players[0].hand.size == 1

    crd.play()
    assert g.players[0].hand.size == 0

    crd.sell()
    assert g.players[0].hand.size == 1
    assert g.players[0].hand[0].dbfId == 64040

def test_micromomie(reinit_game):
    with Sequence('TURN', g):
        crd1 = g.players[0].hand.create_card_in(53445)
        crd1.play()
        crd2 = g.players[0].hand.create_card_in(53445)
        crd2.play()

    assert crd1.attack == crd1.dbfId.attack +1
    assert crd2.attack == crd2.dbfId.attack +1

def test_bronzecouenne(reinit_game):
    crd = g.players[0].hand.create_card_in(70147) # Element Plus
    assert g.players[0].hand.size == 1

    crd.play()
    assert g.players[0].hand.size == 0

    crd.sell()
    assert g.players[0].hand.size == 2
    assert g.players[0].hand[0].dbfId == CardName.BLOOD_GEM

def test_tisse_colere(reinit_game):
    with Sequence('TURN', g):
        tisse = g.players[0].hand.create_card_in(59670) # Tisse-colère
        demon = g.players[0].hand.create_card_in(74910) # Diablotin dégoûtant
        tisse.play()
        demon.play()
        assert tisse.attack == tisse.dbfId.attack + 2
        assert g.players[0].health == 39

def test_forban(reinit_game):
    with Sequence('TURN', g):
        forb = g.players[0].hand.create_card_in(61061) # Forban
        forb.play()
    with Sequence('FIGHT', g):
        forb.die()
        assert g.players[0].board.size == 1
        assert g.players[0].board[0].dbfId == 62213

def test_hyene(reinit_game):
    with Sequence('TURN', g):
        hye = g.players[0].hand.create_card_in(1281) # Hyène charognarde
        hye.play()
        cat = g.players[0].hand.create_card_in(40426) # Forban
        cat.play()
    with Sequence('FIGHT', g):
        cat.die()
        assert g.players[0].board[0].attack == 4
        assert g.players[0].board[0].max_health == 3

def test_chromaile(reinit_game):
    with Sequence('TURN', g):
        chro = g.players[0].hand.create_card_in(74659) # chromaile évolutive
        chro.play()
        g.players[0].levelup()
        assert chro.attack == 2


"""
def test_chasseur_rochecave(reinit_game):
    mur1 = g.players[0].hand.create_card_in(41245)
    mur2 = g.players[0].hand.create_card_in(41245)
    mur1.play()
    mur2.play()
    assert mur2.attack == mur2.dbfId.attack
    assert mur1.attack == mur1.dbfId.attack +1
    assert mur1.max_health == mur1.dbfId.health +1
"""

#TODO test dragonnet ? anomalie... ?


def test_poisson(reinit_game):
    with Sequence('TURN', g):
        fish = g.players[0].hand.create_card_in(67213) # Poisson
        fish.play()
        fish2 = g.players[0].hand.create_card_in(67213) # Poisson
        fish2.play()
        forb = g.players[0].hand.create_card_in(61061) # Forban
        forb.play()

    with Sequence('FIGHT', g):
        forb.die()
        assert g.players[0].board.size == 3
        assert len(fish.entities) == 1
        fish.die()
        assert g.players[0].board.size == 3
        assert len(fish2.entities) == 2
