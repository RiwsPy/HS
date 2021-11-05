import random
from enums import FIELD_SIZE, MAX_TURN, CardName, Rarity, Zone, Type, \
    DEFAULT_MINION_COST, ADAPT_ENCHANTMENT, state_list
from typing import Any
from utils import Card_list, controller, game, my_zone
from action import *
import script_hero_arene
import script_minion_arene
import void
from db_card import CARD_DB, Card_data
from sequence import Sequence

Void = void.Void()

def card_db():
    return CARD_DB

def func_name(function):
    def new_function(self, *args, **kwargs):
        self.func_name = function.__name__
        return function(self, *args, **kwargs)

    return new_function

def khadgar_aura(function):
    def double_invoc(self, sequence, *args, **kwargs):
        card_id = function(self, sequence, *args, **kwargs)
        if card_id:
            for entity in self.controller.board.cards[:]:
                if entity.dbfId in (CardName.KHADGAR, CardName.KHADGAR_P):
                    for _ in range(entity.nb_strike):
                        clone_card = card_id.clone()
                        sequence.position += 1
                        #TODO: activation de SUMMON
                        clone_card.summon(position=sequence.position)
                        #self.controller.board.append(clone_card, position=sequence.position)
        return card_id
    return double_invoc


class Entity:
    default_attr = {
        'quest_value': 0,
        'type': Type.DEFAULT,
        'attack': 0,
        'owner': Void,
        'from_bob': False,
        'ban': 0, # utile ? techniquement une carte ban n'a pas à être créée ?
        'cost': 0,
        'id': 'no_method',
        'zone_type': Zone.NONE,
        'rarity': Rarity.DEFAULT,
        'techLevel': 0,
        'name': '',
        'temp_counter': 0, # set to 0 during each 'turn_on' sequence
    }
    def __init__(self, dbfId, **kwargs) -> None:
        self.entities = Card_list()
        db = {
            **Entity.default_attr,
            **getattr(self.__class__, 'default_attr', {}),
            **CARD_DB[dbfId].data,
            **kwargs}

        for key, data in db.items():
            setattr(self, key, data)

        self.dbfId = Card_data(**db)

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

    def __iter__(self, *args):
        next_entities = Card_list()
        for ent in args or self.entities:
            next_entities += ent.entities
            yield ent
        if next_entities:
            yield from self.__iter__(*next_entities)

    def _iter_seq(self, sequence: Sequence, *args):
        next_entities = Card_list()
        for ent in args or self.entities:
            if ent.type != Type.ZONE or 'ALL' in ent.phase or sequence.name in ent.phase:
                next_entities += ent.entities
            yield ent
        # ON / OFF phase inaccessible pour la source de la séquence
        # sauf si source.valid_for_myself == True
        if sequence.phase_name.rpartition('_')[-1] in ('ON', 'OFF') and\
                not getattr(sequence.source, 'valid_for_myself', False):
            next_entities = next_entities.exclude(sequence.source)
        if next_entities:
            yield from self._iter_seq(sequence, *next_entities)

    @property
    def in_fight_sequence(self) -> bool:
        return self.game.current_sequence == 'FIGHT'

    def no_method(self, *args, **kwargs):
        pass

    @property
    def card_db(self):
        return CARD_DB

    @property
    def level(self):
        return self.techLevel

    def reset(self, id=None) -> None:
        self.__init__(id or self.dbfId)

    def append_action(self, method, *args, order=None, **kwargs):
        if self.game:
            if order is None:
                self.game.action_stack.appendleft([(method, args, kwargs)])
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

    def append(self, *entities):
        for entity in entities[::-1]:
            entity.owner.remove(entity)
            entity.owner = self
        self.entities.extend(entities)

    def remove(self, *entities):
        for entity in entities:
            if entity.owner.type >= Type.GAME:
                #self.game.owner.append(entity) # before .remove, if self is in entities...
                try:
                    entity.owner.entities.remove(entity)
                    #entity.owner = Void
                except ValueError:
                    pass
                    #print(f'{entity} not in owner.entities')

    def remove_attr(self, *args, **kwargs):
        for state in args:
            if state in state_list:
                setattr(self, state, False)

    def create_card_in(self, *args, position=FIELD_SIZE, **kwargs) -> 'Entity':
        """
            Create card and append it in self
        """
        card_id = None
        for id in args:
            card_id = self.create_card(id, **kwargs)
            self.append(card_id)
        return card_id

    def create_card(self, dbfId, **kwargs) -> 'Entity':
        card_id = Card(dbfId, **kwargs)
        card_id.owner = self.controller
        return card_id

    def buff(self, enchantment_dbfId, *args, **kwargs):
        for target in args:
            if target:
                #Enchantment(enchantment_dbfId, source=self, **kwargs).apply(target)
                enchant = Card(enchantment_dbfId, source=self, **kwargs)
                Sequence('ENHANCE', enchant, target=target).start_and_close()

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
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = value

    @property
    def position(self):
        try:
            return self.my_zone.cards.index(self)
        except (ValueError, AttributeError):
            pass
        return None

    @property
    def can_attack(self) -> bool:
        return getattr(self, 'attack', 0) > 0

    def how_many_time_can_I_attack(self) -> int:
        if not self.can_attack:
            return 0
        elif self.MEGA_WINDFURY:
            return 4
        elif self.WINDFURY:
            return 2
        return 1

    def choose_one_of_them(self, choice_list: list, pr: str='') -> Any:
        """
            player chooses one card among ``choice_list`` list
            *return: chosen card id or None
            *rtype: list content
        """
        if not choice_list or not self.controller:
            return None
        elif len(choice_list) == 1:
            return choice_list[0]
        elif self.controller.is_bot or self.game.is_arene:
            return random.choice(choice_list)
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

    @property
    def nb_turn(self) -> int:
        return self.game.nb_turn

    def all_in_bob(self):
        self.game.hand.append(*self.entities)

    def adjacent_neighbors(self) -> Card_list:
        position = self.position

        if position is not None:
            zone = self.my_zone.cards
            if position == 0:
                if zone[1]:
                    return Card_list(zone[1])
            else:
                return Card_list(minion
                for minion in zone[position-1:position+2:2]
                    if minion)

        return Card_list()

    @property
    def has_frenzy(self):
        return self.FRENZY and self.is_alive

    def calc_stat_from_scratch(self, heal=False) -> None:
        if self.DORMANT:
            return None

        old_health = self.health
        old_mechanics = {mechanic: getattr(self, mechanic, False)
            for mechanic in state_list}

        # reset stats & mechanics
        self.max_health = self.dbfId.health
        self.attack = self.dbfId.attack
        for mechanic in state_list:
            setattr(self, mechanic, mechanic in self.dbfId.mechanics)

        for entity in self.entities[::-1]:
            if entity.type == Type.ENCHANTMENT and entity.is_over:
                self.entities.remove(entity)

        for entity in self.entities:
            if entity.type == Type.ENCHANTMENT:
                entity.apply()

        if heal:
            self.health = self.max_health
        else:
            self.health = min(self.max_health, old_health)
            for mechanic, value in old_mechanics.items():
                setattr(self, mechanic, value)

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

    def active_script_arene(self, *args, strat='', **kwargs) -> None:
        if self.type == Type.HERO_POWER:
            met = getattr(script_hero_arene, self.hero_script)
            if met:
                met_turn = getattr(met, f'turn_{self.game.nb_turn}', None)
                if met_turn:
                    met_turn(self.owner, *args, **kwargs)
        elif self.type == Type.MINION:
            met = getattr(script_minion_arene, self.id)
            if met:
                getattr(getattr(met, strat), f'turn_{self.game.nb_turn}')(self, *args, **kwargs)


    @khadgar_aura
    def invoc(self, sequence, repop_dbfId) -> 'Entity':
        #TODO: remplacer position par l'entité présente dans la position suivante
        # ainsi chaque repop sera invoqué juste avant
        minion_id = self.create_card(repop_dbfId)
        if sequence.source in self.controller.board.cards:
            sequence.position += 1

        minion_id.summon(position=sequence.position)
        if minion_id not in self.controller.board: # échec de la séquence summon
            return None

        return minion_id


