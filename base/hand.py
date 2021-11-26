from .enums import Type, LEVEL_MAX, HAND_SIZE, CardName, Zone
from .entity import Entity
from typing import Generator, Any
from itertools import chain
from .utils import Card_list
from .sequence import Sequence

class Player_hand(Entity):
    default_attr = {
        'zone_type': Zone.HAND,
    }
    MAX_SIZE = HAND_SIZE

    def __init__(self, **kwargs) -> None:
        super().__init__(CardName.DEFAULT_HAND, **{**self.default_attr, **kwargs})
        self.cards = Card_list()

    def append(self, entity: Entity, **kwargs) -> None:
        """
            Try to add card to player's hand, remove it from the current owner (if any)
        """
        if not self.is_full and entity.type.can_be_add_in_hand:
            #Sequence('ADD_CARD_IN_HAND', entity).start_and_close()
            super().append(entity)
            self.cards.append(entity)
        # + entity.die() if can't be added ?
        # voir commentaire si une carte ne peut être ajoutée dans la main avec le pouvoir de Maiev

    @property
    def size(self) -> int:
        return len(self.cards)

    def remove(self, entity: Entity) -> None:
        super().remove(entity)
        try:
            self.cards.remove(entity)
        except ValueError:
            pass

    @property
    def is_full(self) -> bool:
        """
            Returns a boolean indicating if it is possible to add a card to player's hand
        """
        return self.size >= self.MAX_SIZE

    def auto_play(self) -> None:
        self.cards.sort(
            key=lambda x:(
                x.type == Type.MINION,
                hasattr(x, 'summon_off'), # Maman des ours
                hasattr(x, 'play_on'), # Pillard pirate
                hasattr(x, 'play_off') and\
                    hasattr(x, 'enchantmentDbfId') and\
                    ((x.enchantmentDbfId.attack or 0) + \
                    (x.enchantmentDbfId.max_health or 0)), # Élémentaire de fête
                hasattr(x, 'play_off'), # Sanglier
                x.AURA,
                not x.MODULAR,
                not x.BATTLECRY,
                hasattr(x, 'battlecry_on'), # Brann
                x.BATTLECRY and hasattr(x, 'repopDbfId'),
                -x.level))

        for card in self.cards[::-1]:
            card.play()
        if self.size > 0:
            self.auto_play()

class Bob_hand(Entity):
    default_attr = {

    }
    MAX_SIZE = 9999

    def __init__(self, **kwargs) -> None:
        super().__init__(CardName.DEFAULT_HAND, entities=[
            Card_list(),
            Card_list(),
            Card_list(),
            Card_list(),
            Card_list(),
            Card_list(),
            Card_list(),],
            **kwargs)

    def __getitem__(self, value) -> Any:
        return self.entities[value]

    def append(self, entity: Entity, **kwargs) -> None:
        """
            Try to add card to bob's hand, remove it from the current owner (if any)
            in order to be the same to Player_hand ``append`` method
            A new card is added to Bob hand
            *param entities: card_ids to append
            *type entities: entity.Card
        """
        entity.owner.remove(entity)
        for ent in entity.entities[::-1]:
            self.append(ent)
        if entity.from_bob:
            self.create_card_in(entity.dbfId)

    def remove(self, entity: Entity) -> None:
        """
            Remove one card from bob's hand
        """
        self.entities[entity.level].remove(entity)

    def discard(self, dbfId: int) -> Entity:
        """
            Take out one card with ``dbfId`` of bob's hand
            Only used by statistical algorithms
            *param key: card_key_number to remove
            *type key: str
            *return: card_id (or None if ``key`` doesn't exist)
            *rtype: entity.Card
        """
        entity = self.search(dbfId)
        if entity:
            self.remove(entity)
        return entity

    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self) -> Generator:
        yield from (i for i in self.cards)

    @property
    def is_full(self) -> bool:
        """
            Returns a boolean indicating if it is possible to add a card to bob's hand
        """
        return False

    @property
    def size(self) -> int:
        return len(self.cards)

    def cards_of_tier_max(self, tier_max=LEVEL_MAX, tier_min=1) -> Card_list:
        """
            Return all cards in bob's hand with ``tier_min`` <= tier_card <= ``tier_max``
            *param tier_max: maximum level of wanted cards
            *param tier_min: minimum level of wanted cards
            *type tier_max: int
            *type tier_min: int
            *rtype: utils.Card_list
        """
        return Card_list(*chain(*self.entities[tier_min:tier_max+1]))

    @property
    def cards(self) -> Card_list:
        return self.cards_of_tier_max()

    def create_card_in(self, dbfId: int, position=None, **kwargs) -> Entity:
        """
            Create a copy of each card in ``entities_id`` parameter to bob's hand
        """
        card_id = self.create_card(dbfId, **kwargs, from_bob=True)
        card_id.owner = self
        self.entities[card_id.level].append(card_id)
        return card_id

    def search(self, dbfId: int) -> Entity:
        card_lvl = self.all_cards[dbfId].techLevel
        if card_lvl:
            for entity in self.entities[card_lvl]:
                if entity.dbfId == dbfId:
                    return entity
        return None

    def give_or_create_in(self, dbfId: int, new_owner) -> Entity:
        dbfId_data = self.all_cards[dbfId]

        if dbfId_data.level:
            card_id = self.search(dbfId) or self.create_card(dbfId)
            if card_id is None:
                card_id = new_owner.create_card_in(dbfId)
            else:
                # TODO: test
                new_owner.append(card_id)
        elif dbfId_data.battlegroundsPremiumDbfId: # plain cant_collect card
            card_id = new_owner.create_card_in(dbfId)
        else: # golden card
            card_id = new_owner.create_card_in(dbfId)
            normal_dbfId = dbfId_data.battlegroundsNormalDbfId
            if normal_dbfId:
                for _ in range(3):
                    plain_card = self.discard(normal_dbfId)
                    if plain_card:
                        card_id.cards.append(plain_card)
                    else:
                        break

        return card_id
