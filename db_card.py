from enums import Race, LEVEL_MAX, Zone, Type, CARD_NB_COPY, state_list
from json import load
from types import GeneratorType
from typing import List, Any

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
        return f"{self.data.get('name')} (dbfId {self})"

    def __getattr__(self, attr):
        return self.data.get(attr)

    def __getitem__(self, key):
        return getattr(self, str(key))

    @property
    def level(self):
        return self.techLevel

    @property
    def nb_copy(self):
        return CARD_NB_COPY[self.level or 0]

    def items(self):
        return self.data.items()

    def get(self, attr, default=None):
        return self.data.get(attr,  default)


class Meta_card_data(List[Card_data]):
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], GeneratorType):
            list.__setitem__(self, slice(None), *args)
        else:
            list.__setitem__(self, slice(None), args)

    def sort(self, attr='', reverse=False) -> None:
        """
            sort IN place.
        """
        super().sort(key=lambda x: x[attr], reverse=reverse)

    def __getitem__(self, value) -> Any:
        # problème avec random.shuffle si dbfId <= len(self) ??
        if not isinstance(value, int):
            print(value)
            return super().__getitem__(value)
        try:
            return super().__getitem__(self.index(value))
        except ValueError:
            print('Warning', value, 'not in Meta_card_data')
            return super().__getitem__(value)

    """
    def filter(self, **kwargs):
        return self.__class__(card
            for k, v in kwargs.items()
                for card in self
                    if card[k] == v)

    def filter_hex(self, **kwargs) -> 'Meta_card_data':
        return self.__class__(card
            for k, v in kwargs.items()
                for card in self
                    if card[k] & v)
    """

    def filter(self, **kwargs) -> 'Meta_card_data':
        cards = self.__class__(*self)
        for k, v in kwargs.items():
            for card in cards[::-1]:
                if getattr(card, k) != v:
                    cards.remove(card)

        return cards

    def filter_hex(self, **kwargs) -> 'Meta_card_data':
        cards = self.__class__(*self)
        for k, v in kwargs.items():
            for card in cards[::-1]:
                if not getattr(card, k) & v:
                    cards.remove(card)

        return cards

    def exclude(self, *args, **kwargs) -> 'Meta_card_data':
        # kwargs : OR relation
        cards = self.__class__(card
            for card in self
                if card not in args)

        for k, v in kwargs.items():
            for card in cards[::-1]:
                if getattr(card, k) == v:
                    cards.remove(card)

        return cards

    def exclude_hex(self, *args, **kwargs) -> 'Meta_card_data':
        cards = self.__class__(card
            for card in self
                if card not in args)

        for k, v in kwargs.items():
            for card in cards[::-1]:
                if getattr(card, k) & v:
                    cards.remove(card)

        return cards

    """
    def exclude(self, *args, **kwargs) -> 'Meta_card_data':
        copy = self.__class__(card
            for card in self
                if card not in args)
        if kwargs:
            return self.__class__(card
                for k, v in kwargs.items()
                    for card in copy
                        if card[k] != v)
        return copy

    def exclude_hex(self, *args, **kwargs) -> 'Meta_card_data':
        copy = self.__class__(card
            for card in self
                if card not in args)
        if kwargs:
            return self.__class__(card
                for k, v in kwargs.items()
                    for card in copy
                        if not card[k] & v)
        return copy
    """

    def filter_maxmin_level(self, level_max=LEVEL_MAX, level_min=1) -> 'Meta_card_data':
        return self.__class__(card
            for card in self
                if level_min <= card.level <= level_max)

def charge_all_cards(db_filename='db/HStat.json') -> Meta_card_data:
    db = Meta_card_data()

    with open(db_filename, "r", encoding="utf-8") as file:
        # normalization
        for value in load(file):
            value['type'] = getattr(Type, value.get('type', 'DEFAULT'))
            value['zone_type'] = getattr(Zone, value.get('zone_type', 'DEFAULT'))
            value['synergy'] = Race(value.get('synergy', 'ALL'))
            value['race'] = Race(value.get('race', 'DEFAULT'))
            value['type'] = Type(value.get('type', 'DEFAULT'))
            if 'mechanics' not in value:
                value['mechanics'] = []
            for mechanic in state_list:
                value[mechanic] = mechanic in value['mechanics']

            db.append(Card_data(**value))
    return db

CARD_DB = charge_all_cards()