class Minion(Entity):
    default_attr = {
        'techLevel': 1,
        'health': 1,
        'attack': 1,
    }

    def __init__(self, dbfId, **kwargs):
        super().__init__(dbfId, **kwargs)
        self._max_health = self.health

    def __repr__(self) -> str:
        #if self.type == Type.MINION:
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

    def play(self, sequence=None, **kwargs):
        if sequence is None:
            kwargs['position'] = kwargs.get('position', None)
            with Sequence('PLAY', self, **kwargs) as seq:
                if seq.is_valid:
                    with Sequence('SUMMON', self, **kwargs) as summon_seq:
                        Sequence('BATTLECRY',
                            self,
                            targets=seq.targets,
                            position=self.position).start_and_close()

    def die(self, sequence=None, **kwargs):
        if sequence is None:
            kwargs['position'] = self.position
            with Sequence('DIE', self, **kwargs) as seq:
                if seq.is_valid:
                    Sequence('DEATHRATTLE', self, **kwargs).start_and_close()
                    #TODO: vérifier le sens d'exécution entre les deux suivants
                    Sequence('REBORN', self, **kwargs).start_and_close()
                    Sequence('AVENGE', self, **kwargs).start_and_close()

    def play_start(self, sequence):
        if self.my_zone.zone_type != Zone.HAND and self.controller.type != Type.BOB:
            sequence.is_valid = False
            print(f'Carte {self.name} non jouée : zone_type {self.my_zone.zone_type} {self.my_zone}')
            return None
        elif self.in_fight_sequence:
            sequence.is_valid = False
            return None

        if self.controller.board.can_add_card(self):
            self.owner.remove(self)
            # + paid cost
        else:
            sequence.is_valid = False

    def play_end(self, sequence):
        self.controller.played_cards[self.nb_turn] += self

    def overkill_start(self, sequence):
        sequence.is_valid = self.OVERKILL

    def avenge_on(self, sequence):
        if sequence.source.controller is self.controller and\
                self.AVENGE and\
                sequence.source is not self:
            self.temp_counter += 1
            if self.temp_counter % self.avenge_counter == 0:
                sequence(self.avenge, sequence)

    @property
    def is_alive(self) -> bool:
        return self.health > 0 and not self.IS_POISONED

    def die_start(self, sequence):
        if self.type == Type.MINION and self.in_fight_sequence:
            if self.AURA:
                print('die de', sequence.source)
                for entity in self.controller.field:
                    if entity.type == Type.ENCHANTMENT: # and entity.source is self and entity.aura:
                        print(entity, entity.source, entity.aura)
                        sequence(entity.remove)
            sequence(self.controller.graveyard.append, self)
        else:
            sequence.is_valid = False
            print('humm die in', self.owner.id, self)

    def copy_enchantment_from(self, source: Entity) -> None:
        for entity in source.entities:
            if entity.type == Type.ENCHANTMENT and not getattr(entity, 'aura', False):
                #attrs = entity.__dict__.copy()
                #del attrs['dbfId']
                #enchant = Card(entity.dbfId, **attrs)
                enchant = Card(**entity.__dict__)
                self.append(enchant)
                enchant.apply()

    def add_adapt(self, nb: int=0) -> None:
        if not nb:
            enchantment_id = random.choice(ADAPT_ENCHANTMENT)
        else:
            try:
                enchantment_id = ADAPT_ENCHANTMENT[nb]
            except KeyError:
                print(f'add_adapt error : unknown adapt n°{nb}')

        self.buff(enchantment_id, self)

    def discover(self, card_list: Card_list, nb: int=3) -> Entity:
        #TODO: Warning, problem if the card is moving during the discover
        card_list = card_list.copy()
        random.shuffle(card_list)
        list_card_choice = Card_list()
        exclude_dbfid = {self.dbfId}

        for card in card_list:
            if card.dbfId not in exclude_dbfid:
                list_card_choice.append(card)
                if len(list_card_choice) >= nb:
                    break
                exclude_dbfid.add(card.dbfId)

        return self.choose_one_of_them(list_card_choice)

    def sell_start(self, sequence) -> None:
        seller = self.controller
        if not self.in_fight_sequence and\
                seller.type == Type.HERO and self in seller.board.cards:
            buyer = seller.bob
            cost = getattr(sequence, 'cost', buyer.minion_cost)
            if buyer.can_buy_minion(cost=cost):
                buyer.gold -= cost
                seller.gold += cost

                seller.sold_minions[self.nb_turn].append(self)
                buyer.bought_minions[self.nb_turn].append(self)
                sequence(buyer.hand.append, self)
            else:
                sequence.is_valid = False
        else:
            sequence.is_valid = False

    def sell(self, sequence=None, **kwargs):
        if sequence is None:
            Sequence('SELL', self, **kwargs).start_and_close()

    def buy_start(self, sequence) -> None:
        seller = self.controller
        if not self.in_fight_sequence and seller.type == Type.BOB:
            buyer = seller.opponent
            cost = getattr(sequence, 'cost', buyer.minion_cost)
            if buyer.can_buy_minion(cost=cost):
                buyer.gold -= cost
                seller.gold += cost

                buyer.hand.append(self)
                seller.sold_minions[self.nb_turn].append(self)
                buyer.bought_minions[self.nb_turn].append(self)
            else:
                sequence.is_valid = False
        else:
            sequence.is_valid = False

    def buy(self, sequence=None, **kwargs):
        if sequence is None:
            Sequence('BUY', self, **kwargs).start_and_close()

    def summon(self, sequence=None, **kwargs):
        # Entity appear in board during summon phase,
        # during summon_on and summon_start entity is not in board yet
        if sequence is None:
            Sequence('SUMMON', self, **kwargs).start_and_close()

    def summon_start(self, sequence):
        if self.controller.board.can_add_card(self):
            sequence(
                self.controller.board.append,
                self,
                position=getattr(sequence, 'position', None))
        else:
            sequence.is_valid = False

    def reborn_start(self, sequence) -> None:
        sequence.is_valid = self.REBORN and\
            self.owner.id == 'Graveyard' and\
            self.in_fight_sequence

    def combat(self, sequence=None):
        if sequence is None:
            seq = Sequence('PRE_COMBAT', self)
            seq.start_and_close()
            if seq.is_valid:
                Sequence('COMBAT', self, targets=seq.targets).start_and_close()

    def pre_combat_start(self, sequence: Sequence) -> None:
        if not self.can_attack or not self.is_alive\
                or not self.in_fight_sequence:
            sequence.is_valid = False
            return

        target = self.search_fight_target()
        if target:
            sequence.add_target(target)
        else:
            sequence.is_valid = False

    def combat_start(self, sequence):
        if self.CLEAVE:
            for target in sequence.targets:
                position = target.position
                if target.owner.cards[position-1]:
                    sequence(self.damage, target.owner.cards[position-1], self.attack, overkill=True)
                sequence(attack, sequence)
                if target.owner.cards[position+1]:
                    sequence(self.damage, target.owner.cards[position+1], self.attack, overkill=True)
        else:
            sequence(attack, sequence)

    def search_fight_target(self) -> Entity:
        opponent_board = self.my_zone.opponent.cards.\
            exclude(is_alive=False, DORMANT=True)

        targets = opponent_board.filter(TAUNT=True) or opponent_board
        if targets:
            return random.choice(targets)
        return None
    
    def loss_shield_start(self, sequence):
        sequence.is_valid = self.DIVINE_SHIELD

    def set_premium(self) -> None:
        if hasattr(self, 'battlegroundsPremiumDbfId') is False:
            return None
        #TODO: l'origine de la carte est erroné si une nouvelle carte ne remplace pas l'ancienne
        #Dans ce cas, des informations utiles peuvent être perdues
        golden_card = Card(self.battlegroundsPremiumDbfId)
        #self.dbfId = golden_card.dbfId

    def clone(self) -> Entity:
        clone_card = self.create_card(self.dbfId)
        clone_card.copy_enchantment_from(self)
        for mechanic in self.mechanics:
            setattr(clone_card, mechanic, True)
        clone_card.health = self.health
        return clone_card

    def damage(self, target: Entity, damage_value: int, overkill=False) -> None:
        with Sequence('HIT',
                self,
                target=target,
                damage_value=damage_value,
                position=self.position) as seq:
            if seq.is_valid and target.IMMUNE is False and target.DORMANT is False:
                if target.DIVINE_SHIELD:
                    with Sequence('LOSS_SHIELD', target) as loss_shield_seq:
                        if loss_shield_seq.is_valid:
                            target.DIVINE_SHIELD = False
                            seq.damage_value = 0

                if seq.damage_value > 0:
                    target.health -= seq.damage_value
                    target.IS_POISONED &= self.POISONOUS
                    if not target.is_alive:
                        if target.health < 0 and overkill:
                            Sequence('OVERKILL', self).start_and_close()
                    elif target.FRENZY:
                        target.FRENZY = False
                        Sequence('FRENZY', target).start_and_close()
        damage_resolve(self, 
            *(self.controller.board.cards + self.controller.opponent.board.cards))

    @khadgar_aura
    def reborn(self, sequence) -> Entity:
        minion = self.create_card(self.dbfId)
        minion.remove_attr('REBORN')
        minion.health = 1
        if self.controller.board.can_add_card(minion):
            minion.summon(position=sequence.position)
            return minion
        return None


