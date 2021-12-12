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
        kwargs['race'] = Race(kwargs['race_id'])
        kwargs['rarity'] = kwargs['rarity_id']
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

    def __getattr__(self, attr) -> Any:
        return self.data.get(attr)

    def __getitem__(self, key) -> Any:
        print('__get__item', key)
        raise IndexError
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
        super().sort(key=lambda x: getattr(x, attr), reverse=reverse)

    def __getitem__(self, value) -> Any:
        # TODO problème de compatibilité avec random.shuffle ??
        if type(value) is Card_data:
            return value
        elif type(value) is str and value.isdigit():
            value = int(value)
        elif isinstance(value, slice):
            return super().__getitem__(value)

        if isinstance(value, int):
            try:
                return super().__getitem__(self.index(value))
            except ValueError:
                print('Meta_card_data __getitem__: unknow', value)
                raise ValueError

        print('strange value', value, type(value))

        return super().__getitem__(value)


class CardDB:
    _instance = None
    _types_ban = []
    _objects = Meta_card_data()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._types_ban = kwargs.get('types_ban', [])
            all_cards = Card.objects.exclude(synergy__in=cls._types_ban)
            db = Meta_card_data(
                Card_data(**card.__dict__)
                for card in all_cards
            )

            for card in db:
                for attr in dbfId_attr:
                    if getattr(card, attr, False):
                        card[attr] = db[getattr(card, attr)]

            cls.objects = db

            cls._instance = super().__new__(cls)
        return cls._instance

    def __getitem__(self, value):
        return self.objects[value]

    @property
    def objects(self):
        return self._objects
