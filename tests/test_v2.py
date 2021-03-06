from base.enums import *
from base.entity import Card, Entity
import pytest
from base.sequence import Sequence
from base.db_card import Meta_card_data, Card_data
from game import Game


player_name = 'p1_name'
g = Card(CardName.DEFAULT_GAME, is_test=True)
hero_name = g.all_cards[CardName.DEFAULT_HERO]


def test_enums():
    assert len(CARD_NB_COPY) == len(LEVELUP_COST)
    assert len(NB_CARD_BY_LEVEL) == LEVEL_MAX+1
    assert GOLD_BY_TURN[-1] == MAX_GOLD

@pytest.fixture()
def reinit_game(monkeypatch):
    def mock_choose_champion(self, lst, pr):
        return hero_name
    monkeypatch.setattr(Game, 'choose_champion', mock_choose_champion)

    g.party_begin({player_name: 0, 'p2_name': 0})


def test_all_in_bob(reinit_game, monkeypatch):
    player = g.players[0]
    assert len(player.bob.board.cards) == 0

    len_old_hand = len(g.hand.cards)
    with Sequence('TURN', g):
        len_new_hand = len(g.hand.cards)
        assert len_new_hand + NB_CARD_BY_LEVEL[player.level]*len(g.players) == len_old_hand
        assert len(player.hand.cards) == 0
        assert player.bob.board.size == 3

        monkeypatch.setattr('base.player.Player.can_buy_minion', lambda *args, **kwargs: True)
        crd = player.bob.board.cards[0]
        crd.buy()
        assert player.bob.board.size == 2
        assert len(player.hand.cards) == 1

        player.all_in_bob()
        assert len(player.hand.cards) == 0

        g.all_in_bob()
        assert len_old_hand == len(g.hand.cards)

def test_game_hand(reinit_game):
    entity_level = 1
    for entity in g.hand[entity_level]:
        assert entity.type == Type.MINION
        assert entity.level == entity_level
        assert isinstance(entity, Card_data)
    assert len(g.hand.cards.filter(dbfId=entity.dbfId)) == CARD_NB_COPY[entity_level]
    for card in g.hand.cards:
        assert card.synergy not in g.types_ban
    nb = len(g.minion_can_collect.filter(level=entity_level))
    assert len(g.hand[entity_level]) == \
                CARD_NB_COPY[entity_level]*nb

def test_minion(reinit_game):
    minion_id = 1915 # Baron
    entity_data = g.minion_can_collect[minion_id]
    assert entity_data != None

    for minion in g.hand.entities[entity_data.level]:
        if minion == minion_id:
            for data, value in entity_data.items():
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
        bob_board.fill_minion()
        old_bob_board = bob_board.cards[:]
        bob_board.freeze()
        for minion in bob_board.cards:
            assert minion.FREEZE
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
    card = player.draw(70143) # tranchebauge
    assert card.dbfId == 70143
    assert card.owner == player.hand
    assert card in player.hand.cards
    card.play()
    g.active_action()
    assert card in player.board.cards
    assert len(player.hand.cards) == 1
    assert card.can_attack
    card = player.draw(976) # chasse-mar??e
    card.play()
    card = player.draw(976) # chasse-mar??e
    card.play()
    g.active_action()
    lst = player.board.cards.exclude(card).filter(race='MURLOC')
    assert len(lst) == 3

def test_card_append(reinit_game):
    player = g.players[0]
    player.bob.board.fill_minion()
    card = player.bob.board.cards[0]
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
    crd = player.draw(70143) # g??omancien

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
        crd = g.players[0].draw(40425) # chat tigr??
        crd.play()
        crd = g.players[1].draw(40425)
        crd.play()

    Sequence('FIGHT', g).start_and_close()
    winner = g.players[0].combat.winner
    damage = g.players[0].combat.damage
    assert winner is None
    assert damage == 0

def test_aura_1(reinit_game):
    player1 = g.players[0]
    with Sequence('TURN', g):
        crd = player1.draw(61061) # Forban
        crd.play()
        assert crd.attack == crd.dbfId.attack

        crd2 = player1.draw(680) # Capitaine des mers du sud
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
    card_data = g.all_cards[41245]
    crd = g.players[0].draw(41245)
    assert card_data.attack == crd.attack
    assert card_data.level == crd.level
    assert card_data.nb_copy == CARD_NB_COPY[crd.level]

def test_meta_card_data(reinit_game):
    crd1 = g.all_cards[41245]
    crd2 = g.all_cards[475]
    crd1.rating = 2
    crd2.rating = 1.1
    meta = Meta_card_data(crd1, crd2)
    meta.sort('rating')
    assert meta == [475, 41245]
    assert type(meta) is Meta_card_data
    for card in meta:
        assert type(card) is Card_data

