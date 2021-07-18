import random
from enums import State, Event, CardName
import script_functions

class Piece_dor:
    def play(self): # self = card_id
        self.controller.gold += 1
        return True

class Recrutement:
    def play(self):
        self.controller.discover(self, nb=3, lvl_min=self.quest_value, lvl_max=self.quest_value)
        return True

def Avenge(self):
    if self.owner.board:
        target = random.choice(self.owner.board)
        target.create_and_apply_enchantment("1001_e")
        return True
    return False

def Autodefense_matrix(self, card):
    if not card.state & State.DIVINE_SHIELD:
        card.state |= State.DIVINE_SHIELD
        return True
    return False

def Competitive_spirit(self):
    if self.owner.board:
        for minion in self.owner.board:
            minion.create_and_apply_enchantment("1000_e")
        return True
    return False

def Splitting_image(self, card): # repop juste à droite de la carte
    pass

def Ice_block(self):
    pass

def Venomstrike_trap(self, card):
    if len(self.owner) < 7:
        script_functions.invocation(self, "152") # repop tout à droite
        return True
    return False

def Sneak_trap(self, card):
    if len(self.owner) < 5:
        script_functions.invocation(self, "153", nb_max=3)
        return True
    return False

# non cumulable avec Khadgar ? Cumul avec réincarnation ?
def Redemption(self, card):
    pass

class Blood_gem:
    def play(self) -> bool:
        player = self.controller
        if player.is_bot:
            minion = Blood_gem.bot_play(self)
        else:
            minion = player.choose_one_of_them(player.board.cards)

        if minion:
            bonus = 1
            #for info in player.aura_active.values():
            #    bonus += info['boost_blood_gem']
            self.buff(CardName.BLOOD_GEM, minion, attack=bonus, max_health=bonus)
            return True
        return False

    def bot_play(self):
        # au tour 3, les résultats sont meilleurs avec la méthode random.

        # random method : 1.8
        # ciblage de l'attaque la plus faible : 1.85
        # ciblage de l'attaque la plus élevée : 1.4
        # ciblage 'adapté' au tour ou attaque la plus élevée : 1.67
        # ciblage 'adapté' au tour ou attaque la plus faible : 1.85

        # protéger les State.aura du Zapp ?
        targets = self.controller.board.cards
        if not targets:
            return None
        elif len(targets) < 2:
            return targets[0]
        nb_turn = self.game.nb_turn
        sorted_board = sorted(targets, reverse=True,
                key=lambda x: (
                not x.state & State.POISONOUS,
                not x.state & State.ATTACK_WEAK,
                x.state & State.CLEAVE,
                x.state & State.DIVINE_SHIELD,
                x.event & Event.OVERKILL,
                x.event & Event.ADD_ENCHANTMENT_ON,
                x.state & State.FRENZY,
                nb_turn <= 5 and nb_turn - x.attack == 1,
                nb_turn <= 5 and nb_turn - x.health == 0,
                -x.attack,
                ))
        return sorted_board[0]

class Banana:
    def play(self):
        player = self.controller
        minion = player.choose_one_of_them(player.board.cards)
        if minion:
            self.buff("53217", minion)
            return True
        return False

class Great_banana:
    def play(self):
        player = self.controller
        minion = player.choose_one_of_them(player.board.cards)
        if minion:
            self.buff("65231", minion)
            return True
        return False
