import random
import constants
import script_functions

def Piece_dor(self): # self = card_id
    self.owner.owner.gold += 1

def Recrutement_2(self):
    self.owner.owner.discover(self, nb=3, lvl_min=2, lvl_max=2)

def Recrutement_3(self):
    self.owner.owner.discover(self, nb=3, lvl_min=3, lvl_max=3)

def Recrutement_4(self):
    self.owner.owner.discover(self, nb=3, lvl_min=4, lvl_max=4)

def Recrutement_5(self):
    self.owner.owner.discover(self, nb=3, lvl_min=5, lvl_max=5)

def Recrutement_6(self):
    self.owner.owner.discover(self, nb=3, lvl_min=6, lvl_max=6)

def Avenge(self):
    if self.owner.board:
        target = random.choice(self.owner.board)
        target.create_and_apply_enchantment("1001")
        return True
    return False

def Autodefense_matrix(self, card):
    if not card.state & constants.STATE_DIVINE_SHIELD:
        card.state |= constants.STATE_DIVINE_SHIELD
        return True
    return False

def Competitive_spirit(self):
    if self.owner.board:
        for minion in self.owner.board:
            minion.create_and_apply_enchantment("1000")
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
    player = self.owner.owner
    minion = player.minion_choice(player.board)
    if minion:
        minion.create_and_apply_enchantment("500")
        # + special effect
        return minion
    return False

def Banana(self):
    player = self.owner.owner
    minion = player.minion_choice(player.board)
    if minion:
        minion.create_and_apply_enchantment("501")
        return minion
    return False

def Great_banana(self):
    player = self.owner.owner
    minion = player.minion_choice(player.board)
    if minion:
        minion.create_and_apply_enchantment("502")
        return minion
    return False
