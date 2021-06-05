from constants import General, State, Type, Event
from typing import Dict, List
from json import load
from utils import game

def charge_all_cards() -> Dict[str, dict]:
    all_cards = {}
    with open("bdd_card.json", "r", encoding="utf-8") as file:
        all_cards = load(file)

    # normalization
    for key, value in all_cards.items():
        value['entity_id'] = key
        value['general'] = getattr(General, value.get('general', 'DEFAULT'))
        value['synergy'] = Type(getattr(Type, value.get('synergy', 'ALL')))
        value['type'] = Type(getattr(Type, value.get('type', 'DEFAULT')))
        if 'state' in value:
            value['state'] = int(value['state'], 16)
        if 'event' in value:
            value['event'] = int(value['event'], 16)
        all_cards[key] = value

    return all_cards

CARD_DB = charge_all_cards()


class Entity(object):
    default_attr = {
        'entities': [],
        'quest_value': 0,
        '_owner': None,
        'from_bob': False,
        'event': Event.DEFAULT,
        'ban': 0, # utile ? techniquement une carte ban n'a pas à être créée ?
        'cost': 0,
    }
    def __init__(self, id, **attr) -> None:
        self.data = {}
        self.data.update({
            **Entity.default_attr,
            **self.__class__.default_attr,
            **CARD_DB.get(id),
            **attr})

        for key, data in self.data.items():
            self[key] = data
        self.card_in = [self]

    def __getattr__(self, attr):
        if attr[:5] == 'init_':
            return self.data[attr[5:]]
        raise AttributeError(f'{type(self)} have no attribute: {attr}')

    def __getitem__(self, attr):
        return getattr(self, attr)

    def __setitem__(self, attr: str, value) -> None:
        setattr(self, attr, value)

    def reset(self, id=None) -> None:
        self.__init__(id or self.entity_id)

    def active_event(self, event):
        if event & self.event:
            game.trigger_stack.append('houhoulala')

    @property
    def owner(self) -> object:
        return self._owner

    @owner.setter
    def owner(self, value) -> None:
        if self._owner:
            self._owner.entities.remove(self)
        if value and value != self._owner:
            value.entities.append(self)
        self._owner = value

class Minion(Entity):
    default_attr = {
        'health': 1,
        'attack': 1,
        '_max_health': 1, 
        'state': State.DEFAULT,
        'event': Event.DEFAULT,
    }
    def __init__(self, id):
        super().__init__(id)

    @property
    def max_health(self) -> int:
        return self._max_health

    @max_health.setter
    def max_health(self, value) -> None:
        bonus = value - self.max_health
        self._max_health = value
        if bonus >= 0:
            self.health += bonus
        else:
            self.health = min(self.health, value)

    def play(self):
        if self.owner and hasattr(self.owner, 'board'):
            if not self.owner.board.append(self):
                print(f'{self.name} non jouée')
        else:
            print(f"can't play {self.name} : no board.")

class Hero(Entity):
    default_attr = {
        '_max_health': 1, 
        'state': State.DEFAULT,
    }

    def __init__(self, id):
        super().__init__(id)
        self.health = self.max_health

    @property
    def max_health(self) -> int:
        return self._max_health

    @max_health.setter
    def max_health(self, value) -> None:
        bonus = value - self.max_health
        self._max_health = value
        if bonus < 0:
            self.health = min(self.health, value)

class Enchantment(Entity):
    default_attr = {}

    buff_attr_add = {
        'attack', # : int
        'max_health', # : int
        'method', # : list
    }

    buff_attr_hex = {
        'state',
        'event',
    }

    def __init__(self, id, **attr):
        super().__init__(id, **attr)

    def apply(self, target_id=None) -> None:
        if hasattr(self, 'no_combinable') and self.no_combinable:
            old_enchantment = None
            for entity in self.entities:
                if entity.entity_id == self.entity_id:
                    old_enchantment = entity
                    break
            if old_enchantment:
                if self.data != old_enchantment.data:
                    old_enchantment.data = self.data
                return None
        if hasattr(self, "script") and self.script in dir(self):
            target_id = target_id or self.owner
            self.owner = target_id
            if target_id:
                getattr(self, self.script)(target_id)

    def add_stat(self, target_id):
        for attr in self.__class__.buff_attr_add & set(dir(self)) & set(dir(target_id)):
            target_id[attr] += self[attr]
        for attr in self.__class__.buff_attr_hex & set(dir(self)) & set(dir(target_id)):
            target_id[attr] |= self[attr]

    def set_stat(self, target_id):
        targetable_attr = self.__class__.buff_attr_add.copy()
        targetable_attr.union(self.__class__.buff_attr_hex)
        
        for attr in targetable_attr & set(dir(self)) & set(dir(target_id)):
            target_id[attr] = self[attr]

    def dec_duration(self):
        if hasattr(self, "duration"):
            self.duration -= 1


class Hero_power(Entity):
    default_attr = {}

    def __init__(self, id):
        super().__init__(id)


class Card:
    init_class = {
        General.NONE: Entity,
        General.MINION: Minion,
        General.HERO: Hero,
        General.ENCHANTMENT: Enchantment,
        General.HERO_POWER: Hero_power
    }

    def __new__(cls, id):
        return cls.init_class[CARD_DB[id]['general']](id)

if __name__ == "__main__":
    crd = Card('100')
    enc = Card('1_e')
    print(enc.attack)
    enc.apply(crd)
    print(crd.method)
