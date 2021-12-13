from game import Game
import pytest
from base.entity import Card
from base.enums import CardName, GOLD_BY_TURN
from base.sequence import Sequence


player_name = 'p1_name'
g = Card(CardName.DEFAULT_GAME, is_test=True)
hero_name = g.all_cards[CardName.DEFAULT_HERO]


@pytest.fixture()
def reinit_game(monkeypatch):
    def mock_choose_champion(self, lst, pr):
        return hero_name
    monkeypatch.setattr(Game, 'choose_champion', mock_choose_champion)

    g.party_begin({player_name: 0, 'p2_name': 0})


def test_start_sequence(reinit_game):
    crd = g.players[0].draw(60055) # Micro-machine
    crd.play()
    Sequence('TURN', g).start_and_close()
    assert crd.attack == crd.dbfId.attack + crd.enchantmentDbfId.attack


def test_play_sequence(reinit_game):
    tisse = g.players[0].draw(59670) # Tisse-colère
    demon = g.players[0].draw(74910) # Diablotin dégoûtant
    tisse.play()
    demon.play()
    assert tisse.attack == tisse.dbfId.attack + 2


def test_battlecry_sequence(reinit_game):
    cat = g.players[0].draw(40426) # Chat de gouttière
    cat.play()
    assert g.players[0].board.size == 2


def test_die_sequence(reinit_game):
    with Sequence('TURN', g):
        cat = g.players[0].draw(40426) # Chat de gouttière
        cat.play()
        hye = g.players[0].draw(1281) # Hyène charognarde
        hye.play()
        assert g.players[0].board.size == 3
    with Sequence('FIGHT', g):
        cat.die()
        assert g.players[0].board.size == 2
        assert hye.attack == hye.dbfId.attack + 2


def test_avenge_sequence(reinit_game):
    with Sequence('TURN', g):
        cat = g.players[0].draw(40426) # Chat de gouttière
        cat.play()
        pote = g.players[0].draw(72055) # Pote à plumes
        pote.play()
    with Sequence('FIGHT', g):
        cat.die()
        assert g.players[0].board.cards[0].attack == g.players[0].board.cards[0].dbfId.attack +1

def test_frenzy(reinit_game):
    with Sequence('TURN', g):
        chof = g.players[0].draw(70157) # Chauffard huran
        chof.play()
        assert g.players[0].hand.size == 0
        assert chof.FRENZY is True
    with Sequence('FIGHT', g):
        chof.damage(chof, 1)
        assert g.players[0].hand.size == 1
        assert chof.FRENZY is False

        # once by battle
        chof.damage(chof, 1)
        assert g.players[0].hand.size == 1

def test_hit_by(reinit_game):
    with Sequence('TURN', g):
        chef = g.players[0].draw(2288) # Chef du gang des diablotins
        chef.play()
        assert g.players[0].board.size == 1
    with Sequence('FIGHT', g):
        chef.damage(chef, 1)
        assert g.players[0].board.size == 2
 
def test_reborn(reinit_game):
    with Sequence('TURN', g):
        aco = g.players[0].draw(63614) # Acolyte de C'thun
        aco.play()
    with Sequence('FIGHT', g):
        assert aco.REBORN is True
        aco.die()
        assert g.players[0].board.size == 1
        assert g.players[0].board.cards[0].health == 1
        assert g.players[0].board.cards[0].REBORN is False

def test_play_error(reinit_game):
    boss1 = g.players[0].draw(72065) # boss écailles-salines
    boss2 = g.players[0].draw(72065) # boss écailles-salines
    with Sequence('TURN', g):
        boss2.play()
    assert boss2.health == boss2.dbfId.health

def test_levelup(reinit_game):
    p1 = g.players[0]
    with Sequence('TURN', g):
        assert p1.level == 1
        assert p1.gold == 3
        p1.levelup()
        assert p1.level == 1
    with Sequence('TURN', g):
        assert p1.level == 1
        assert p1.gold == 4
        p1.levelup()
        assert p1.level == 2
        assert p1.gold == 0

def test_roll(reinit_game):
    p1 = g.players[0]
    with Sequence('TURN', g):
        old_bob_board = p1.bob.board.cards[:]
        assert p1.bob.board.size == 3
        roll_cost = p1.cost_next_roll
        p1.roll()
        assert p1.bob.board.cards != old_bob_board
        assert p1.gold == GOLD_BY_TURN[p1.nb_turn] - roll_cost


def test_brann(reinit_game):
    p1 = g.players[0]
    with Sequence('TURN', g):
        brann= p1.draw(2949) # Brann
        brann.play()
        assert p1.hand.size == 0
        geo= p1.draw(70143) # Géomancien de Tranchebauge
        geo.play()
        assert p1.hand.size == 2

        # check non cumul des effets
        brann= p1.draw(2949) # Brann
        brann.play()
        geo= p1.draw(70143) # Géomancien de Tranchebauge
        geo.play()
        assert p1.hand.size == 4

def test_khadgar(reinit_game):
    p1 = g.players[0]
    with Sequence('TURN', g):
        khad = p1.draw(52502) # Khadgar
        khad.play()
        forb = p1.draw(61061) # Forban
        forb.play()

    with Sequence('FIGHT', g):
        forb.die()
        assert p1.board.size == 3

