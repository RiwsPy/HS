from constants import General, LEVEL_MAX

def game(self):
    ret = self
    while ret.general > General.GAME:
        ret = ret.owner
    if ret.general == General.GAME:
        return ret
    return None

def hasevent(self, event) -> bool:
    ret = self
    while ret.general > General.GAME:
        if not ret.event & event:
            return False
        ret = ret.owner
    return True

def controller(self):
    ret = self
    while ret.general > General.HERO:
        ret = ret.owner
    return ret

def my_zone(self):
    ret = self
    while ret.general > General.ZONE:
        ret = ret.owner
    if ret.general == General.ZONE:
        return ret
    return None


class Card_list(list):
    def __getitem__(self, value):
        if isinstance(value, slice):
            return self.__class__(super().__getitem__(value))
        return super().__getitem__(value)

    def filter(self, **kwargs):
        return self.__class__(card
            for card in self
                for k, v in kwargs.items()
                    if getattr(card, k) == v)

    def filter_hex(self, **kwargs):
        return self.__class__(card
            for card in self
                for k, v in kwargs.items()
                    if getattr(card, k) & v)

    def exclude(self, *args, **kwargs):
        copy = self.__class__(card
            for card in self
                if card not in args)
        if kwargs:
            return self.__class__(card
                for card in copy
                    for k, v in kwargs.items()
                        if getattr(card, k) != v)
        return copy

    def exclude_hex(self, *args, **kwargs):
        copy = self.__class__(card
            for card in self
                if card not in args)
        if kwargs:
            return self.__class__(card
                for card in copy
                    for k, v in kwargs.items()
                        if not getattr(card, k) & v)
        return copy

    def filter_level(self, level_max=LEVEL_MAX, level_min=1):
        return self.__class__(card
            for card in self
                if level_min <= card.level <= level_max)


class Board_Card_list(Card_list):
    def __getitem__(self, value):
        try:
            return super().__getitem__(value)
        except IndexError:
            return None
