from collections import defaultdict
import constants
import bob
import script_minion
import script_spell
import player
import board
import script_functions

class Card:
    def __init__(self, key_number, bob, owner=None):
        self.name = ''
        self.bob = bob
        self.init_state = 0
        self.type = 0
        self.cost = 0
        self.script = {}
        self.init_attack = 0
        self.init_health = 0
        self.effects = defaultdict(int)
        self.from_bob = False
        self.level = 0
        self.key_number = key_number
        self._position = None
        self.general = 'minion'
        self.card_in = []

        self.reinitialize()
        self.owner = owner

    def __repr__(self):
        if self.general == 'minion':
            return f'{self.name} ({self.attack}-{self.health})'
        return self

    @property
    def is_premium(self):
        return self.key_number[-2:] == '_p'

    def reinitialize(self, owner=None): # board to bob
        self.purge_fight_effects(owner)
        for key, value in self.bob.all_card[self.key_number].items():
            setattr(self, key, value)
        self.script = self.script.copy()
        self.card_in = [self] # toutes les cartes fusionnées avec celle-ci (magnétisme, triple...)
        self.attack_bonus = 0
        self.health_bonus = 0
        for key, value in self.effects.copy().items():
            if self.bob.all_effect[key]['duration'] > 0:
                self.apply_effect_on(key, nb=-value)

    def purge_fight_effects(self, owner): # end fight
        self.attack_fight = 0 # effet qui se dissipe à la fin du combat
        self.health_fight = 0
        self.state_fight = 0
        if owner is not None and type(owner) != board.Board:
            print("ERROR minion initialize", self.name, type(owner))
        self.owner = owner
        #self.current_health = self.max_health

    def apply_effect_on(self, effect_key, nb=1):
        # ne modifie que les caractéristiques de combat
        if not nb:
            return None

        info = self.bob.all_effect.get(effect_key)
        mult = 1
        if not info and effect_key[:-2] == '_p':
            info = self.bob.all_effect.get(effect_key[-2:])
            mult = 2

        if info:
            if nb < 1:
                nb = max(nb, -self.effects[effect_key])
                self.state &= constants.STATE_ALL - info.get('s', 0)
                #TODO: recalculate state
            else:
                self.state |= info.get('s', 0)

            self.attack += info.get('a', 0)*nb*mult
            self.health += info.get('h', 0)*nb*mult
            self.effects[effect_key] += nb

            if self.effects[effect_key] == 0:
                del self.effects[effect_key]

    def set_effect_on(self, effect_key, nb=1):
        self.apply_effect_on(effect_key, -self.effects[effect_key])
        self.apply_effect_on(effect_key, nb)

    """
    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, new_owner):
        print('ici la')
        if self.general == "secret":
            self._owner = new_owner.board
            return None
        elif self.general == 'minion':
            if self.owner != new_owner: # and (not new_owner or new_owner.can_add_card()):
                if self.owner:
                    self.owner.remove(self)
                if new_owner is not None:
                    new_owner.append(self, self._position)
                self._owner = new_owner
        elif self.owner != new_owner and (not new_owner or new_owner.can_add_card()):
            if self.owner:
                self.owner.remove(self)
            if new_owner is not None:
                new_owner.append(self)
    """

    def die(self, killer=None):
        self.owner.remove(self)

        if self.general != 'minion' or type(self.owner) != board.Board:
            return None

        # deathrattle
        self.active_script_type(constants.EVENT_DEATHRATTLE)

        # le charognard s'active après le râle d'agonie du serviteur
        # mais avant la réincarnation
        self.owner.owner.active_event(constants.EVENT_DIE_ALLY, self)
        self.owner.owner.opponent.active_event(constants.EVENT_KILLER_ALLY, killer, self)

        if self.state_fight & constants.STATE_REBORN:
            script_functions.reborn(self)

    def can_attack(self):
        if self.attack > 0:
            return True
        return False

    def how_many_time_can_I_attack(self):
        nb_attack_max = 1
        if self.state_fight & constants.STATE_MEGA_WINDFURY:
            nb_attack_max *= 4
        elif self.state_fight & constants.STATE_WINDFURY:
            nb_attack_max *= 2
        return nb_attack_max

    def set_card(self, source_key_number, copy=True):
        if source_key_number not in self.bob.all_card:
            print(f"set_card ERROR {source_key_number} not exist")
            return None

        if copy: # Reno power
            infos = self.bob.all_card[source_key_number]
            self.init_attack = infos['init_attack']
            self.init_health = infos['init_health']
            for key, value in self.bob.all_card[self.key_number].get('script', {}).items(): # retrait des scripts de la carte initiale
                for effect in value:
                    self.script[key].remove(effect)
            self.add_script(source_key_number)

        else: # habitué sans-visage, gestion de la vente ? la carte est enlevée de la main de bob?
            # ou bien seul l'habitué est enlevé ?
            for key, value in self.bob.all_card[self.key_number].items():
                setattr(self, key, value)
            self.attack_bonus = 0
            self.health_bonus = 0
            self.card_in = [self]

        self.key_number = source_key_number
        self.owner.refresh_enchantment()

    @property
    def is_alive(self):
        return self.health > 0 and not self.state & constants.STATE_IS_POISONED

    def are_same_type(self, other):
        return self.type & other.type

    def is_type(self, typ):
        return self.type & typ

    def combine_card(self, source):
        # add source card stat to self card
        self.attack += source.attack
        self.health += source.health
        self.state |= source.state
        self.copy_deathrattle(source)
        self.card_in.append(source)

    def set_deathrattle(self, source):
        lst_script = source.script.get(constants.EVENT_DEATHRATTLE)
        if lst_script:
            self.script[constants.EVENT_DEATHRATTLE] = lst_script

    def copy_deathrattle(self, source):
        # copie des scripts (deathrattle) et les ajoutent aux siens
        lst_script = source.script.get(constants.EVENT_DEATHRATTLE)
        if lst_script:
            if constants.EVENT_DEATHRATTLE not in self.script:
                self.script[constants.EVENT_DEATHRATTLE] = lst_script
            else:
                self.script[constants.EVENT_DEATHRATTLE] += lst_script

    def add_deathrattle(self, deathrattle):
        if constants.EVENT_DEATHRATTLE not in self.script:
            self.script[constants.EVENT_DEATHRATTLE] = [deathrattle]
        else:
            self.script[constants.EVENT_DEATHRATTLE].append(deathrattle)

    def add_script(self, source_key_number):
        # ajoute tous les scripts présents dans source_key_number, à self
        infos = self.bob.all_card.get(source_key_number, {}).get('script', {})
        for key, value in infos.items():
            if key in self.script:
                self.script[key].extend(value)
            else:
                self.script[key] = value

    @property
    def attack(self):
        bonus = 0
        if self.owner and type(self.owner) == board.Board:
            if self.key_number in ("208", "208_p"): # Vieux Troubloeil
                add = self.double_if_premium(1)
                for minion in self.owner + self.owner.opponent:
                    if constants.TYPE_MURLOC & minion.type and minion != self:
                        bonus += add

            for enchanter, value in self.owner.enchantment.items():
                if self != enchanter and (self.type & value['restr_type'] or\
                        not value['restr_type']):
                    bonus += value['attack']

        return max(0, self.init_attack + self.attack_bonus + self.attack_fight + bonus)

    @attack.setter
    def attack(self, value):
        self.attack_bonus += value - self.attack

    @property
    def max_health(self):
        bonus = 0
        if self.owner and type(self.owner) == board.Board:
            for enchanter, value in self.owner.enchantment.items():
                if self != enchanter and (self.type & value['restr_type'] or\
                        not value['restr_type']):
                    bonus += value['max_health']
        return self.init_health + self.health_bonus + self.health_fight + bonus

    @property
    def health(self):
        bonus = 0
        if self.owner and type(self.owner) == board.Board:
            for enchanter, value in self.owner.enchantment.items():
                if self != enchanter and (self.type & value['restr_type'] or\
                        not value['restr_type']):
                    bonus += value['health']
            # problème en cas de mort du serviteur, le pv est perdu
        return self.init_health + self.health_bonus + self.health_fight + bonus

    @health.setter
    def health(self, value):
        add = value - self.health
        self.health_bonus += add
        if add < 0:
            print("Health : value < 0 ??!")

    @property
    def state(self):
        return self.init_state | self.state_fight

    @property
    def has_frenzy(self):
        return self.state_fight & constants.STATE_FRENZY and self.is_alive

    @state.setter
    def state(self, value):
        self.init_state = value

    @property
    def position(self):
        if not self.owner:
            return self._position
        elif type(self.owner) is board.Board:
            if not self in self.owner:
                if self._position is not None:
                    return self._position
                print(f"{self.name} introuvable sur le champ de bataille.")
                return None
            return self.owner.index(self)
        return None

    @position.setter
    def position(self, position):
        self._position = position

    def double_if_premium(self, value):
        if self.is_premium:
            return value*2
        return value

    def have_script_type(self, typ):
        return typ in self.script

    def active_script_type(self, event, *arg):
        if not event in self.script:
            return None

        nb_strike = 1

        if type(self.owner) is board.Board:
            if event == constants.EVENT_DEATHRATTLE:
                for value in self.owner.enchantment.values():
                    nb_strike = max(nb_strike, 1+value['boost_deathrattle'])
            elif event == constants.EVENT_BATTLECRY:
                for value in self.owner.enchantment.values():
                    nb_strike = max(nb_strike, 1+value['boost_battlecry'])
            elif event == constants.EVENT_PLAY_ENCHANTMENT:
                if type(self.owner.owner) is bob.Bob:
                    return None

        for _ in range(nb_strike):
            for effect in self.script[event]:
                getattr(script_minion, effect)(self, *arg)

    def play(self, board=None, position=constants.BATTLE_SIZE): # hand to board or board in board
        if board is None:
            if type(self.owner.owner) is player.Player:
                board = self.owner.owner.board
            else:
                print('Unknown board')
                return None

        # possibilité de jouer la carte d'un autre joueur ?!
        if self.owner == board:
            if position != self.position:
                board.append(self, position)
        elif self.general == 'minion' and board.can_add_card():
            self.position = position
            board.append(self, position)
            if type(self.owner.owner) is player.Player:
                playr = self.owner.owner
                if self.is_premium:
                    spell_lst = [0, "1009", "1010", "1011", "1012", "1013", "1013"]
                    playr.hand.create_card(spell_lst[self.level])

                playr.minion_play_this_turn.append(self)

                playr.active_event(constants.EVENT_PLAY, self)
                playr.active_event(constants.EVENT_INVOC, self)
                self.active_script_type(constants.EVENT_BATTLECRY)

                if self.owner[-1] != self and self.state & constants.STATE_MAGNETIC:
                    target = self.owner[position+1]
                    if target.type & constants.TYPE_MECH:
                        target.combine_card(self)
                        target.state &= (constants.STATE_ALL - constants.STATE_MAGNETIC)
                        self.owner.remove(self)
            else:
                self.owner.opponent.owner.active_event(constants.EVENT_BOB_PLAY, self)
        elif self.general == 'spell':
            if self.owner.owner.gold >= self.cost:
                self.owner.owner.gold -= self.cost
                self.active_spell()
                self.owner.remove(self)

        return self

    def trade(self): # board to hand
        seller = self.owner.owner
        buyer = self.owner.opponent.owner
        if self.general == "minion":
            if buyer.can_buy_minion() and not self.state & constants.STATE_DORMANT:
                self.state &= (constants.STATE_ALL - constants.STATE_STILL_BOB)
                seller.sell_card(self, cost=buyer.minion_cost)
                buyer.buy_card(self, cost=buyer.minion_cost)
                buyer.hand.append(self)
                return True
            else:
                print('Achat de serviteur impossible, dormant ou manque de gold')
        else:
            print('Achat de sort/secret impossible')
        return False

    def active_spell(self, typ=0, *arg):
        if self.general == "spell":
            for spl in self.script.values():
                getattr(script_spell, spl)(self)
        elif typ in self.owner.secret:
            for spell in self.owner.secret[typ]:
                result = getattr(script_spell, spell.script[typ])(self, *arg)
                if result:
                    self.owner.secret[typ].discard(spell.script[typ])

