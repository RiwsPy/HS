import random
from enums import State, Event, CardName
import script_functions

class TB_BaconShop_HP_008a:
    # Pièce d'or
    def play(self): # self = card_id
        self.controller.gold += 1
        return True

class TB_BaconShop_HP_047t:
    # Carte de recrutement
    def play(self):
        self.controller.discover(self, nb=3, lvl_min=self.quest_value, lvl_max=self.quest_value)
        return True
TB_BaconShop_HP_101t2= TB_BaconShop_HP_047t # Trophée
TB_BaconShop_Triples_01= TB_BaconShop_HP_047t # Récompense de triple


class TB_Bacon_Secrets_08:
    # Vengeance
    def play(self):
        if self.owner.board:
            target = random.choice(self.owner.board)
            target.create_and_apply_enchantment("1812")
            return True
        return False

class TB_Bacon_Secrets_07:
    # Matrice d'autodéfense
    def play(self, card):
        if not card.state & State.DIVINE_SHIELD:
            card.state |= State.DIVINE_SHIELD
            return True
        return False

class TB_Bacon_Secrets_13:
    # esprit compétitif
    def play(self):
        if self.owner.board:
            for minion in self.owner.board:
                minion.create_and_apply_enchantment("1000_e")
            return True
        return False

class TB_Bacon_Secrets_04:
    # Portrait caché
    def play(self, card): # repop juste à droite de la carte
        pass

class TB_Bacon_Secrets_12:
    # Bloc de glace
    def play(self):
        pass

class TB_Bacon_Secrets_01:
    # piège frappe-venin
    def play(self, card):
        if len(self.owner) < 7:
            script_functions.invocation(self, "152") # repop tout à droite
            return True
        return False

class TB_Bacon_Secrets_02:
    # piège à serpents
    def play(self, card):
        if len(self.owner) < 5:
            script_functions.invocation(self, "153", nb_max=3)
            return True
        return False

# non cumulable avec Khadgar ? Cumul avec réincarnation ?
class TB_Bacon_Secrets_10:
    # Rédemption
    def play(self, card):
        pass

class BG20_GEM:
    # Gemme de sang
    def play(self) -> bool:
        player = self.controller
        if player.is_bot:
            minion = BG20_GEM.bot_play(self)
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

class TRL_509t:
    # Banane
    def play(self):
        player = self.controller
        minion = player.choose_one_of_them(player.board.cards)
        if minion:
            self.buff("53217", minion)
            return True
        return False

class BGS_Treasures_000:
    # Grosse banane
    def play(self):
        player = self.controller
        minion = player.choose_one_of_them(player.board.cards)
        if minion:
            self.buff("65231", minion)
            return True
        return False
