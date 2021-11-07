from utils import Board_Card_list
from enums import CardName, Type, Zone, FIELD_SIZE, SECRET_SIZE, LEVEL_MAX
import random
from entity import Entity, card_db
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
    MAX_SIZE = FIELD_SIZE

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

    def remove(self, *cards) -> None:
        super().remove(*cards)
        for card in cards:
            #if card in self.cards:
            try:
                self.cards.remove(card)
            except ValueError:
                print(f'{card} remove but not in {self}')
                return

            for enchantment in card.entities:
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
        if len(self.cards) < 2:
            return None

        # placement initial de la plus forte attaque à la moins
        self.cards.sort(key=lambda x: (
                        not x.CLEAVE,
                        not x.OVERKILL,
                        #not x.event & Event.ATK_ALLY,
                        #x.event & Event.DIE,
                        #x.event & Event.INVOC,
                        x.AURA,
                        #x.event & Event.HIT_BY,
                        not x.DEATHRATTLE,
                        x.TAUNT,
                        -x.attack,
                        x.health))



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

    def fill_minion(self, nb_card_to_play=0, entity_list=[]) -> None:
        #TODO? Sequence REFRESH ??
        nb_card_to_play = nb_card_to_play or (self.owner.opponent.nb_card_by_roll - self.size_without_dormant)
        if nb_card_to_play >= 1:
            entity_list = entity_list or self.owner.local_hand
            random.shuffle(entity_list)
            for card_id in entity_list[:nb_card_to_play]:
                card_id.owner = self.controller
                self.game.hand.remove(card_id)
                card_id.summon()

    def fill_minion_battlecry(self) -> None:
        entity_list = self.owner.local_hand.filter(BATTLECRY=True)
        self.fill_minion(entity_list=entity_list)

    def fill_minion_temporal(self) -> None:
        bob = self.owner
        self.fill_minion(
            nb_card_to_play = \
            self.owner.nb_card_by_refresh - self.size_without_dormant - 1)

        lvl = min(LEVEL_MAX, bob.level+1)
        entity_list = bob.hand.cards_of_tier_max(tier_max=lvl, tier_min=lvl)
        if entity_list:
            self.append(random.choice(entity_list))

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
