from .enums import LEVEL_MAX, MAX_TURN, CardName, Zone, Type, \
    DEFAULT_MINION_COST, state_list
from .utils import Card_list, controller, game, my_zone
from .action import attack
from .scripts import hero_arene, minion_arene
from .void import Void
from .db_card import Card_data, Meta_card_data, CardDB
from .sequence import Sequence
from typing import Any


def khadgar_aura(function):
    def double_invoc(self, sequence, *args, **kwargs):
        card_id = function(self, sequence, *args, **kwargs)
        if card_id:
            for entity in self.controller.board.cards[:]:
                if entity.dbfId in (CardName.KHADGAR, CardName.KHADGAR_P):
                    for _ in range(entity.nb_strike):
                        clone_card = card_id.clone()
                        sequence.position += 1
                        # TODO: activation de SUMMON
                        clone_card.summon(position=sequence.position)
        return card_id
    return double_invoc


class Entity:
    default_attr = {
        'quest_value': 0,
        'attack': 0,
        'armor': 0,
        'from_bob': False,
        'temp_counter': 0,  # set to 0 during each 'turn_on' sequence
    }

    def __init__(self, dbfId, **kwargs) -> None:
        self.entities = Card_list()
        self.owner = Void()
        db = {
            **self.get_default_attr(),
            **CardDB()[dbfId].__dict__,
            **kwargs}
        for key, data in db.items():
            if data is not None:
                setattr(self, key, data)

    def get_default_attr(self) -> dict:
        default_attr = {}
        for cls in self.__class__.__mro__:
            default_attr = {**getattr(cls, 'default_attr', {}), **default_attr}
        return default_attr

    def __getitem__(self, attr) -> Any:
        return getattr(self, attr)

    def __setitem__(self, attr: str, value) -> None:
        setattr(self, attr, value)

    def __iter__(self, *args):
        next_entities = Card_list()
        for ent in args or self.entities:
            next_entities += ent.entities
            yield ent
        if next_entities:
            yield from self.__iter__(*next_entities)

    @property
    def in_fight_sequence(self) -> bool:
        return self.game.current_sequence == 'FIGHT'

    def no_method(self, *args, **kwargs):
        pass

    @property
    def all_cards(self) -> Meta_card_data:
        return self.game.all_cards

    @property
    def level(self) -> int:
        return self.techLevel

    def reset(self, dbfId=None) -> None:
        self.__init__(dbfId or self.dbfId)

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

    def append(self, entity: 'Entity', **kwargs) -> None:
        entity.owner.remove(entity)
        entity.owner = self
        self.entities.append(entity)

    def remove(self, entity: 'Entity') -> None:
        try:
            entity.owner.entities.remove(entity)
        except ValueError:
            pass

    def create_card_in(self, dbfId: int, position=None, **kwargs) -> 'Entity':
        """
            Create card and append it in self
        """
        card_id = self.create_card(dbfId, **kwargs)
        self.append(card_id)
        return card_id

    def create_card(self, dbfId: int, **kwargs) -> 'Entity':
        card_id = Card(dbfId, **kwargs)
        card_id.owner = self.controller
        return card_id

    def buff(self, target: 'Entity', enchantmentDbfId: int = 0, **kwargs) -> None:
        enchantmentDbfId = enchantmentDbfId or self.enchantmentDbfId
        if target:
            Sequence(
                'ENHANCE',
                Card(enchantmentDbfId, source=self, **kwargs),
                target=target
            ).start_and_close()

    @property
    def controller(self) -> 'Entity':
        return controller(self)

    @property
    def my_zone(self) -> 'Entity':
        return my_zone(self)

    @property
    def game(self):
        return game(self)

    @property
    def attack(self) -> int:
        return getattr(self, '_attack', None)

    @attack.setter
    def attack(self, value) -> None:
        self._attack = value

    @property
    def position(self) -> int:
        if self.type <= Type.ZONE:
            return 0
        return self.my_zone.cards.index(self)
        """
        try:
            return self.my_zone.cards.index(self)
        except (ValueError, AttributeError):
            pass
        return None
        """

    @property
    def can_attack(self) -> bool:
        return getattr(self, 'attack', 0) > 0

    def how_many_time_can_I_attack(self) -> int:
        if self.can_attack:
            if self.WINDFURY:
                if self.MEGA_WINDFURY:
                    return 4
                return 2
            return 1
        return 0

    @property
    def nb_turn(self) -> int:
        return self.game._turn

    def all_in_bob(self) -> None:
        """
            All cards in self.entities are removed and
            go back to game.hand (if possible)
        """
        for entity in self.entities[::-1]:
            self.game.hand.append(entity)

    def adjacent_neighbors(self) -> Card_list:
        position = self.position

        if position is not None:
            zone = self.my_zone.cards
            if position == 0:
                if zone[1]:
                    return Card_list(zone[1])
            else:
                return Card_list(
                    minion
                    for minion in zone[position-1:position+2:2]
                    if minion)

        return Card_list()

    @property
    def has_frenzy(self) -> bool:
        return self.FRENZY and self.is_alive

    @property
    def is_alive(self) -> bool:
        return True

    def calc_stat_from_scratch(self, heal=False) -> None:
        if self.DORMANT:
            return None

        old_health = self.health
        old_mechanics = {
            mechanic: getattr(self, mechanic, False)
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

    def active_script_arene(self, *args, strat='', **kwargs) -> None:
        if self.type == Type.HERO_POWER:
            met = getattr(hero_arene, self.hero_script)
            if met:
                met_turn = getattr(met, f'turn_{self.nb_turn}', None)
                if met_turn:
                    met_turn(self.owner, *args, **kwargs)
        elif self.type == Type.MINION:
            met = getattr(minion_arene, self.id)
            if met:
                getattr(
                    getattr(met, strat),
                    f'turn_{self.nb_turn}'
                )(self, *args, **kwargs)

    def damage(
            self,
            target: 'Entity',
            damage_value: int,
            overkill=False) -> None:
        with Sequence(
                'HIT',
                self,
                target=target,
                damage_value=damage_value,
                position=self.position) as seq:
            if seq.is_valid and target.IMMUNE is False\
                    and target.DORMANT is False:
                if target.DIVINE_SHIELD:
                    with Sequence('LOSS_SHIELD', target) as loss_shield_seq:
                        if loss_shield_seq.is_valid:
                            target.DIVINE_SHIELD = False
                            seq.damage_value = 0

                if seq.damage_value > 0:
                    real_damage = seq.damage_value - target.armor
                    target.armor = max(0, -real_damage)
                    target.health -= real_damage
                    target.IS_POISONED &= self.POISONOUS  # TODO: delete IS_POISONED
                    if not target.is_alive:
                        if target.health < 0 and overkill:
                            Sequence('OVERKILL', self).start_and_close()
                    elif target.FRENZY:
                        target.FRENZY = False
                        Sequence('FRENZY', target).start_and_close()

    def discover(
            self,
            card_list: Card_list,
            nb: int = 3,
            player: 'Entity' = None,
            remove: bool = True
    ) -> Card_data:
        """
            Entit?? source, son dbfId est exclu de la d??couverte
            Card_list sur laquelle effectuer les recherches
            player qui choisit la carte
            nombre de carte dans la d??couverte
        """

        if nb <= 0:
            return None

        list_card_choice = Card_list()
        for card in card_list.exclude(self.dbfId).shuffle():
            if card not in list_card_choice:
                list_card_choice.append(card)
                if remove:
                    self.game.hand.remove(card)
                if nb <= 1:
                    break
                nb -= 1

        chosen_card = list_card_choice.choice(player or self.controller)

        if remove:
            for card in list_card_choice:
                self.game.hand.create_card_in(card)

        return chosen_card

    @khadgar_aura
    def invoc(self, sequence: Sequence, repopDbfId: int) -> 'Entity':
        minion_id = self.create_card(repopDbfId)
        if sequence.source in self.controller.board.cards:
            sequence.position += 1

        minion_id.summon(position=sequence.position)
        if minion_id not in self.controller.board:
            # ??chec de la s??quence summon
            return None

        return minion_id


class Minion(Entity):
    default_attr = {
    }

    def __init__(self, dbfId, **kwargs):
        super().__init__(dbfId, cards=Card_list(), **kwargs)
        self._max_health = self.health

    def __repr__(self) -> str:
        return f'{self.name} {self.attack}-{self.health}'

    @property
    def max_health(self) -> int:
        return self._max_health

    @max_health.setter
    def max_health(self, value) -> None:
        if value is not None:
            bonus = value - self.max_health
            self._max_health = value
            if bonus >= 0:
                self.health += bonus
            else:
                self.health = min(self.health, value)

    @property
    def level(self) -> int:
        if not hasattr(self, 'techLevel') and\
                getattr(self, 'battlegroundsNormalDbfId'):
            return self.battlegroundsNormalDbfId.level
        return getattr(self, 'techLevel', 1)

    def all_in_bob(self) -> None:
        super().all_in_bob()
        for card in self.cards:
            self.game.hand.append(card)

    @property
    def is_premium(self) -> bool:
        return hasattr(self, 'battlegroundsNormalDbfId')

    def play(self, sequence=None, **kwargs):
        if sequence is None:
            kwargs['position'] = kwargs.get('position', None)
            with Sequence('PLAY', self, **kwargs) as seq:
                if seq.is_valid:
                    with Sequence('SUMMON', self, **kwargs):
                        Sequence(
                            'BATTLECRY',
                            self,
                            target=seq.target,
                            position=self.position
                        ).start_and_close()
        elif self.is_premium:
            self.controller.draw(
                CardName.TRIPLE_REWARD,
                quest_value=min(self.controller.level+1, LEVEL_MAX))

    def die(self, sequence=None, **kwargs):
        if sequence is None:
            kwargs['position'] = self.position
            with Sequence('DIE', self, **kwargs) as seq:
                if seq.is_valid:
                    Sequence('DEATHRATTLE', self, **kwargs).start_and_close()
                    # Avenge s'active avant le die off
                    Sequence('AVENGE', self, **kwargs).start_and_close()

            Sequence('REBORN', self, **kwargs).start_and_close()

    def play_start(self, sequence: Sequence):
        if self.my_zone.zone_type != Zone.HAND and\
                self.controller.type != Type.BOB:
            sequence.is_valid = False
            print(
                f'Carte {self.name} non jou??e : ' +
                f'zone_type {self.my_zone.zone_type} {self.my_zone}'
            )
            return None
        elif self.in_fight_sequence:
            sequence.is_valid = False
            return None

        if self.controller.board.can_add_card(self):
            self.owner.remove(self)
            # + paid cost

            # MODULAR > Sequence ??
            if self.MODULAR and sequence.position is not None:
                target = self.controller.board.cards[sequence.position]
                if target.race.MECHANICAL:
                    sequence.modular_target = target
            #
        else:
            sequence.is_valid = False

    def play_end(self, sequence: Sequence):
        self.controller.played_cards[self.nb_turn] += self
        self.modular(sequence)

    def modular(self, sequence: Sequence) -> None:
        # copie des caract??ristiques ou application des enchantements ?
        # les enchantements non buff sont-ils conserv??s ?
        modular_target = getattr(sequence, 'modular_target', None)
        if modular_target is None:
            return None

        self.buff(
            modular_target,
            attack=self.attack,
            max_health=self.health,
            mechanics=self.mechanics)
        self.my_zone.cards.remove(self)
        modular_target.cards.append(self)

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
                for entity in self.controller.field:
                    if entity.type == Type.ENCHANTMENT and\
                            entity.aura and\
                            entity.source is self:
                        sequence(entity.remove)
            sequence(self.controller.graveyard.append, self)
        else:
            sequence.is_valid = False
            print('humm die in', self.owner.id, self)

    def copy_enchantment_from(self, source: Entity) -> None:
        for entity in source.entities:
            if entity.type == Type.ENCHANTMENT and\
                    not getattr(entity, 'aura', False):
                enchant = Card(**entity.__dict__)
                self.append(enchant)
                enchant.apply()

    def replace(self, substitute: 'Entity') -> None:
        # TODO: un minion gel?? puis remplac?? doit pouvoir rester gel??
        # TODO: activer les auras
        position = self.position
        old_zone = self.owner
        self.all_in_bob()
        self.game.hand.append(self)
        old_zone.append(substitute, position=position)

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
                Sequence('COMBAT', self, target=seq.target).start_and_close()

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
            target = sequence.target
            position = target.position
            if target.owner.cards[position-1]:
                sequence(
                    self.damage,
                    target.owner.cards[position-1],
                    self.attack,
                    overkill=True
                )
            sequence(attack, sequence)
            if target.owner.cards[position+1]:
                sequence(
                    self.damage,
                    target.owner.cards[position+1],
                    self.attack,
                    overkill=True
                )
        else:
            sequence(attack, sequence)

    def search_fight_target(self) -> Entity:
        opponent_board = self.my_zone.opponent.cards.\
            exclude(is_alive=False, DORMANT=True)

        return (opponent_board.filter(TAUNT=True) or opponent_board).random_choice()

    def loss_shield_start(self, sequence: Sequence) -> None:
        sequence.is_valid = self.DIVINE_SHIELD

    def set_premium(self) -> 'Entity':
        if hasattr(self, 'battlegroundsPremiumDbfId') is False:
            return None
        # TODO: l'origine de la carte est erron?? si
        # une nouvelle carte ne remplace pas l'ancienne
        # Dans ce cas, des informations utiles peuvent ??tre perdues
        # d'apr??s les observations en date du 30/11/2021, une nouvelle carte est cr????e

        owner = self.owner
        position = self.position
        self.owner.remove(self)
        card_id = Card(self.battlegroundsPremiumDbfId)
        card_id.cards.append(self)
        for entity in self.entities:
            card_id.append(entity)
            entity.apply()
        owner.append(card_id, position=position)
        return card_id

    def clone(self) -> Entity:
        clone_card = self.create_card(self.dbfId)
        clone_card.copy_enchantment_from(self)
        for mechanic in self.mechanics:
            setattr(clone_card, mechanic, True)
        clone_card.health = self.health
        return clone_card

    @khadgar_aura
    def reborn(self, sequence) -> Entity:
        minion = self.create_card(self.dbfId)
        minion.REBORN = False
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
    # TODO: fusion des enchantements de dbfId identiques ?
    # > g??ne la r??troactivit?? des bonus
    # > pas de r??troactivit?? des bonus
    default_attr = {
        'aura': False,
        'source': Void(),
    }

    def __init__(self, dbfId, **kwargs):
        super().__init__(dbfId, **kwargs)
        if not hasattr(self, 'duration'):
            if self.source.in_fight_sequence:
                self.duration = 0
            else:
                self.duration = MAX_TURN
        elif self.duration == -1:
            self.duration = MAX_TURN
        else:
            self.duration += self.source.nb_turn

    @property
    def is_over(self) -> bool:
        return self.duration <= self.nb_turn and self.duration != 0

    def enhance_start(self, sequence: Sequence) -> None:
        target = sequence.target
        if target is None or target.DORMANT or\
                self.duration <= target.nb_turn and self.duration != 0:
            sequence.is_valid = False
            return None

        target.append(self)
        self.apply()

    def apply(self) -> None:
        pass

    def remove(self):
        old_owner = self.owner
        super().remove(self)
        # uniquement si en cas de modification de caract??ristiques ?
        if old_owner.type == Type.MINION:
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
        self.is_enabled = getattr(self, 'remain_use', 1) > 0

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
        return self.controller.board

    @property
    def hand(self) -> Entity:
        return self.controller.hand

    def change(self, dbfId, **kwargs) -> None:
        # TODO: test
        new_power_id = self.create_card(dbfId, **kwargs)
        if new_power_id.type == Type.HERO_POWER:
            self.owner.remove(self)
            self.owner.append(new_power_id)
            self.owner.power = new_power_id


class Spell(Entity):
    default_attr = {
    }

    def play(self, sequence=None):
        if sequence is None:
            if not self.in_fight_sequence and\
                    self.cost <= self.controller.gold:
                self.controller.gold -= self.cost
                with Sequence('PLAY', self) as seq:
                    # TODO: counterspell effect ?
                    if seq.is_valid:
                        if self.SECRET is False:
                            self.cast(seq)
                            self.owner.remove(self)
                            self.controller.graveyard.append(self)
                        else:
                            self.controller.secret_board.append(self)

    def die(self, sequence=None):
        self.controller.graveyard.append(self)


class Card:
    def __new__(cls, dbfId, **kwargs):
        from .scripts import event
        # ok = dbCard.objects.filter(pk=int(dbfId)) # retro3 base_T1 > 37s > 53s
        self = getattr(event, str(CardDB()[dbfId].id))
        return self(dbfId, **kwargs)
