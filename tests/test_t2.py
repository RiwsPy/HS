import pytest
from entity import Card
from enums import CardName
from db_card import CARD_DB
from sequence import Sequence
from game import Game


player_name = 'p1_name'
hero_name = CARD_DB[CardName.DEFAULT_HERO]
g = Card(CardName.DEFAULT_GAME, is_test=True)

@pytest.fixture()
def reinit_game(monkeypatch):
    def mock_choose_champion(*args, **kwargs):
        return hero_name
    monkeypatch.setattr(Game, 'choose_champion', mock_choose_champion)

    g.party_begin(player_name, 'p2_name')


def test_gardien_glyphes(reinit_game):
    with Sequence('TURN', g):
        crd = g.players[0].hand.create_card_in(61029) # Gardien des glyphes
        crd.play()
        crd = g.players[1].hand.create_card_in(61029) # Gardien des glyphes
        crd.play()

    with Sequence('FIGHT', g):
        assert g.players[0].combat.winner


def test_saurolisque(reinit_game):
    with Sequence('TURN', g):
        crd = g.players[0].hand.create_card_in(62162) # Saurolisque
        crd.play()
        crd2 = g.players[0].hand.create_card_in(72042) # Saute-mouton
        crd2.play()

    assert crd.attack == 4
    assert crd.max_health == 4


def test_capitaine_mer_du_sud(reinit_game):
    with Sequence('TURN', g):
        forb = g.players[0].hand.create_card_in(61061) # Forban
        forb.play()
        cap = g.players[0].hand.create_card_in(680) # Capitaine
        cap.play()
        forb2 = g.players[0].hand.create_card_in(61061) # Forban
        forb2.play()
        assert forb.attack == forb.dbfId.attack+1
        assert forb2.attack == forb2.dbfId.attack+1
        assert cap.attack == cap.dbfId.attack

    with Sequence('FIGHT', g):
        cap.die()
        assert forb.attack == forb.dbfId.attack
        assert forb2.attack == forb2.dbfId.attack


def test_defense_robuste(reinit_game):
    p1 = g.players[0]
    with Sequence('TURN', g):
        rob = p1.hand.create_card_in(70162)
        rob.play()
        p1.buff(CardName.BLOOD_GEM_ENCHANTMENT, rob)
        assert rob.attack == rob.dbfId.attack +1
        assert rob.DIVINE_SHIELD == True

    with Sequence('TURN', g):
        assert rob.attack == rob.dbfId.attack +1
        assert rob.DIVINE_SHIELD == False


def test_saute_mouton(reinit_game):
    p1 = g.players[0]
    with Sequence('TURN', g):
        sheep = p1.hand.create_card_in(72042) # Saute-mouton
        sheep.play()
        sheep2 = p1.hand.create_card_in(72042) # Saute-mouton
        sheep2.play()
        yooh = p1.hand.create_card_in(61060) # Yo-oh ogre
        yooh.play()

    with Sequence('FIGHT', g):
        sheep.die()
        assert sheep2.attack == sheep2.dbfId.attack + sheep2.enchantment_dbfId.attack
        assert len(sheep2.entities) == 1

    with Sequence('TURN', g):
        sheep = p1.hand.create_card_in(72042) # Saute-mouton
        sheep.play()

    with Sequence('FIGHT', g):
        p1.board[0].die()
        p1.board[0].die()
        sheep = p1.board[1]
        assert len(sheep.entities) == 2
        assert sheep.attack == sheep.dbfId.attack + sheep.enchantment_dbfId.attack*2

