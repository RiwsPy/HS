import constants
import card

class Player_hand(list):
    def __init__(self, owner):
        list.__setitem__(self, slice(None), [])
        self.owner = owner

    def append(self, card, position=None) -> bool:
        """
            Try to add card to player's hand, remove it from the current owner (if any)
            position parameter is inconsistent,
            *param card: card_id to append
            *type card: card.Card
            *return: True if the card is added, False otherwise
            *rtype: bool
        """
        if self.can_add_card():
            if card.owner:
                try:
                    card.owner.remove(card)
                except ValueError:
                    pass
            super().append(card)
            card.owner = self
            return True
        return False

    def can_add_card(self) -> bool:
        """
            Returns a boolean indicating if it is possible to add a card to player's hand
            *rtype: bool
        """
        return len(self) < constants.HAND_SIZE

    def create_card(self, *keys_number, atk_bonus=0, def_bonus=0) -> card:
        """
            Create a copy of each card in ``keys_number`` parameter to bob's hand
            *param atk_bonus: attack bonus for each card
            *param def_bonus: health_bonus for each card
            *typ atk_bonus: int
            *typ def_bonus: int
            *return: last card_id created
            *rtype: card.Card
        """
        card_id = None
        for nb in keys_number:
            card_id = card.Card(nb, self.owner.bob)
            card_id.attack += atk_bonus
            card_id.max_health += def_bonus
            card_id.health += def_bonus
            self.append(card_id)
        return card_id


class Bob_hand(list):
    # bob.hand renvoie une liste contenant toutes les cartes de Bob
    # bob.hand.hand renvoie la liste selon leur niveau
    def __init__(self, owner) -> None:
        # un set / niveau (dont 0)
        list.__setitem__(self, slice(None), [[], [], [], [], [], [], []])
        self.owner = owner

    def append(self, card, position=None) -> bool:
        """
            Try to add card to bob's hand, remove it from the current owner (if any)
            position parameter is inconsistent,
            in order to be the same to Player_hand ``append`` method
            Card is reset before being added to Bob hand
            *param card: card_id to append
            *type card: card.Card
            *return: True if the card is added, False otherwise
            *rtype: bool
        """
        if card.owner:
            try:
                card.owner.remove(card)
            except ValueError:
                pass
        if card.from_bob:
            card.reinitialize() # la carte perd tous ses bonus
            self[card.level].append(card)
            card.owner = self
        else:
            card.owner = None
        return True

    def remove(self, card) -> None:
        """
            Remove one card from bob's hand
            *param card: card_id to remove
            *type card: card.Card
            *return: None
        """
        self[card.level].remove(card)

    def discard(self, key) -> card:
        """
            Take out one card with ``key`` of bob's hand
            Only used by statistical algorithms
            *param key: card_key_number to remove
            *type key: str
            *return: card_id (or None if ``key`` doesn't exist)
            *rtype: card.Card
        """
        minion_info = self.owner.all_card.get(key)
        if minion_info:
            for card in self[minion_info['level']]:
                if card.key_number == key:
                    self.remove(card)
                    card.owner = None
                    return card
        return None

    def __len__(self) -> int:
        return len(self.all_cards())

    def __iter__(self):
        yield from (i for i in self.all_cards())

    def can_add_card(self) -> bool:
        """
            Returns a boolean indicating if it is possible to add a card to bob's hand
            *return: True (always)
            *rtype: bool
        """
        return True

    def nb_cards_of_tier_max(self, tier_max=constants.LEVEL_MAX, tier_min=1) -> int:
        """
            Returns number of cards between tier_min and tier_max to bob's hand
            Only used by statistical algorithms
            *param tier_max: card maximum level
            *param tier_min: card minimum level
            *type tier_max: int
            *type tier_min: int
            *rtype: int
        """
        nb = 0
        for cards in self[tier_min:tier_max+1]:
            nb += len(cards)
        return nb

    def cards_of_tier_max(self, tier_max=constants.LEVEL_MAX, tier_min=1) -> list:
        """
            Return all cards in bob's hand with ``tier_min`` <= tier_card <= ``tier_max``
            *param tier_max: maximum level of wanted cards
            *param tier_min: minimum level of wanted cards
            *type tier_max: int
            *type tier_min: int
            *rtype: list
        """
        result = []
        for cards in self[tier_min:tier_max+1]:
            result += cards
        return result
    all_cards = cards_of_tier_max

    def cards_type_of_tier_max(self, typ=0, tier_max=constants.LEVEL_MAX, tier_min=1) -> list:
        """
            Return all cards with matching type ``typ`` in bob's hand
            with ``tier_min`` <= tier_card <= ``tier_max``

            Similar to ``cards_of_tier_max`` with optional ``typ`` parameter
            *typ: type of wanted cards
            *param tier_max: maximum level of wanted cards
            *param tier_min: minimum level of wanted cards
            *type typ: int
            *type tier_max: int
            *type tier_min: int
            *rtype: list
        """
        if not typ:
            return self.cards_of_tier_max(tier_max=tier_max, tier_min=tier_min)

        return [crd
            for crd in self.cards_of_tier_max(tier_max, tier_min)
                if crd.type & typ]

    def create_card(self, *keys_number, atk_bonus=0, def_bonus=0) -> card:
        """
            Create a copy of each card in ``keys_number`` parameter to bob's hand
            *param atk_bonus: attack bonus for each card
            *param def_bonus: health_bonus for each card
            *typ atk_bonus: int
            *typ def_bonus: int
            *return: last card_id created
            *rtype: card.Card
        """
        card_id = None
        for key_number in keys_number:
            card_id = card.Card(key_number, self.owner, owner=self)
            card_id.attack += atk_bonus
            card_id.max_health += def_bonus
            card_id.health += def_bonus
            self.append(card_id)
        return card_id
