
from base.utils import Card_list
from .entity import Entity
from .enums import Type

class Zone(Entity):
    default_attr = {
        'type': Type.ZONE,
    }

    def __init__(self, dbfId, **kwargs):
        super().__init__(dbfId, **{**self.default_attr, **kwargs})

    def __len__(self) -> int:
        return len(self.cards)

    @property
    def size(self) -> int:
        return len(self.cards)

    @property
    def is_full(self) -> bool:
        """
            Returns a boolean indicating if it is possible to add a card to player's hand
        """
        return getattr(self, 'MAX_SIZE') and self.size >= self.MAX_SIZE

