from collections import defaultdict
import random
from constants import BATTLE_SIZE, CARD_NB_COPY, General, State, Type, Event, Zone, DEFAULT_MINION_COST, MAX_TURN
from typing import Dict, List
from json import load
from utils import Card_list, controller, game, hasevent, my_zone
import script_event
from action import *
import script_hero_arene
import void
from db_card import CARD_DB, Card_data, Meta_card_data

Void = void.Void()

def card_db():
    return CARD_DB

def func_name(function):
    def new_function(self, *args, **kwargs):
        self.func_name = function.__name__
        return function(self, *args, **kwargs)

    return new_function

class Entity(object):
    default_attr = {
        'quest_value': 0,
        'general': General.NONE,
        'state': State.NONE,
        'attack': 0,
        'owner': Void,
        'from_bob': False,
        'event': Event.DEFAULT,
        'ban': 0, # utile ? techniquement une carte ban n'a pas à être créée ?
        'cost': 0,
        'method': 'no_method',
        'zone_type': Zone.NONE,
    }
    def __init__(self, id, **kwargs) -> None:
        self.entities = Card_list()
        db = {
            **Entity.default_attr,
            **self.__class__.default_attr,
            **CARD_DB[id].data,
            **kwargs}
        self.dbfId = Card_data(id, **db)

        for key, data in db.items():
            setattr(self, key, data)

    def __repr__(self) -> str:
        #if hasattr(self, 'name'):
        #    return self.name
        return super().__repr__()

    def __getitem__(self, attr):
        if isinstance(attr, str):
            return getattr(self, attr)

        return self.entities[attr]

    def __setitem__(self, attr: str, value) -> None:
        if isinstance(attr, str):
            setattr(self, attr, value)

    def __iter__(self):
        yield self.entities

    @property
    def card_db(self):
        return CARD_DB

    def reset(self, id=None) -> None:
        self.__init__(id or self.dbfId)

    def append_action(self, method, *args, order=None, **kwargs):
        if self.game:
            if order is None:
                self.game.action_stack.insert(0, [(method, args, kwargs)])
            else:
                self.game.action_stack[order].append((method, args, kwargs))
        else:
            print(self, method, 'Void append action ?')

    def append_action_with_priority(self, method, *args, **kwargs):
        self.game.action_stack.append((method, args, kwargs))

    def active_action(self):
        while self.game.action_stack:
            for method in self.game.action_stack.pop():
                action, args, kwargs = method
                action(*args, **kwargs)

    def active_local_event(self, event, **kwargs) -> bool:
        if self.event & event:
            event = Event(event)
            func = getattr(getattr(script_event, self.method), event.method, None)
            if func:
                func(self, **kwargs)
            return True
        return False

    def active_global_event(self, event, *args, **kwargs) -> None:
        """
            Active l'event local ``event`` sur ``args`` puis sur toutes leurs entités
        """
        entities_list = Card_list()
        for entity in args:
            if entity.active_local_event(event, **kwargs):
                entities_list += entity.entities

        if entities_list:
            self.active_global_event(event, *entities_list, **kwargs)

    def append(self, *entities):
        for entity in entities[::-1]:
            entity.owner.remove(entity)
            entity.owner = self
        self.entities.extend(entities)

    def remove(self, *entities):
        for entity in entities:
            if entity.owner.general >= General.GAME:
                #self.game.owner.append(entity) # before .remove, if self is in entities...
                try:
                    entity.owner.entities.remove(entity)
                    #entity.owner = Void
                except ValueError:
                    print(f'{entity} not in owner.entities')

    def remove_attr(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                if attr == 'state':
                    if value & State.DIVINE_SHIELD and self.state & State.DIVINE_SHIELD:
                        self.active_global_event(Event.LOSS_SHIELD, self.controller)
                    self.state &= State.ALL - value
                elif attr == 'event':
                    self.event &= Event.ALL - value

    def create_card_in(self, *args, position=BATTLE_SIZE, **kwargs):
        """
            Create card and append it in self
        """
        card_id = None
        for id in args:
            card_id = Card(id, **kwargs)
            self.append(card_id)
        return card_id

    def create_card(self, id, **kwargs):
        return Card(id, **kwargs)

    def buff(self, enchant_key, *args, **kwargs):
        for target in args:
            if target:
                Enchantment(enchant_key, source=self, **kwargs).apply(target)

    @property
    def controller(self):
        return controller(self)

    @property
    def my_zone(self):
        return my_zone(self)

    @property
    def game(self):
        return game(self)

    @property
    def attack(self):
        bonus = 0
        if self.my_zone.zone_type == Zone.PLAY and \
                self.dbfId in ('736', '58382'): # vieux troubloeil
            for entity in self.owner.cards + self.owner.opponent.cards:
                if entity.type & Type.MURLOC and entity is not self:
                    bonus += 1
            if self.dbfId == '58382':
                bonus *= 2
        return self._attack + bonus

    @attack.setter
    def attack(self, value):
        self._attack = value

    @property
    def position(self):
        try:
            return self.my_zone.cards.index(self)
        except ValueError:
            pass
        except AttributeError:
            pass
        return None

    @property
    def can_attack(self) -> bool:
        return hasattr(self, 'attack') and self.attack > 0

    def how_many_time_can_I_attack(self):
        if self.state & State.MEGA_WINDFURY:
            return 4
        elif self.state & State.WINDFURY:
            return 2
        return 1

    def prepare_attack(self):
        if not self.can_attack or not self.is_alive:
            return
        target = self.search_target()
        if target:
            self.append_action(attack, self, target)
            #print('prepare_attack', self, target)

    def search_target(self, *targets):
        if not targets:
            if self.state & State.ATTACK_WEAK:
                targets = self.attack_search_weak_style()
            else:
                targets = self.attack_search_normal_style()
        
        if not targets:
            return None
        return random.choice(targets)

    def attack_search_normal_style(self):
        other_board = self.my_zone.opponent.cards.\
            exclude(is_alive=False).\
            exclude_hex(state=State.NOT_TARGETABLE)

        return other_board.filter_hex(state=State.TAUNT) or other_board

    def attack_search_weak_style(self) -> list:
        other_board = self.my_zone.opponent.cards.\
            exclude(is_alive=False).\
            exclude_hex(state=State.NOT_TARGETABLE)

        if not other_board:
            return []

        new_board = sorted(other_board, key=lambda x: x.attack)
        for nb, card in enumerate(new_board):
            if card.attack != new_board[0].attack:
                break

        return new_board[:nb+1]

    def choose_one_of_them(self, choice_list, pr: str=''):
        """
            player chooses one card omong ``choice_list`` iterable
            *return: chosen card or None
            *rtype: iterable content
        """
        if not choice_list:
            return None

        long = len(choice_list)
        if long == 1:
            return choice_list[0]
        elif self.controller.is_bot or self.game.is_arene:
            return random.choice(choice_list)
        elif long > 1:
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

    @property
    def nb_turn(self) -> int:
        return self.game.nb_turn

    def all_in_bob(self):
        self.game.hand.append(*self.entities)

    def adjacent_neighbors(self) -> Card_list:
        if self in self.my_zone.cards:
            return Card_list(minion
                for minion in (
                    self.my_zone.cards[self.position-1],
                    self.my_zone.cards[self.position+1])
                    if minion)
        return Card_list()

    @property
    def has_frenzy(self):
        return self.state & State.FRENZY and self.is_alive

    def calc_stat_from_scratch(self, heal=False):
        if self.state & State.DORMANT:
            return None

        old_health = self.health
        old_state = self.state
        self.max_health = self.dbfId.health
        self.state = self.dbfId.state
        self.attack = self.dbfId.attack
        self.method = self.dbfId.method[:]
        for entity in self.entities[::-1]:
            if entity.general == General.ENCHANTMENT:
                entity.apply(self)
        #for entity, aura_met in self.controller.active_aura.items():
        #    aura_met(entity, self)

        if heal:
            self.health = self.max_health
        else:
            self.health = min(self.max_health, old_health)
            self.state &= old_state

    def apply_met_on_all_children(self, met, *targets, **kwargs) -> None:
        if targets:
            entities_list = []
            for entity in targets:
                met(self, entity, **kwargs)
                entities_list += entity.entities
            self.apply_met_on_all_children(met, *entities_list, **kwargs)

    def active_aura(self) -> None:
        # active current aura on the entity
        for buff_source, aura_buff in self.controller.aura_active.items():
            aura_buff(buff_source, self)
        # add entity aura and active it
        if hasevent(self, Event.PLAY_AURA):
            getattr(getattr(script_event, self.method), 'play_aura')(self)
            #self.controller.aura_active[self] = getattr(getattr(script_event, self.method), 'aura')

    def remove_my_aura_action(self, target) -> None:
        if getattr(target, 'aura', False) and getattr(target, 'source', None) is self:
            target.remove()

    def search_id(self, target):
        if target in Void.temp_list:
            print(f'{target} found in {Void}')
            return True

        if target in self.entities:
            print(f'{target} found in {self}')
            return True
        for entity in self.entities:
            if entity.search_id(target):
                break
        return False

class Minion(Entity):
    default_attr = {
        'health': 1,
        'attack': 1,
        'state': State.DEFAULT,
        'old_position': 0,
    }
    def __init__(self, id, **kwargs):
        super().__init__(id, **kwargs)
        self._max_health = self.health

    def __repr__(self) -> str:
        #if self.general == General.MINION:
        #    return f'{self.name} ({self.attack}-{self.health})'
        return f'{self.name}'

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

    def play(self, board=None, position=BATTLE_SIZE) -> None:
        if board is None:
            if self.my_zone.zone_type != Zone.HAND:
                print(f'Carte {self.name} non jouée')
                return None
            board = self.controller.board

        if self.general == General.MINION:
            board.append(self, position)
        elif self.general == General.SPELL:
            getattr(script_event, self.method).play(self)

    @property
    def is_alive(self):
        return self.health > 0 and not self.state & State.IS_POISONED

    def die(self, killer=None):
        if self.owner.zone_type != Zone.PLAY:
            return None

        position = self.position
        controller = self.controller
        if position is None:
            print(f'Error {self} position is None, zone : {self.my_zone.cards} {controller}')
        self.owner.remove(self)
        # la hyène est buffée après l'activation du râle
        # donc le poisson meure de la goule instable avant de récupérer son râle ?
        self.active_local_event(Event.DEATHRATTLE, position=position)

        self.active_global_event(Event.DIE, controller, controller.opponent, source=self, killer=killer)

        if self.state & State.REBORN:
            self.append_action(self.reborn, position)

    def reborn(self, position):
        minion = self.create_card(self.dbfId)
        minion.remove_attr(state=State.REBORN)
        minion.health = 1
        self.my_zone.append(minion, position=position)


class Enchantment(Entity):
    default_attr = {
        'aura': False,
        'source': Void,
    }

    buff_attr_add = {
        'attack', # : int
        'max_health', # : int
        'health', # int
        #'method', # : list
    }

    buff_attr_hex = {
        'state',
        'event',
    }

    def __init__(self, id, **kwargs):
        super().__init__(id, **kwargs)

    def apply(self, target_id) -> None:
        if target_id is None or target_id.state & State.NOT_TARGETABLE:
            return None

        if hasattr(self, 'duration'):
            if self.owner.general == General.ZONE:
                self.duration += target_id.game.nb_turn
            elif self.duration <= target_id.game.nb_turn:
                super().remove()
                return None

        if getattr(self, 'no_combinable', None):
            for entity in target_id.entities:
                if entity.dbfId == self.dbfId:
                    if self.data != entity.data:
                        entity.data = {**self.data}
                    return None

        if hasattr(self, 'script'):
            if self.owner is not target_id:
                target_id.append(self)
            getattr(self, self.script)(target_id)
            if self.owner is not target_id:
                self.active_global_event(Event.ADD_ENCHANTMENT_ON, self.controller)

    def add_stat(self, target_id):
        for attr in self.__class__.buff_attr_add & set(dir(self)) & set(dir(target_id)):
            target_id[attr] += self[attr]
        for attr in self.__class__.buff_attr_hex & set(dir(self)) & set(dir(target_id)):
            target_id[attr] |= self[attr]

    def remove_event(self, target_id):
        target_id.remove_attr(event=self.event)

    def set_stat(self, target_id):
        targetable_attr = self.__class__.buff_attr_add.copy()
        targetable_attr.union(self.__class__.buff_attr_hex)
        #targetable_attr.discard('method')

        for attr in targetable_attr & set(dir(self)) & set(dir(target_id)):
            target_id[attr] = self[attr]

    def remove(self):
        old_owner = self.owner
        super().remove(self)
        old_owner.calc_stat_from_scratch()


class Hero_power(Entity):
    default_attr = {
        'script': '',
        'minion_cost': DEFAULT_MINION_COST,
        'hero_script': 'Default_script',
        'roll_cost': 1,
        'cost': 0,
        'is_enabled': True,
        'temp_counter': 0, # set to 0 at 'begin_turn'
    }

    def __init__(self, id, **kwargs):
        super().__init__(id, **kwargs)
        if hasattr(self, 'max_health'):
            self.health = self.max_health

    def enable(self) -> None:
        if getattr(self, 'remain_use', 0) >= 1:
            self.is_enabled = True

    def disable(self) -> None:
        self.is_enabled = False

    def dec_remain_use(self) -> None:
        if hasattr(self, 'remain_use'):
            self.remain_use -= 1

    def dec_power_cost(self) -> None:
        self.cost = max(0, self.cost - 1)

    def active_script_arene(self, *args, **kwargs) -> None:
        met = getattr(script_hero_arene, self.hero_script)
        if met:
            getattr(met, f'turn_{self.game.nb_turn}')(self.owner, *args, **kwargs)

    def use(self):
        if self.is_enabled:
            if self.owner.gold >= self.cost:
                self.owner.gold -= self.cost
                cls = getattr(script_event, self.method)
                if hasattr(cls, Event(Event.USE_POWER).method):
                    ret = getattr(cls, Event(Event.USE_POWER).method)(self)
                    if ret:
                        self.dec_remain_use()
                        self.disable()

class Card:
    init_class = {
        General.MINION: Minion,
        General.ENCHANTMENT: Enchantment,
        General.HERO_POWER: Hero_power,
    }

    def __new__(cls, id, **kwargs):
        return cls.init_class.get(card_db()[id]['general'], Entity)(id, **kwargs)


if __name__ == "__main__":
    al = Meta_card_data(CARD_DB[card] for card in ['41245', '102', '201'])
    print(al)
    print(al.sort('attack'))
