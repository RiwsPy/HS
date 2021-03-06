from .utils import Board_Card_list, Card_list
from .enums import CardName, Type, Zone, BOARD_SIZE, SECRET_SIZE, LEVEL_MAX
import random
from .entity import Entity
from typing import List, Generator
from .sequence import Sequence
from .zone import Zone as ZoneEntity


class Board(ZoneEntity):
    default_attr = {
        'zone_type': Zone.PLAY,
        'next_opponent': None, # adversaire rencontré après un end_turn
    }
    MAX_SIZE = BOARD_SIZE

    def __init__(self, dbfId: int, **kwargs):
        super().__init__(dbfId, **kwargs)
        self.purge()

        self.cards_save = []
        self.entities_save = []

    #def __iter__(self) -> Generator:
    #    yield from (i for i in self.cards)

    def purge(self):
        self.cards = Board_Card_list()
        self.cards.owner = self

    @property
    def opponent(self):
        return self.owner.opponent.board

    @property
    def level(self) -> int:
        return self.owner.level

    @property
    def cumulative_level(self) -> int:
        return sum(entity.level for entity in self.cards)

    def remove(self, entity: Entity) -> None:
        super().remove(entity)
        try:
            self.cards.remove(entity)
        except ValueError:
            print(f'{entity} remove but not in {self}')
            return

        for enchantment in entity.entities:
            if getattr(enchantment, 'aura', False):
                enchantment.remove()

    def append(self, entity: Entity, position=None, **kwargs) -> None:
        if position is None:
            position = self.MAX_SIZE

        if entity.owner is self and entity in self.cards:
            if position != entity.position:
                del self.cards[self.cards.index(entity)]
                self.cards.insert(position, entity)
        elif self.can_add_card(entity):
            super().append(entity)
            self.cards.insert(position, entity)
        else:
            raise BoardAppendError

    def create_card_in(self, dbfId: int, position=None, **kwargs) -> Entity:
        """
            Create card and append it in self
        """
        card_id = self.create_card(dbfId, **kwargs)
        self.append(card_id, position=position)
        return card_id

    def can_add_card(self, card_id) -> bool:
        return card_id.type.MINION and not self.is_full


class Player_board(Board):
    @property
    def last_opponent(self) -> 'Board':
        if self.nb_turn > 1:
            for field in self.game.fights[self.nb_turn-1]:
                if self is field.p1.board:
                    return field.p2.board
                if self is field.p2.board:
                    return field.p1.board
        return None

    def turn_on(self, sequence):
        pass
        #self.next_opponent = ??

    #def fight_on(self, sequence):
    #    for entity in self.cards:
    #        entity.calc_stat_from_scratch(heal=True)


    def fight_off(self, sequence):
        # l'ordre d'exécution des scripts change au fil des tours
        # cela peut avoir pour origine une non sauvegarde de entities
        # qui serait calqué sur cards
        self.cards = self.cards_save[-1][:] # TODO: deepcopy ?? > excessif actuellement
        self.entities = self.entities_save[-1][:]
        for card in self.entities:
            card.owner = self
        for entity in self.cards:
            for enchant in entity.entities:
                if enchant.type == Type.ENCHANTMENT and\
                        enchant.duration == 0:
                    enchant.remove()
            entity.calc_stat_from_scratch(heal=True)

    def turn_off(self, sequence):
        #if self.is_bot:
        if True:
            self.auto_placement_card()
        self.cards_save.append(self.cards[:])
        self.entities_save.append(self.entities[:])

    def auto_placement_card(self) -> None:
        """
            Sort all cards in the board based on low intelligence algorithm
            self.cards is altered by the method
        """
        # Warning: Une carte comme Casseur Oméga se retrouvera à la fin
        if self.size >= 2:
            self.cards.sort(key=lambda x: (
                        hasattr(x, 'combat_start'),
                        hasattr(x, 'combat_end'),
                        x.DEATHRATTLE and not hasattr(x, 'repopDbfId'),
                        x.CLEAVE,
                        x.OVERKILL,

                        not x.TAUNT,
                        not hasattr(x, 'avenge'),
                        not hasattr(x, 'combat_on'),
                        not hasattr(x, 'die_off') or not hasattr(x, 'loss_shield_off'),
                        not hasattr(x, 'summon_off'),
                        not x.AURA,
                        not hasattr(x, 'hit'),
                        x.DEATHRATTLE,
                        x.attack,
                        -x.health),
                        reverse=True)



class Bob_board(Board):
    def can_add_card(self, card) -> bool:
        return card.type == Type.MINION and not self.is_full

    def turn_on(self, sequence: Sequence) -> None:
        if self.game.no_bob is False:
            self.fill_minion()

    def turn_off(self, sequence: Sequence) -> None:
        self.drain_minion()

    def roll(self, sequence: Sequence) -> None:
        self.drain_minion(freeze=True)
        self.fill_minion()

    def freeze(self) -> None:
        if self.size > 0:
            is_freeze = self.cards[0].FREEZE
            for minion in self.cards:
                minion.FREEZE = not is_freeze

    def drain_minion(self, freeze=False, dormant=False) -> None:
        cards = self.cards
        if not dormant:
            cards = cards.exclude(DORMANT=True)
        if not freeze:
            cards = cards.exclude(FREEZE=True)

        for minion in cards:
            self.owner.hand.append(minion)

    def fill_minion(self, nb_card_to_play=0, entity_list=Card_list()) -> None:
        #TODO? Sequence REFRESH ??
        nb_card_to_play = (nb_card_to_play or \
            self.owner.opponent.nb_card_by_roll) - len(self.cards.exclude(DORMANT=True))
        entity_list = (entity_list or self.owner.local_hand).shuffle()
        while nb_card_to_play >= 1 and not self.is_full:
            nb_card_to_play -= 1
            card_id = self.game.hand.give_or_create_in(entity_list[nb_card_to_play], self)
            card_id.summon()

    def fill_minion_temporal(self) -> None:
        self.fill_minion(
            nb_card_to_play=self.owner.nb_card_by_refresh - 1)

        lvl = min(LEVEL_MAX, self.owner.level+1)
        self.fill_minion(
            nb_card_to_play=1,
            entity_list=self.owner.hand.cards_of_tier_max(tier_max=lvl, tier_min=lvl))


class Graveyard(Board):
    default_attr = {
        'zone_type': Zone.GRAVEYARD,
    }

    def __init__(self, dbfId=CardName.DEFAULT_GRAVEYARD):
        super().__init__(dbfId)
        self.owner = None

    @property
    def is_full(self) -> bool:
        return False

    def can_add_card(self, card_id: Entity) -> bool:
        return True

    def turn_on(self, sequence: Sequence) -> None:
        self.purge()


class Secret_board(Board):
    MAX_SIZE = SECRET_SIZE

    @property
    def dbfId_list(self) -> List[int]:
        return [entity.dbfId for entity in self.cards]

    def can_add_card(self, entity: Entity) -> bool:
        return entity.SECRET and not self.is_full and\
            entity.dbfId not in self.dbfId_list


class BoardAppendError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)

    def __str__(self):
        return "Exception: the card can't be added."