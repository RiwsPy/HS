import card
import script_minion # problématique, import circulaire probable
import constants
import random
from copy import deepcopy

# TODO : le repop n'est pas dans le bon ordre en cas de repop multiple (Magnetic, Reincarnation etc) :
# tout repop sur la position initiale du minion
# TODO : peut générer plusieurs repops mais ne renvoie qu'un seul id, à changer ?
def invocation(self, key_number, nb_max=1, position=constants.BATTLE_SIZE):
    """
        *param self: invocateur
        *param key_number: invoqué
        *param nb_max: nombre d'invocation
        *param position: position de l'invoqué
        *param enemy: l'invocation se fait sur le board adverse
        *return: invocation id
    """
    if self.key_number == key_number and not self.state & 0x4:
        print(f"Erreur ? {self.name} reinvoque himself ?!")

    if self in self.owner and self.key_number not in ("303", "303_p"): # test
        position += 1

    repop_id = None
    for _ in range(nb_max):
        if self.owner.can_add_card():
            repop_id = card.Card(key_number, self.owner.owner.bob)
            # enchantement avant que le repop soit ajouté au board
            enchant_copy = self.owner.enchantment.copy()
            self.owner.append(repop_id, position)

            self.owner.owner.active_event(constants.EVENT_INVOC, repop_id)

            if self.key_number not in ('303', '303_p'):
                for khadgar, value in enchant_copy.items():
                    for _ in range(value['boost_invoc']):
                        position += 1
                        copy_minion(khadgar, repop_id, 1, position)
        else:
            break

    return repop_id

def copy_minion(self, minion_id, nb, position):
    for _ in range(nb):
        repop = invocation(self, minion_id.key_number, 1, position=position)
        if repop:
            repop.state |= minion_id.state
            repop.attack = minion_id.attack
            repop.health = minion_id.health
            repop.set_deathrattle(minion_id)

def reborn(self):
    serviteur = invocation(self, self.key_number, 1, self.position)
    if serviteur:
        serviteur.state_fight = serviteur.init_state & (constants.STATE_ALL - constants.STATE_REBORN)
        serviteur.health_fight = 1 - serviteur.init_health

def invocation_random_list(self, key_lst, nb_max=1):
    if self.key_number in key_lst: # un serviteur ne peut se réinvoquer lui-même
        key_lst.remove(self.key_number)

    if key_lst:
        for _ in range(nb_max):
            repop_id = invocation(self, random.choice(key_lst), 1, self.position)
        return repop_id
    return None
