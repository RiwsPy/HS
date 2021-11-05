from utils import my_zone, controller, game
from game import Game
from enums import *
from entity import Entity
from db_card import CARD_DB
import pytest
from sequence import Sequence
from db_card import Meta_card_data, Card_data

# pytest --cov=../HS tests/test_v2.py
# 25% avec beaucoup de fichiers obsolètes

player_name = 'rivvers'
hero_name = CARD_DB[CardName.DEFAULT_HERO]
g = Game()


def test_enums():
    assert len(CARD_NB_COPY) == len(LEVELUP_COST)
    assert len(NB_CARD_BY_LEVEL) == LEVEL_MAX+1
    assert GOLD_BY_TURN[-1] == MAX_GOLD

@pytest.fixture()
def reinit_game(monkeypatch):
    def mock_choose_one_of_them(self, lst, pr):
        return hero_name
    monkeypatch.setattr(Entity, 'choose_one_of_them', mock_choose_one_of_them)

    g.party_begin(player_name, 'notoum')

"""
def test_game(monkeypatch):
    db = {
    "":{"general":General.NONE, 'synergy': Type.ALL},
    "GAME":{"general":General.GAME, 'synergy': Type.ALL},
    "HAND":{"general":General.ZONE, "synergy":Type.ALL, "zone_type":Zone.HAND},
    '100': {'level': 1, 'synergy': Type.ALL, 'name': 'minion_level1', 'general': General.MINION},
    '201': {'level': 2, 'synergy': Type.ALL, 'name': 'minion_level2', 'general': General.MINION},
    '402': {'level': 3, 'synergy': Type.ALL, 'name': 'minion_level3', 'general': General.MINION},
    '403': {'level': 4, 'synergy': Type.ALL, 'name': 'minion_level4', 'general': General.MINION},
    '504': {'level': 5, 'synergy': Type.ALL, 'name': 'minion_level5', 'general': General.MINION},
    '605': {'level': 6, 'synergy': Type.ALL, 'name': 'minion_level6', 'general': General.MINION},
    '106': {'level': 1, 'synergy': Type.ALL, 'name': 'minion_level1', 'general': General.MINION, 'ban':1},
    }
    def mock_card_db(*args, **kwargs):
        return Meta_card_data(Card_data(k, **v)
            for k, v in db.items())
    monkeypatch.setattr('entity.card_db', mock_card_db)

    g = Game()
    assert g.nb_turn == 0
    assert g.type_present != Type.NONE
    assert len(g.hand.entities) == LEVEL_MAX+1
    for nb, minions in enumerate(g.hand.entities[1:]):
        assert len(minions) == CARD_NB_COPY[nb+1]

"""

def test_all_in_bob(reinit_game, monkeypatch):
    player = g.players[0]
    assert len(player.bob.board.cards) == 0

    len_old_hand = len(g.hand.cards)
    with Sequence('TURN', g):
        len_new_hand = len(g.hand.cards)
        assert len_new_hand + NB_CARD_BY_LEVEL[player.level]*len(g.players) == len_old_hand
        assert len(player.hand.cards) == 0
        assert player.bob.board.size == 3

        monkeypatch.setattr('player.Player.can_buy_minion', lambda *args, **kwargs: True)
        crd = player.bob.board[0]
        crd.buy()
        assert player.bob.board.size == 2
        assert len(player.hand.cards) == 1

        player.all_in_bob()
        assert len(player.hand.cards) == 0

        g.all_in_bob()
        assert len_old_hand == len(g.hand.cards)

def test_game_hand(reinit_game):
    entity_level = 1
    entity = g.hand[entity_level][0]
    id = entity.dbfId
    assert entity.type == Type.MINION
    assert entity.level == entity_level
    assert entity.synergy & g.type_present != 0
    assert isinstance(entity, Entity)
    assert len(g.hand.cards.filter(dbfId=id)) == CARD_NB_COPY[entity_level]
    nb = 0
    for card_id in g.card_can_collect:
        if card_id.level == entity_level:
            nb += 1
    assert len(g.hand.cards_of_tier_max(
            tier_max=entity_level, tier_min=entity_level)) == \
                CARD_NB_COPY[entity_level]*nb

def test_minion(reinit_game):
    minion_id = 1915 # Baron
    entity_data = g.card_can_collect[minion_id]
    assert entity_data != None

    for minion in g.hand.entities[entity_data['level']]:
        if minion == minion_id:
            for data, value in entity_data.data:
                assert getattr(minion, data) == value
            break

def test_player(reinit_game):
    player = g.players[0]
    assert player.pseudo == player_name
    assert player.name == hero_name.name
    assert hasattr(player, 'hand')
    assert hasattr(player, 'board')
    assert player.level == 1
    player.level = LEVEL_MAX+32
    assert player.level == LEVEL_MAX

def test_board_bob(reinit_game):
    with Sequence('TURN', g):
        player = g.players[0]
        bob_board =  player.bob.board
        assert len(bob_board.cards) == NB_CARD_BY_LEVEL[player.level]
        old_len_bob_hand = len(g.hand.cards)
        bob_board.drain_minion()
        assert len(bob_board.cards) == 0
        assert len(g.hand.cards) == old_len_bob_hand + NB_CARD_BY_LEVEL[player.level]
        bob_board.fill_minion_battlecry()
        assert len(bob_board.cards) == NB_CARD_BY_LEVEL[player.level]
        for minion in bob_board.cards:
            assert minion.BATTLECRY
        old_bob_board = bob_board.cards[:]
        bob_board.freeze()
        for minion in bob_board.cards:
            assert minion.FREEZE
        bob_board.drain_minion()
        assert len(bob_board.cards) == NB_CARD_BY_LEVEL[player.level]
        assert old_bob_board == bob_board.cards
        player.level = 2
        bob_board.fill_minion()
        assert len(bob_board.cards) == NB_CARD_BY_LEVEL[player.level]
        assert old_bob_board == bob_board.cards[:len(old_bob_board)]

