from .enums import Race, Zone, Type, CARD_NB_COPY, state_list, dbfId_attr
from typing import List, Any
from .utils import Card_list
import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_battlegrounds.settings')
django.setup()
from card.models import Card


class Card_data(int):
    def __new__(cls, **kwargs):
        return super().__new__(cls, kwargs['dbfId'])

    def __init__(self, **kwargs) -> None:
        try:
            del kwargs['_state']
        except KeyError:
            pass

        kwargs['dbfId'] = self
        kwargs['type'] = Type(kwargs['type'])
        kwargs['synergy'] = Race(kwargs['synergy'])
        kwargs['race'] = Race(kwargs['race'])
        for mechanic in state_list:
            kwargs[mechanic] = False
        for mechanic in kwargs['mechanics']:
            kwargs[mechanic] = True
        self.data = kwargs

        self.value = 0
        self.all_rating = {}
        self.rating = -999
        self.counter = 0
        self.esp_moy = 0

        self.counter_2 = 0
        self.value_2 = 0
        self.T1_to_T3_rating = -999

    def __repr__(self) -> str:
        return self.name

    def __getattr__(self, attr):
        return self.data.get(attr)

    def __getitem__(self, key):
        return getattr(self, str(key))

    def __setitem__(self, key, value) -> None:
        self.data[key] = value

    def __iter__(self):
        yield from (k for k in self.data)

    @property
    def level(self) -> int:
        return self.techLevel

    @property
    def nb_copy(self) -> int:
        return CARD_NB_COPY[self.level]

    def items(self):
        return self.data.items()

    def get(self, attr, default=None):
        return self.data.get(attr, default)

    @property
    def __dict__(self) -> dict:
        return self.data

class Meta_card_data(Card_list):
    def sort(self, attr='', reverse=False) -> None:
        """
            sort IN place.
        """
        super().sort(key=lambda x: x[attr], reverse=reverse)

    def __getitem__(self, value) -> Any:
        # TODO problème avec random.shuffle si dbfId <= len(self) ??
        if isinstance(value, str):
            try:
                return super().__getitem__(self.index(int(value)))
            except ValueError:
                return super().__getitem__(self.index(value))

        if not isinstance(value, int):
            return super().__getitem__(value)
        try:
            value = super().__getitem__(self.index(value))
        except ValueError:
            #print('Warning', value, 'not in Meta_card_data ret:', super().__getitem__(value))
            return super().__getitem__(value)
        else:
            pass
            #print('pas warning', value)
        return value

def charge_all_cards() -> Meta_card_data:
    db = Meta_card_data(Card_data(**card.__dict__)
        for card in Card.objects.all())

    for card in db:
        for attr in dbfId_attr:
            if getattr(card, attr, False):
                card[attr] = db[card[attr]]

    return db

CARD_DB = charge_all_cards()
