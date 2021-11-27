import pytest
from base.entity import Card
from base.enums import CardName
from base.sequence import Sequence
from game import Game


player_name = 'p1_name'
g = Card(CardName.DEFAULT_GAME, is_test=True)
hero_name = g.all_cards[CardName.DEFAULT_HERO]

@pytest.fixture()
def reinit_game(monkeypatch):
    def mock_choose_champion(*args, **kwargs):
        return hero_name
    monkeypatch.setattr(Game, 'choose_champion', mock_choose_champion)

    g.party_begin(player_name, 'p2_name')


def test_murozond(reinit_game):
    p1, p2 = g.players
    with Sequence('TURN', g):
        crd = p1.draw(60637) # Murozond
        crd.play()
    assert p1.hand.size == 0
    Sequence('FIGHT', g).start_and_close()
    with Sequence('TURN', g):
        crd = p2.draw(60637) # Murozond
        crd.play()
        assert p2.hand.size == 1
        assert p2.hand.cards[0].dbfId == 60637
        """
        p2.hand.cards[0].play()
        assert p2.hand.size == 1
        assert p2.hand.cards[0].dbfId == 60669 # Murozond premium
        p2.hand.cards[0].play()
        assert p2.hand.size == 0 # golden murozond can't create himself
        """
