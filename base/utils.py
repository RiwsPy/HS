from collections import defaultdict
from .enums import Type, LEVEL_MAX, VERSION, Race
import json
from types import GeneratorType
import random
from typing import Any

def requirements(**kwargs):
    def constraint(function):
        def decorator(self, sequence):
            return function(self, sequence)

        is_valid = True
        for k, v in kwargs:
            is_valid = True

        if is_valid:
            return decorator
        return None

    return constraint


def repeat_effect(function):
    def decorator(self, sequence):
        nb_strike = getattr(self, 'nb_strike', 1)

        # Brann/Vaillefendre effect
        if getattr(sequence, 'triple_effect', False):
            nb_strike *= 3
        elif getattr(sequence, 'double_effect', False):
            nb_strike *= 2

        for _ in range(nb_strike):
            function(self, sequence)
    return decorator

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

    def one_minion_by_race(self) -> 'Card_list':
        """
            Return a list which contains until one minion by race
        """
        # Non fonctionnel en cas de serviteur bi-race sans être de race ALL (Bête/Dragon...)
        # les race 'ALL' sont pris par défaut (en cas de non représentation d'un serviteur d'une race)
        # A suivre

        shuffle_copy = self.shuffle()
        tri = defaultdict(list)
        for minion in shuffle_copy:
            tri[minion.race].append(minion)

        ret = Card_list()
        all_race = Race('ALL')
        for race in Race.battleground_race():
            try:
                ret.append(tri[race][0]) # ajout du premier minion
            except IndexError:
                if tri[all_race]:
                    ret.append(tri[all_race].pop(0))
        return ret

    def shuffle(self) -> 'Card_list':
        shuffle_copy = self[:]
        random.shuffle(shuffle_copy)
        return shuffle_copy

    def random_choice(self):
        try:
            return random.choice(self)
        except IndexError:
            return None

    def choice(self, player, pr: str = '') -> Any:
        choice_list = self.exclude(DORMANT=True)
        if not choice_list or not player:
            return None
        elif len(choice_list) == 1:
            return choice_list[0]
        elif player.is_bot or self.game.is_arene:
            return choice_list.random_choice()
        else:
            if pr:
                print(pr)
            for nb, entity in enumerate(choice_list):
                print(f'{nb}- {entity}')
            while True:
                try:
                    return choice_list[int(input())]
                except IndexError:
                    print('Valeur incorrecte.')
                except ValueError:
                    print('Saississez une valeur.')



class Board_Card_list(Card_list):
    def __getitem__(self, value):
        try:
            return super().__getitem__(value)
        except IndexError:
            return None

    def append(self, card):
        super().append(card)
        if getattr(self, 'owner', None):
            self.owner.owner.check_triple()

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
