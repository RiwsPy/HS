import pytest
from game import Game
from entity import Entity, Card
from enums import CardName, GOLD_BY_TURN, Race
import db_card
from sequence import Sequence


@pytest.fixture()
def charge_init_db_card(monkeypatch):
    # non fonctionnel
    def charge_all_mock(*args, **kwargs):
        return db_card.charge_all_cards('tests/HStat_mock.json')
    monkeypatch.setattr(db_card, 'charge_all_cards', charge_all_mock)


def test_game_type_ban(charge_init_db_card):
    g = Card(CardName.DEFAULT_GAME, type_ban=Race('BEAST').hex)
    assert g.type_ban == Race('BEAST').hex
    assert len(g.craftable_card.exclude(synergy='BEAST')) == len(g.craftable_card)
