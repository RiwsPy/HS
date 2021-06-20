import random
from constants import State

def Piece_dor(self): # self = card_id
    self.controller.gold += 1

def Recrutement(self):
    self.controller.discover(self, nb=3, lvl_min=self.quest_value, lvl_max=self.quest_value)

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

def Blood_gem(self):
    player = self.controller
    minion = player.minion_choice(player.board)
    if minion:
        bonus = 1
        for info in minion.controller.aura_active.values():
            bonus += info['boost_blood_gem']
        minion.create_and_apply_enchantment("72191", a=bonus, h=bonus)
        return minion
    return False

def Banana(self):
    player = self.owner.owner
    minion = player.minion_choice(player.board)
    if minion:
        minion.create_and_apply_enchantment("501_e")
        return minion
    return False

def Great_banana(self):
    player = self.owner.owner
    minion = player.minion_choice(player.board)
    if minion:
        minion.create_and_apply_enchantment("502_e")
        return minion
    return False
