from constants import Zone, General, LEVEL_MAX, HAND_SIZE, CARD_NB_COPY
from entity import Card, Entity, card_db
from typing import List, Generator
from itertools import chain
from utils import Card_list

class Player_hand(Entity):
    default_attr = {

    }
    def __init__(self, **kwargs):
        super().__init__("HAND", **kwargs)
        self.cards = Card_list()

    def append(self, *entities, position=None) -> None:
        """
            Try to add card to player's hand, remove it from the current owner (if any)
            position parameter is inconsistent,
            *param card: card_id to append
            *type card: card.Card
        """
        if entities:
            for entity in entities[::-1]:
                if entity.general in (General.MINION, General.SPELL):
                    if self.can_add_card():
                        super().append(entity)
                        self.cards.append(entity)
                #elif entity.general != General.ZONE:
                #    super().append(entity)

    def remove(self, *entities) -> None:
        super().remove(*entities)
        for entity in entities:
            try:
                self.cards.remove(entity)
            except ValueError:
                pass

    def can_add_card(self, card=None) -> bool:
        """
            Returns a boolean indicating if it is possible to add a card to player's hand
            *rtype: bool
        """
        return len(self.cards) <= HAND_SIZE-1


class Bob_hand(Entity):
    default_attr = {

    }
    def __init__(self, **kwargs) -> None:
        super().__init__("HAND", entities=[
            Card_list(),
            Card_list(),
            Card_list(),
            Card_list(),
            Card_list(),
            Card_list(),
            Card_list(),],
            **kwargs)

    def append(self, *entities, position=None):
        """
            Try to add card to bob's hand, remove it from the current owner (if any)
            position parameter is inconsistent,
            in order to be the same to Player_hand ``append`` method
            Card is reset before being added to Bob hand
            *param entities: card_ids to append
            *type entities: entity.Card
            *return: True if the card is added, False otherwise
            *rtype: bool
        """
        for crd in entities[::-1]:
            crd.owner.remove(crd)
            self.append(*crd.entities)
            if crd.from_bob:
                self.create_card_in(crd.dbfId)
        return True

    def remove(self, *cards) -> None:
        """
            Remove one card from bob's hand
            *param card: card_id to remove
            *type card: entity.Card
            *return: None
        """
        for card in cards:
            #self.game.owner.append(card)
            self.entities[card.level].remove(card)

    def discard(self, id) -> Entity:
        """
            Take out one card with ``id`` of bob's hand
            Only used by statistical algorithms
            *param key: card_key_number to remove
            *type key: str
            *return: card_id (or None if ``key`` doesn't exist)
            *rtype: entity.Card
        """
        entity = self.search(id)
        if entity:
            self.remove(entity)
        return entity

    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self) -> Generator:
        yield from (i for i in self.cards)

    def can_add_card(self, card=None) -> bool:
        """
            Returns a boolean indicating if it is possible to add a card to bob's hand
            *return: True (always)
            *rtype: bool
        """
        return True

    def cards_of_tier_max(self, tier_max=LEVEL_MAX, tier_min=1) -> Card_list:
        """
            Return all cards in bob's hand with ``tier_min`` <= tier_card <= ``tier_max``
            *param tier_max: maximum level of wanted cards
            *param tier_min: minimum level of wanted cards
            *type tier_max: int
            *type tier_min: int
            *rtype: utils.Card_list
        """
        return Card_list(chain(*self.entities[tier_min:tier_max+1]))

    @property
    def cards(self) -> Card_list:
        return self.cards_of_tier_max()

    def create_card_in(self, *args, **kwargs) -> Card:
        """
            Create a copy of each card in ``entities_id`` parameter to bob's hand
            *return: last card_id created
            *rtype: entity.Card
        """
        card_id = None
        for id in args:
            card_id = Card(id, **kwargs, from_bob=True)
            card_id.owner = self
            self.entities[card_id.level].append(card_id)
        return card_id

    def search(self, id: str) -> Entity:
        if id in self.game.card_can_collect:
            card_lvl = self.card_db[id]['level']
            for entity in self.entities[card_lvl]:
                if entity.dbfId == id:
                    return entity
        return None