def test_khadgar2(reinit_game):
    p1 = g.players[0]
    with Sequence('TURN', g):
        khad = p1.draw(52502) # Khadgar
        khad.play()
        mum = p1.draw(60036) # Maman ourse
        mum.play()
        cat = p1.draw(40426) # Chat de gouttière
        cat.play()

        assert p1.board.size == 5
        assert cat.position == 2
        assert cat.attack == cat.dbfId.attack +5
        assert p1.board.cards[cat.position+1].attack == cat.dbfId.attack +5
        assert p1.board.cards[cat.position+2].attack == cat.dbfId.attack +10


def test_roll(reinit_game):
    p1 = g.players[0]
    with Sequence('TURN', g):
        old_bob_board = p1.bob.board.cards[:]
        p1_gold = p1.gold
        p1.roll()
        assert p1.gold == p1_gold - p1.power.roll_cost
        assert old_bob_board != p1.bob.board.cards

        ano = p1.draw(64045) # Anomalie actualisante premium
        ano.play()

        for _ in range(ano.bonus_value):
            old_bob_board = p1.bob.board.cards[:]
            p1_gold = p1.gold
            p1.roll()
            assert p1.gold == p1_gold
            assert old_bob_board != p1.bob.board.cards

        old_bob_board = p1.bob.board.cards[:]
        p1_gold = p1.gold
        p1.roll()
        assert p1.gold == p1_gold-p1.power.roll_cost
        assert old_bob_board != p1.bob.board.cards

def test_modular(reinit_game):
    p1 = g.players[0]
    with Sequence('TURN', g):
        crd = p1.draw(53445) # Micromomie
        crd.play()
        enn = p1.draw(48993) # Ennuy-o-module
        enn.play(position=0)
        assert p1.board.size == 1
        assert crd.cards == [enn]
        assert crd.attack + crd.dbfId.attack + enn.dbfId.attack
        assert crd.max_health + crd.dbfId.health + enn.dbfId.health
        assert crd.DIVINE_SHIELD
        assert crd.TAUNT

        men = p1.draw(48536) # Menace répliquante
        men.play(position=0)
        assert crd.cards == [enn, men]

    with Sequence('FIGHT', g):
        crd.die()
        assert p1.board.size == 4
        """
        assert p1.board.cards[0].dbfId == 48842
        assert p1.board.cards[-1].dbfId == 53445
        old_size = p1.game.hand.size
        """

def test_give_golden_card(reinit_game):
    p1 = g.players[0]
    old_hand_len = g.hand.size
    with Sequence('TURN', g):
        p1.draw(65658) # Acolyte de C'thun
        assert p1.hand.size == 1
        assert g.hand.size == old_hand_len - len(g.players)*3 - 3


def test_discover(reinit_game):
    p1 = g.players[0]
    with Sequence('TURN', g):
        gue = p1.draw(60028) # Guetteur primaileron
        gue.play()
        assert p1.hand.size == 0
        gue2 = p1.draw(60028) # Guetteur primaileron
        gue2.play()
        assert p1.hand.size == 1
        assert p1.hand.cards[0].race.MURLOC
        assert p1.hand.cards[0].dbfId != gue2.dbfId

def test_draw(reinit_game):
    p1 = g.players[0]
    old_len_game_cards = len(g.hand.cards)
    p1.draw(60028) # Guetteur primaileron
    assert p1.hand.size == 1
    assert old_len_game_cards == len(g.hand.cards)+1

def test_triple(reinit_game):
    p1 = g.players[0]
    id = p1.draw(68469)
    id.play()
    id = p1.draw(68469)
    id.play()
    ench_data = g.all_cards[60644]
    p1.buff(id, 60644)
    p1.draw(68469)
    for card in p1.hand.cards + p1.board.cards:
        assert card.dbfId != 68469
    assert p1.hand.cards.filter(dbfId=id.dbfId.battlegroundsPremiumDbfId)
    assert p1.hand.cards[0].attack == p1.hand.cards[0].dbfId.attack + ench_data.attack
    p1.hand.cards[0].play()
    assert p1.hand.cards.filter(dbfId=59604)
    assert p1.hand.cards[0].quest_value == p1.level+1
    p1.hand.cards[0].play()
    assert p1.hand.cards[0].level == p1.level+1

def test_set_premium(reinit_game):
    # Phase I
    p1 = g.players[0]
    card = p1.draw(68469)
    premium_id = card.set_premium()
    assert card.dbfId == 68469
    assert premium_id.dbfId == card.battlegroundsPremiumDbfId
    assert premium_id.battlegroundsNormalDbfId == card.dbfId

    # Phase II
    premium_id.play()
    card1 = p1.draw(68469)
    card2 = p1.draw(68469)
    card1.play()
    card2.play()
    p1.buff(card1, 72191) # gemme de sang
    assert card1.position == 1
    assert card1.entities
    card1_premium = card1.set_premium()
    assert card1_premium.position == 1
    assert p1.board.cards == [premium_id, card1_premium, card2]
    assert card1 in card1_premium.cards
    assert card1_premium.entities
    assert card1_premium.attack == card1_premium.dbfId.attack + g.all_cards[72191].attack
