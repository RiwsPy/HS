from base.db_card import Meta_card_data
from .enums import Type, LEVEL_MAX, HAND_SIZE, CardName, Zone
from .entity import Entity
from typing import Generator, Any
from itertools import chain
from .utils import Card_list, Board_Card_list
from .sequence import Sequence
from .zone import Zone as ZoneEntity

class Player_hand(ZoneEntity):
    default_attr = {
        'zone_type': Zone.HAND,
    }
    MAX_SIZE = HAND_SIZE

    def __init__(self, **kwargs) -> None:
        super().__init__(CardName.DEFAULT_HAND, **{**self.default_attr, **kwargs})
        self.cards = Board_Card_list()
        self.cards.owner = self

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

    def remove(self, entity: Entity) -> None:
        super().remove(entity)
        try:
            self.cards.remove(entity)
        except ValueError:
            pass

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

class Bob_hand(ZoneEntity):
    default_attr = {

    }

    def __init__(self, **kwargs) -> None:
        super().__init__(CardName.DEFAULT_HAND, entities=[
            Meta_card_data(),
            Meta_card_data(),
            Meta_card_data(),
            Meta_card_data(),
            Meta_card_data(),
            Meta_card_data(),
            Meta_card_data()],
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
            self.entities[entity.level].append(entity.dbfId)

    def remove(self, entity: Entity) -> None:
        """
            Remove one card from bob's hand
        """
        if isinstance(entity, int):
            entity = self.all_cards[entity]
        else:
            print('BOB board remove entity ??')
        self.entities[entity.level].remove(entity.dbfId)

    def remove_and_create(self, dbfId: int) -> Entity:
        try:
            self.remove(dbfId)
        except ValueError:
            return self.create_card(dbfId)
        return self.create_card(dbfId, from_bob=True)

    @property
    def cards(self) -> Card_list:
        return self.cards_of_tier_max()

    def __iter__(self) -> Generator:
        yield from (i for i in self.cards)

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

    def create_card_in(self, dbfId: int, position=None, **kwargs) -> None:
        """
            Create a copy of each card in ``entities_id`` parameter to bob's hand
        """
        dbfId_data = self.all_cards[dbfId]
        if dbfId_data.level:
            self.entities[dbfId_data.level].append(dbfId_data)

    def give_or_create_in(self, dbfId: int, new_owner, **kwargs) -> Entity:
        try:
            dbfId_data = self.all_cards[dbfId]
        except ValueError:
            return None

        if dbfId_data.level:
            in_bob = dbfId in self.cards
            if in_bob:
                self.remove(dbfId)
            card_id = new_owner.create_card_in(dbfId, from_bob=in_bob, **kwargs)
        else:
            card_id = new_owner.create_card_in(dbfId, **kwargs)

            normal_dbfId = dbfId_data.battlegroundsNormalDbfId
            if normal_dbfId:
                for _ in range(3):
                    card_id.cards.append(
                        self.remove_and_create(normal_dbfId)
                    )

        return card_id