def test_play(reinit_game):
    player = g.players[0]
    with Sequence('TURN', g):
        assert player.gold == GOLD_BY_TURN[g.nb_turn]
        assert player.levelup_cost == LEVELUP_COST[player.level]-1
        nb_minions = len(player.bob.board.cards)
        player.gold = player.minion_cost
        assert len(player.hand.cards) == 0
        homoncule = player.bob.create_card(43121)
        homoncule.play()
        #assert player.bob.max_health == player.bob.health
        homoncule.buy()
        assert player.gold == 0
        assert homoncule in player.hand.cards
        assert player.bob.board.size == nb_minions
        homoncule.play()
        g.active_action()
        assert player.health + 2 == player.max_health
        assert homoncule not in player.hand.cards
        assert homoncule in player.board.cards
        assert len(player.board.cards) == 1

def test_play_2(reinit_game):
    player = g.players[0]
    card = player.hand.create_card_in(70143) # tranchebauge
    assert card.dbfId == 70143
    assert card.owner == player.hand
    assert card in player.hand.cards
    card.play()
    g.active_action()
    assert card in player.board.cards
    assert len(player.hand.cards) == 1
    assert card.can_attack
    card = player.hand.create_card_in(976) # chasse-marée
    card.play()
    card = player.hand.create_card_in(976) # chasse-marée
    card.play()
    g.active_action()
    lst = player.board.cards.exclude_hex(card, race=Race('ALL').hex-Race('MURLOC').hex)
    assert len(lst) == 3

def test_card_append(reinit_game):
    player = g.players[0]
    player.bob.board.fill_minion()
    card = player.bob.board[0]
    old_owner = card.owner
    old_len_old_owner = len(card.owner.cards)
    new_owner = player.hand
    old_len_new_owner = len(new_owner.cards)
    new_owner.append(card)

    assert card.owner == new_owner
    assert len(new_owner.cards) == old_len_new_owner+1
    assert len(old_owner.cards) == old_len_old_owner-1

def test_entity_reset(reinit_game):
    player = g.players[0]
    crd = player.hand.create_card_in(70143) # géomancien

    assert crd.attack == crd.dbfId.attack
    crd.attack += 2
    assert crd.attack == crd.dbfId.attack + 2

    for mechanic in state_list:
        assert getattr(crd, mechanic) == getattr(crd.dbfId, mechanic)

    crd.reset()
    assert crd.attack == crd.dbfId.attack
    for mechanic in state_list:
        assert getattr(crd, mechanic) == getattr(crd.dbfId, mechanic)

def test_append_action(reinit_game):
    player = g.players[0]
    assert not g.game.action_stack

    g.append_action(test_entity_reset, test=1)
    old_action_0 = g.action_stack[0]

    assert old_action_0[0][0] is test_entity_reset
    assert not old_action_0[0][1]
    assert old_action_0[0][2] == {'test': 1}

    g.append_action(test_entity_reset, player, test=32)
    assert old_action_0 == g.action_stack[1]
    assert g.action_stack[0][0][1] == (player,)

def test_fight_1_1(reinit_game):
    with Sequence('TURN', g):
        crd = g.players[0].hand.create_card_in(40425) # chat tigré
        crd.play()
        crd = g.players[1].hand.create_card_in(40425)
        crd.play()

    Sequence('FIGHT', g).start_and_close()
    winner = g.players[0].combat.winner
    damage = g.players[0].combat.damage
    assert winner is None
    assert damage == 0

def test_aura_1(reinit_game):
    player1 = g.players[0]
    with Sequence('TURN', g):
        crd = player1.hand.create_card_in(61061) # Forban
        crd.play()
        assert crd.attack == crd.dbfId.attack

        crd2 = player1.hand.create_card_in(680) # Capitaine des mers du sud
        crd2.play()
        g.active_action()
        assert crd2.attack == crd2.dbfId.attack
        assert crd.attack == crd.dbfId.attack+1
        assert crd.health == crd.dbfId.health+1

        player1.bob.board.drain_minion()
        crd = player1.board.create_card_in(736) # vieux troubloeil
        player1.board.create_card_in(736)
        assert crd.attack == crd.dbfId.attack + 1

def test_adjacent_neighbors(reinit_game):
    player = g.players[0]
    crd1 = player.board.create_card_in(41245)
    crd_test = player.board.create_card_in(41245)
    assert crd_test.adjacent_neighbors() == [crd1]
    crd2 = player.board.create_card_in(41245)
    assert crd_test.adjacent_neighbors() == [crd1, crd2]

def test_card_data(reinit_game):
    card_data = g.card_db[41245]
    crd = g.players[0].hand.create_card_in(41245)
    assert card_data.attack == crd.attack
    assert card_data.level == crd.level
    assert card_data.nb_copy == CARD_NB_COPY[crd.level]

def test_meta_card_data(reinit_game):
    crd1 = g.card_db[41245]
    crd2 = g.card_db[475]
    crd1.rating = 2
    crd2.rating = 1.1
    meta = Meta_card_data(crd1, crd2)
    meta.sort('rating')
    assert meta == [475, 41245]
    assert type(meta) is Meta_card_data
    assert type(meta[0]) is Card_data