class Enchantment(Entity):
    """
        duration X (int): timing X turns
        duration -1: timing MAX_TURN turns
        duration: not hasattr(self, 'duration') : special
            > Duration 1 if applied during fight_sequence
            > Duration MAX_TURN otherwise
    """
    #TODO: fusion des enchantements de dbfId identiques ? > gène la rétroactivité des bonus
    default_attr = {
        'aura': False,
        'source': Void,
    }

    buff_attr_add = {
        'attack', # : int
        'max_health', # : int
        'health', # int
        'mechanics', # list
    }

    def __init__(self, dbfId, **kwargs):
        super().__init__(dbfId, **kwargs)

        if not hasattr(self, 'duration'):
            if self.source.in_fight_sequence:
                self.duration = self.source.game.nb_turn +1
            else:
                self.duration = MAX_TURN
        elif self.duration == -1:
            self.duration = MAX_TURN
        else:
            self.duration += self.source.game.nb_turn

    @property
    def is_over(self) -> bool:
        return self.duration <= self.nb_turn

    def enhance_start(self, sequence: Sequence) -> None:
        target = sequence.target
        if target is None or target.DORMANT or self.duration <= target.nb_turn:
            sequence.is_valid = False
            return None

        target.append(self)
        self.apply()

    def apply(self) -> None:
        pass

    """
    def add_stat(self, target_id):
        for attr in self.__class__.buff_attr_add & set(dir(self)) & set(dir(target_id)):
            target_id[attr] += self[attr]
        for mechanic in self.mechanics:
            setattr(target_id, mechanic, True)

    def remove_mechanics(self, target_id):
        for mechanic in self.mechanics:
            setattr(target_id, mechanic, False)

    def set_stat(self, target_id):
        for attr in self.__class__.buff_attr_add & set(dir(self)) & set(dir(target_id)):
            target_id[attr] = self[attr]
    """

    def remove(self):
        old_owner = self.owner
        super().remove(self)
        # uniquement si en cas de modification de caractéristiques ?
        old_owner.calc_stat_from_scratch()


