from utils import Board_Card_list, Card_list
from enums import CardName, Type, Zone, BOARD_SIZE, SECRET_SIZE, LEVEL_MAX
import random
from entity import Entity
from typing import List, Generator
from sequence import Sequence

#TODO: bloquer les fonctions manuelles board en cours de combat
class Board(Entity):
    default_attr = {
        'type': Type.ZONE,
        'zone_type': Zone.PLAY,
        'next_opponent': None, # adversaire rencontré après un end_turn
        'last_opponent': None,
    }
    MAX_SIZE = BOARD_SIZE

    def __init__(self, dbfId, **kwargs):
        super().__init__(dbfId, **kwargs)
        self.purge()

        self.cards_copy = self.cards.__class__()
        self.entities_copy = self.entities.__class__()

    def __iter__(self) -> Generator:
        yield from (i for i in self.cards)

    def purge(self):
        self.cards = Board_Card_list()

    @property
    def opponent(self):
        return self.owner.opponent.board

    @property
    def size(self) -> int:
        return len(self.cards)

    @property
    def size_without_dormant(self) -> int:
        return len(self.cards.exclude(DORMANT=True))

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

    def append(self, entity: Entity, position=None) -> None:
        # TODO : problème de positionnement en cas de repop multiple
        # faire pop avant le minion d'après ou en dernier en cas d'inexistance ?
        if position is None:
            position = self.MAX_SIZE

        if entity.owner is self and entity in self.cards:
            if position != entity.position:
                del self.cards[self.cards.index(entity)]
                self.cards.insert(position, entity)
            return True

        if self.can_add_card(entity):
            super().append(entity)
            self.cards.insert(position, entity)

    def create_card_in(self, dbfId: int, position=None, **kwargs) -> Entity:
        """
            Create card and append it in self
        """
        card_id = self.create_card(dbfId, **kwargs)
        if self.can_add_card(card_id):
            self.append(card_id, position=position)
            return card_id
        return None

    @property
    def is_full(self) -> bool:
        return self.size >= self.MAX_SIZE

    def can_add_card(self, card_id) -> bool:
        return card_id.type.MINION and not self.is_full


class Player_board(Board):
    def turn_on(self, sequence):
        self.last_opponent = self.opponent
        #self.next_opponent = ??

    def fight_off(self, sequence):
        self.cards = self.cards_copy[:]
        self.entities = self.entities_copy[:]
        for card in self.entities:
            card.owner = self

    def turn_off(self, sequence):
        self.cards_copy = self.cards[:]
        self.entities_copy = self.entities[:]
        #if self.is_bot:
        if True:
            self.auto_placement_card()

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
                        x.DEATHRATTLE and not hasattr(x, 'repop_dbfId'),
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
        self.drain_all_minion()
        self.fill_minion()

    def freeze(self) -> None:
        if self.size > 0:
            is_freeze = self.cards[0].FREEZE
            for minion in self.cards:
                minion.FREEZE = not is_freeze

    def drain_minion(self) -> None:
        for minion in self.cards.exclude(FREEZE=True, DORMANT=True):
            self.owner.hand.append(minion)

    def drain_all_minion(self) -> None:
        for minion in self.cards.exclude(DORMANT=True):
            self.owner.hand.append(minion)

    def fill_minion(self, nb_card_to_play=0, entity_list=Card_list()) -> None:
        #TODO? Sequence REFRESH ??
        nb_card_to_play = (nb_card_to_play or \
            self.owner.opponent.nb_card_by_roll) - self.size_without_dormant
        entity_list = (entity_list or self.owner.local_hand).shuffle()
        while nb_card_to_play >= 1 and not self.is_full:
            nb_card_to_play -= 1
            card_id = entity_list[nb_card_to_play]
            card_id.owner = self.controller
            self.game.hand.remove(card_id)
            card_id.summon()

    def fill_minion_temporal(self) -> None:
        bob = self.owner
        self.fill_minion(
            nb_card_to_play = self.owner.nb_card_by_refresh - 1)

        lvl = min(LEVEL_MAX, bob.level+1)
        entity = bob.hand.cards_of_tier_max(tier_max=lvl, tier_min=lvl).random_choice()
        if entity:
            entity.owner = self.controller
            self.game.hand.remove(entity)
            entity.summon()

class Graveyard(Board):
    MAX_SIZE = 9999

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
        return entity.type == Type.SPELL and\
            entity.SECRET and not self.is_full and\
            entity.dbfId not in self.dbfId_list
