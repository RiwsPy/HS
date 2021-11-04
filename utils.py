from enums import Type, LEVEL_MAX, VERSION, Race
import json
from types import GeneratorType
import random

def game(self):
    ret = self
    while ret.type > Type.GAME:
        ret = ret.owner
    if ret.type == Type.GAME:
        return ret
    return None

def controller(self):
    ret = self
    while ret.type > Type.HERO:
        ret = ret.owner
    return ret

def my_zone(self):
    ret = self
    #while ret.type > Type.ZONE:
    while ret.type not in (Type.ZONE, Type.GAME):
        ret = ret.owner
    if ret.type == Type.ZONE:
        return ret
    return None


class Card_list(list):
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], GeneratorType):
            list.__setitem__(self, slice(None), *args)
        else:
            list.__setitem__(self, slice(None), args)

    def __getitem__(self, value):
        if isinstance(value, slice):
            return self.__class__(*super().__getitem__(value))
        return super().__getitem__(value)

    def filter(self, **kwargs) -> 'Card_list':
        cards = self.__class__(*self)
        for k, v in kwargs.items():
            for card in cards[::-1]:
                if getattr(card, k) != v:
                    cards.remove(card)

        return cards

    def filter_hex(self, **kwargs) -> 'Card_list':
        cards = self.__class__(*self)
        for k, v in kwargs.items():
            for card in cards[::-1]:
                if not getattr(card, k) & v:
                    cards.remove(card)

        return cards

    def exclude(self, *args, **kwargs) -> 'Card_list':
        # kwargs : OR relation
        cards = self.__class__(card
            for card in self
                if card not in args)

        for k, v in kwargs.items():
            for card in cards[::-1]:
                if getattr(card, k) == v:
                    cards.remove(card)

        return cards

    def exclude_hex(self, *args, **kwargs) -> 'Card_list':
        cards = self.__class__(card
            for card in self
                if card not in args)

        for k, v in kwargs.items():
            for card in cards[::-1]:
                if getattr(card, k) & v:
                    cards.remove(card)

        return cards

    def filter_maxmin_level(self, level_max=LEVEL_MAX, level_min=1) -> 'Card_list':
        return self.__class__(card
            for card in self
                if level_min <= card.level <= level_max)

    def one_minion_by_type(self) -> 'Card_list':
        """
            Return a list which contains until one minion by type
        """
        #TODO: gestion des Race.ALL incorrecte sur le fond
        # exclu de fait les minions multi-type
        tri = {minion_race: self.filter(race=minion_race)
            for minion_race in Race.battleground_race()}

        result = Card_list(random.choice(minions)
                for minions in tri.values()
                    if minions)

        return result + self.filter(race=Race.ALL)



class Board_Card_list(Card_list):
    def __getitem__(self, value):
        try:
            return super().__getitem__(value)
        except IndexError:
            return None

class db_arene(dict):
    filename = 'db/arene_minion.json'

    def __init__(self, version=VERSION, type_ban="0", **kwargs):
        with open(self.__class__.filename, 'r') as file:
            data = json.load(file)
        type_ban = str(type_ban)
        if version not in data:
            data[version] = {}
            data[version][type_ban] = {}
        elif type_ban not in data[version]:
            data[version][type_ban] = {}
        self.data = data
        self.version = version
        self.type_ban = type_ban

        super().__init__(data[version][type_ban])

    def init_minion(self, minion):
        try:
            ret = self[minion]
        except KeyError:
           self[minion] = {'name': minion.name, 'rating': {}}
           ret = self[minion]
        return ret

    def search(self, minion='', **kwargs) -> dict:
        return self[minion]

    def search_minion_rate(self, minion, method) -> int:
        try:
            return self[minion]['rating'][method]
        except KeyError:
            return 0

    def save(self):
        self.data[self.version][self.type_ban] = self
        with open(self.__class__.filename, 'w', encoding='utf8') as file:
            json.dump(self.data, file, indent=1, ensure_ascii=False)
