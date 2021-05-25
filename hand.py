import constants
import bob
import player
import card

class Player_hand(list):
    def __init__(self, owner):
        list.__setitem__(self, slice(None), [])
        self.owner = owner

    def append(self, card, position=None):
        if self.can_add_card():
            if card.owner:
                card.owner.remove(card)
            super().append(card)
            card.owner = self
            return True
        return False

    def can_add_card(self):
        return len(self) < constants.HAND_SIZE

    def create_card(self, *keys_number, atk_bonus=0, def_bonus=0):
        # crée une carte sur le board mais sans la jouer
        for nb in keys_number:
            card_id = card.Card(nb, self.owner.bob)
            card_id.attack += atk_bonus
            card_id.health += def_bonus
            self.append(card_id)
        return card_id


class Bob_hand(list):
    # bob.hand renvoie une liste contenant toutes les cartes de Bob
    # bob.hand.hand renvoie la liste selon leur niveau
    def __init__(self, owner):
        # un set / niveau (dont 0)
        list.__setitem__(self, slice(None), [[], [], [], [], [], [], []])
        self.owner = owner

    def append(self, card, position=None):
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

    def remove(self, card):
        self[card.level].remove(card)

    def discard(self, key):
        minion_info = self.owner.all_card.get(key)
        if minion_info:
            for card in self[minion_info['level']]:
                if card.key_number == key:
                    self.remove(card)
                    card.owner = None
                    return card
        return None

    def __len__(self):
        return len(self.cards_of_tier_max())

    def __iter__(self):
        yield from (i for i in self.cards_of_tier_max())

    def all_cards(self):
        # renvoie toutes les cartes de la main
        return self.cards_of_tier_max()

    def can_add_card(self):
        return True

    def nb_cards_of_tier_max(self, tier_max=constants.LEVEL_MAX, tier_min=1):
        nb = 0
        for cards in self[tier_min:tier_max+1]:
            nb += len(cards)
        return nb

    def cards_of_tier_max(self, tier_max=constants.LEVEL_MAX, tier_min=1):
        """
            *rtype: list
        """
        # renvoie toutes les cartes de la main de bob de tier inférieur ou égal à tier_max et inférieur ou égal à tier_min
        result = []
        for cards in self[tier_min:tier_max+1]:
            result += cards
        return result

    def cards_of_tier(self, tier):
        return self[min(constants.LEVEL_MAX, max(1, tier))]

    def cards_type_of_tier_max(self, typ=0, tier_max=constants.LEVEL_MAX, tier_min=1):
        lst = self.cards_of_tier_max(tier_max, tier_min)
        return [crd
            for crd in lst
                if crd.type & typ and tier_min <= crd.level <= tier_max]

    def create_card(self, *keys_number, atk_bonus=0, def_bonus=0):
        # crée une carte sur le board mais sans la jouer
        for nb in keys_number:
            card_id = card.Card(nb, self.owner.bob, owner=self)
            card_id.attack += atk_bonus
            card_id.health += def_bonus
            self.append(card_id)
        return card_id
