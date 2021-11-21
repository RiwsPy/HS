import pytest
from game import Game
from base.entity import Entity, Card
from base.enums import CardName, GOLD_BY_TURN, Race
import base.db_card
from base.sequence import Sequence


@pytest.fixture()
def charge_init_db_card(monkeypatch):
    # non fonctionnel
    def charge_all_mock(*args, **kwargs):
        return base.db_card.charge_all_cards('tests/HStat_mock.json')
    monkeypatch.setattr(base.db_card, 'charge_all_cards', charge_all_mock)


def test_game_type_ban(charge_init_db_card):
    g = Card(CardName.DEFAULT_GAME, type_ban=Race('BEAST').hex)
    assert g.type_ban == Race('BEAST').hex
    assert len(g.craftable_cards.exclude(synergy='BEAST')) == len(g.craftable_cards)
