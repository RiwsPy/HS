from utils import Card_list, Board_Card_list, hasevent
from constants import General, NB_CARD_BY_LEVEL, State, Event, Type, Zone, BATTLE_SIZE, SECRET_SIZE, LEVEL_MAX
from entity import Card
import random
import script_event
from collections import defaultdict
from entity import Entity
from typing import List
from operator import itemgetter

#TODO: bloquer les fonctions manuelles board en cours de combat
class Board(Entity):
    default_attr = {
        'general': General.ZONE,
        'zone_type': Zone.PLAY,
        'opponent': None,
        'next_opponent': None, # adversaire rencontré après un end_turn
        'last_opponent': None,

    }
    def __init__(self, **kwargs):
        super().__init__("BOARD", **kwargs)
        self.cards = Board_Card_list()
        self.cards_copy = self.cards.__class__()
        self.entities_copy = self.entities.__class__()
        self.secret = defaultdict(set) # dict('0x1': set())
        #self.secret_key = []
        #self.enchantment = []

    @property
    def nb_minions(self):
        return len(self.cards.exclude(state=State.DORMANT))

    @property
    def level(self):
        return self.owner.level

    def remove(self, *cards):
        super().remove(*cards)
        for card in cards:
            #if card in self.cards:
            try:
                self.old_position = self.position
                self.cards.remove(card)
            except ValueError:
                print(f'{card} remove but not in {self}')
                return

            if hasevent(card, Event.PLAY_AURA):
                del self.controller.aura_active[card]
                card.apply_met_on_all_children(Entity.remove_my_aura_action, card.controller)
            for enchantment in card.entities:
                if getattr(enchantment, 'aura', False):
                    enchantment.remove()

    def append(self, card, position=BATTLE_SIZE) -> bool:
        # TODO : problème de positionnement en cas de repop multiple
        # faire pop avant le minion d'après ou en dernier en cas d'inexistance
        # TODO: gestion des secrets et sorts
        # comment exclure le repop de Khadgar d'une nouvelle invocation ?
        if card.owner is self and card in self.cards:
            if position != card.position:
                del self.cards[self.cards.index(card)]
                self.cards.insert(position, card)
            return True

        if not self.can_add_card(card):
            return False

        if card.general == General.MINION:
            old_owner = card.owner
            card.owner.remove(card)
            card.owner = self
            self.entities.append(card)
            self.cards.insert(position, card)
            card.active_aura()
            self.active_global_event(Event.INVOC, self.controller, source=card)
            if old_owner.zone_type == Zone.HAND and \
                    old_owner.owner is self.owner:
                self.active_global_event(Event.PLAY, self.controller, source=card)
                card.active_local_event(Event.BATTLECRY)
                if self.owner.general == General.HERO:
                    self.owner.played_minions[self.owner.nb_turn] += card
            return True

        return False

    def create_card_in(self, id, position=BATTLE_SIZE, **kwargs):
        """
            Create card and append it in self
        """
        card_id = Card(id, **kwargs)
        self.append(card_id, position)
        return card_id

    def can_add_card(self, card_id) -> bool:
        if card_id.general == General.MINION:
            return len(self.cards) <= BATTLE_SIZE-1

        if card_id.general == General.SPELL:
            if not card_id.state & State.SECRET:
                return True

            current_secrets = self.entities.filter_hex(state=State.SECRET)

            if len(current_secrets) >= SECRET_SIZE:
                return False

            return card_id.dbfId not in set(secret.dbfId for secret in current_secrets)

        return False

    def classification_by_type(self) -> dict:
        # exclu de fait les minions multi-type
        return {typ: self.cards.filter(type=typ)
            for typ in [0, 1, 2, 4, 8, 16, 32, 64, 128]}

    def one_minion_by_type(self) -> Card_list:
        """
            Return a set which contains until one minion by type
        """
        tri = self.classification_by_type()
        del tri[0] # exclusion des types neutres

        result = Card_list(random.choice(minions)
                for minions in tri.values()
                    if minions)

        return result + self.cards.filter(type=Type.ALL)

    def auto_placement_card(self) -> None:
        """
            Sort all cards in the board based on low intelligence algorithm
            self.cards is altered by the method
        """
        if len(self.cards) < 2:
            return None

        # placement initial de la plus forte attaque à la moins
        self.cards.sort(key=lambda x: (
                        not x.state & State.CLEAVE,
                        not x.event & Event.OVERKILL,
                        x.event & Event.DIE,
                        x.event & Event.INVOC,
                        x.event & Event.PLAY_AURA,
                        x.event & Event.HIT_BY,
                        not x.event & Event.DEATHRATTLE,
                        x.state & State.TAUNT,
                        -x.attack,
                        x.health))


class Bob_board(Board):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def freeze(self) -> None:
        if self.cards:
            if self.cards[0].state & State.FREEZE: # unfreeze
                for minion in self.cards:
                    minion.remove_attr(state=State.FREEZE)
            else: # freeze
                for minion in self.cards:
                    minion.state |= State.FREEZE

    def drain_minion(self) -> None:
        self.owner.hand.append(
            *self.cards.exclude_hex(state=State.STILL_BOB))

    def drain_all_minion(self) -> None:
        self.owner.hand.append(
            *self.cards.exclude_hex(state=State.DORMANT))

    def fill_minion(self, nb_card_to_play=0, entity_list=[]) -> None:
        nb_card_to_play = nb_card_to_play or (self.owner.nb_card_by_refresh - self.nb_minions)
        if nb_card_to_play >= 1:
            entity_list = entity_list or self.owner.local_hand
            random.shuffle(entity_list)
            for card_id in entity_list[:nb_card_to_play]:
                self.append(card_id)

    def fill_minion_battlecry(self) -> None:
        entity_list = self.owner.local_hand.filter_hex(event=Event.BATTLECRY)
        self.fill_minion(entity_list=entity_list)

    def fill_minion_temporal(self) -> None:
        bob = self.owner
        self.fill_minion(
            nb_card_to_play = \
            self.owner.nb_card_by_refresh - self.nb_minions - 1)

        lvl = min(LEVEL_MAX, bob.level+1)
        entity_list = bob.hand.cards_of_tier_max(tier_max=lvl, tier_min=lvl)
        if entity_list:
            self.append(random.choice(entity_list))

class Graveyard(Card_list):
    def __init__(self, owner):
        self.owner = owner
