import constants
import player
import bob
import hand
import card
import random
from collections import defaultdict

#TODO: bloquer les fonctions manuelles board en cours de combat
class Board(list):
    def __init__(self, owner):
        list.__setitem__(self, slice(None), [])
        self.owner = owner
        self.enchantment = {} # dict(card_id: {'bonus': value, 'restr_type': type})
        self.secret = defaultdict(set) # dict('0x1': set())
        self.secret_key = []
        self._opponent = None # pour Bob, id du joueur qui a accès à ce board

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except IndexError:
            pass
        return None

    @property
    def opponent(self):
        return self._opponent

    @opponent.setter
    def opponent(self, value):
        self.refresh_enchantment()
        self._opponent = value

    def copy(self, source):
        self.clear()
        self.extend(source)
        self.owner = source.owner
        self.opponent = source.opponent
        self.secret = source.secret.copy() # dict('0x1': set())

    def remove(self, card):
        if card.general == 'minion':
            card._position = card.position # sauvegarde
            try:
                super().remove(card)
            except ValueError:
                pass
            self.refresh_enchantment()
        elif card.general == 'secret':
            for key in card.script.keys():
                self.secret[key].discard(card)
            self.secret_key.remove(card.key_number)

    def append(self, card, position=constants.BATTLE_SIZE):
        if self.can_add_card() and card.general == 'minion':
            if card.owner:
                card.owner.remove(card)
            card.owner = self
            super().insert(position, card)
            self.refresh_enchantment()
            return True
        elif card.general == 'secret' and self.can_add_this_secret(card):
            for key in card.script.keys():
                self.secret[key].add(card)
            self.secret_key.append(card.key_number)

        return False

    def can_add_card(self):
        return len(self) < constants.BATTLE_SIZE

    def can_add_secret(self):
        card_id = set()
        for cards in self.secret.values():
            card_id.add(cards)
        return len(card_id) < constants.SECRET_SIZE

    def can_add_this_secret(self, secret):
        if secret.key_number not in self.secret_key and self.can_add_secret():
            return True
        return False

    def create_card(self, *keys_number, atk_bonus=0, def_bonus=0):
        # crée une carte sur le board mais sans la jouer
        for nb in keys_number:
            card_id = card.Card(nb, self.owner.bob)
            card_id.attack += atk_bonus
            card_id.health += def_bonus
            self.append(card_id)
        return card_id

    def freeze(self):
        if self:
            if self[0].state & constants.STATE_FREEZE: # unfreeze
                for minion in self:
                    minion.state &= constants.STATE_ALL - constants.STATE_FREEZE
            else: # freeze
                for minion in self:
                    if not minion.state & constants.STATE_DORMANT:
                        minion.state |= constants.STATE_FREEZE

    def drain_minion(self):
        for minion in self[::-1]:
            if not minion.state & constants.STATE_STILL_BOB:
                self.owner.hand.append(minion)

    def drain_all_minion(self):
        for minion in self[::-1]:
            if not minion.state & constants.STATE_DORMANT:
                self.owner.hand.append(minion)

    def fill_minion(self):
        player = self.opponent.owner
        nb_card_to_play = max(0, min(constants.BATTLE_SIZE - len(self), player.nb_card_by_refresh))
        bob_hand = self.owner.hand.cards_of_tier_max(tier_max=player.level)

        for _ in range(nb_card_to_play):
            if bob_hand:
                random.choice(bob_hand).play(board=self)
            else:
                print('main insuffisante !!!')
                break

    def fill_minion_battlecry(self):
        player = self.opponent.owner
        nb_card_to_play = max(0, min(constants.BATTLE_SIZE - len(self), player.nb_card_by_refresh))
        bob_hand = [minion
            for minion in self.owner.hand.cards_of_tier_max(tier_max=player.level)
                if minion.script and constants.EVENT_BATTLECRY in minion.script]

        for _ in range(nb_card_to_play):
            if bob_hand:
                random.choice(bob_hand).play(board=self)

    def fill_minion_temporal(self):
        player = self.opponent.owner
        nb_card_to_play = max(0, min(constants.BATTLE_SIZE - len(self), player.nb_card_by_refresh-1))
        bob_hand = self.owner.hand.cards_of_tier_max(tier_max=player.level)

        for _ in range(nb_card_to_play):
            if bob_hand:
                random.choice(bob_hand).play(board=self)

        lvl = min(constants.LEVEL_MAX, player.level+1)
        bob_hand = self.owner.hand.cards_of_tier_max(tier_max=lvl, tier_min=lvl)
        if bob_hand:
            random.choice(bob_hand).play(board=self)

    def remove_enchantment(self, owner):
        try:
            del self.enchantment[owner]
        except KeyError:
            pass

    def add_enchantment(self, owner, **infos):
        if owner not in self.enchantment:
            self.enchantment[owner] = defaultdict(int)
        self.enchantment[owner].update(infos)

    def refresh_enchantment(self):
        self.enchantment.clear()
        self.owner.active_event(constants.EVENT_PLAY_ENCHANTMENT)

    def nb_premium_card(self):
        nb = 0
        for minion in self:
            if minion.is_premium:
                nb += 1
        return nb