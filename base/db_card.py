from .enums import Race, Zone, Type, CARD_NB_COPY, state_list
from json import load
from typing import List, Any
from .utils import Card_list
import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_battlegrounds.settings')
django.setup()
from card.models import Card

col_to_attr = {
    'enchantment_dbfId': 'enchantmentDbfId',
    'repop_dbfId': 'repopDbfId',
    'premium_dbfId': 'battlegroundsPremiumDbfId',
    'normal_dbfId': 'battlegroundsNormalDbfId',
    'power_dbfId': 'powerDbfId',
}

class Card_data(int):
    def __new__(cls, **kwargs):
        return super().__new__(cls, kwargs['dbfId'])

    def __init__(self, **kwargs) -> None:
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
        # problème avec random.shuffle si dbfId <= len(self) ??
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
    db = Meta_card_data()

    for card in Card.objects.all():
        value = card.__dict__.copy()
        del value['_state']
        value['type'] = Type(getattr(Type, value['type']))
        value['synergy'] = Race(value['synergy'])
        value['race'] = Race(value['race'])
        for mechanic in state_list:
            value[mechanic] = False
        for mechanic in value['mechanics']:
            value[mechanic] = True

        db.append(Card_data(**value))

    for card in db:
        for k, v in col_to_attr.items():
            if getattr(card, v, False):
                card[k] = db[getattr(card, v)]
                del card.data[v]

    return db

CARD_DB = charge_all_cards()