class Hero_power(Entity):
    default_attr = {
        'minion_cost': DEFAULT_MINION_COST,
        'hero_script': 'Default_script',
        'roll_cost': 1,
        'cost': 0,
        'is_enabled': True,
        'levelup_cost_mod': 0,
        'card_by_roll_mod': 0,
    }

    def __init__(self, dbfId, **kwargs):
        super().__init__(dbfId, **kwargs)
        if hasattr(self, 'max_health') and self.nb_turn == 1:
            self.health = self.max_health

    def enable(self) -> None:
        self.is_enabled = getattr(self, 'remain_use', 0) > 0

    def disable(self) -> None:
        self.is_enabled = False

    def dec_remain_use(self) -> None:
        if hasattr(self, 'remain_use'):
            self.remain_use -= 1

    def dec_power_cost(self) -> None:
        self.cost = max(0, self.cost - 1)

    def use(self) -> None:
        if self.is_enabled and not self.in_fight_sequence:
            if self.owner.gold >= self.cost:
                with Sequence('USE_POWER', self) as seq:
                    if seq.is_valid:
                        self.owner.gold -= self.cost
                        self.dec_remain_use()
                        self.disable()

    @property
    def board(self) -> Entity:
        return self.owner.board

    def change(self, dbfId) -> None:
        #TODO: test
        new_power_id = self.create_card(dbfId)
        if new_power_id.type == Type.HERO_POWER:
            self = new_power_id


class Spell(Entity):
    default_attr = {
    }

    def play(self, sequence=None):
        if sequence is None:
            if not self.in_fight_sequence and self.cost <= self.controller.gold:
                self.controller.gold -= self.cost
                with Sequence('PLAY', self) as seq:
                    #TODO: conterspell effect ?
                    if seq.is_valid:
                        if self.SECRET is False:
                            self.owner.remove(self)
                            self.cast(seq)
                            self.controller.graveyard.append(self)
                        else:
                            self.controller.secret_board.append(self)


    def die(self, sequence=None):
        self.controller.graveyard.append(self)

class Card:
    def __new__(cls, dbfId, **kwargs):
        import script_event
        self = getattr(script_event, str(CARD_DB[dbfId]['id']))
        #Card.init_class[CARD_DB[dbfId].get('type', 'DEFAULT')].__init__(self, dbfId, **kwargs)
        return self(dbfId, **kwargs)


if __name__ == "__main__":
    pass
