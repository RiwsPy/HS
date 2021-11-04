import random
from enums import Event, CardName, FIELD_SIZE
from entity import Spell

#TODO: automatic die for card.SECRET ?
# > empêche l'utilisation du nb_strike car le self.die() serait activé plusieurs fois

class TB_BaconShop_HP_008a(Spell):
    # Pièce d'or
    def cast(self, sequence): # self = card_id
        self.controller.gold += 1


class TB_BaconShop_HP_047t(Spell):
    # Carte de recrutement
    def cast(self, sequence):
        self.controller.discover(self, nb=3, lvl_min=self.quest_value, lvl_max=self.quest_value)
TB_BaconShop_HP_101t2= TB_BaconShop_HP_047t # Trophée
TB_BaconShop_Triples_01= TB_BaconShop_HP_047t # Récompense de triple


class TB_Bacon_Secrets_08(Spell):
    # Vengeance
    def die_off(self, sequence):
        if sequence.source.controller is self.controller and self.controller.board.size > 0:
            self.buff(self.enchantment_dbfId, random.choice(self.controller.board.cards))
            self.die()


class TB_Bacon_Secrets_07(Spell):
    # Matrice d'autodéfense
    def combat_on(self, sequence):
        if sequence.source.controller is self.controller and not sequence.source.DIVINE_SHIELD:
            sequence.source.DIVINE_SHIELD = True
            self.die()


class TB_Bacon_Secrets_13(Spell):
    # Esprit combatif
    def turn_on(self, sequence):
        if self.controller.board.size > 0:
            for minion in self.controller.board.cards:
                self.buff(self.enchantment_dbfId, minion)
                self.die()


class TB_Bacon_Secrets_04(Spell):
    # Portrait caché
    def combat_on(self, sequence): # repop juste à droite de la carte
        if not self.controller.board.is_full:
            for target in sequence.targets:
                if target.controller is self.controller:
                    clone_card = target.clone()
                    target.my_zone.append(clone_card, position=target.position+1)
                    self.die()
                    break


class TB_Bacon_Secrets_12(Spell):
    # Bloc de glace
    def hit_on(self, sequence):
        if sequence.target is self.controller and\
                self.in_fight_sequence and\
                sequence.damage_value >= self.controller.health:
            self.buff(self.enchantment_dbfId, self.controller)
            self.die()


class TB_Bacon_Secrets_01(Spell):
    # piège frappe-venin
    nb_repop = 1
    def combat_on(self, sequence):
        if not self.controller.board.is_full:
            for target in sequence.targets:
                if target.controller is self.controller:
                    self.invoc(sequence, self.repop_dbfId)
                    self.die()
                    break


class TB_Bacon_Secrets_02(Spell):
    # piège à serpents
    # nb_strike will repeat self.die()
    def combat_on(self, sequence):
        if not self.controller.board.is_full:
            for target in sequence.targets:
                if target.controller is self.controller:
                    for _ in range(3):
                        self.invoc(sequence, self.repop_dbfId)
                    self.die()
                    break


# cumulable avec Khadgar ?
# Cumul avec Reborn (théoriquement oui)
class TB_Bacon_Secrets_10(Spell):
    # Rédemption
    # Resurrecting effects such as Redemption don't move the dead minion. They summon a new copy of it.
    # Positionnement du repop ? A la place du mort ou à la fin du board ?
    def die_off(self, sequence):
        if self.controller is sequence.source.controller and not self.controller.board.is_full:
            new_minion = self.create_card(sequence.source.dbfId)
            new_minion.health = 1
            self.controller.board.append(new_minion)
            self.die()


class TRL_509t(Spell):
    # Banane
    def cast_start(self, sequence):
        player = self.controller
        minion = player.choose_one_of_them(player.board.cards)
        if minion:
            sequence.targets.append(minion)
        else:
            sequence.is_valid = False
        
    def cast(self, sequence):
        for minion in sequence.targets:
            self.buff(self.enchantment_dbfId, minion)


class BGS_Treasures_000(TRL_509t):
    # Grande banane
    pass


class BG20_GEM(TRL_509t):
    # Gemme de sang
    def cast_start(self, sequence):
        player = self.controller
        if player.is_bot:
            minion = self.bot_play()
        else:
            minion = player.choose_one_of_them(player.board.cards)

        if minion:
            sequence.targets.append(minion)
        else:
            sequence.is_valid = False

    def bot_play(self):
        # au tour 3, les résultats sont meilleurs avec la méthode random.

        # random method : 1.8
        # ciblage de l'attaque la plus faible : 1.85
        # ciblage de l'attaque la plus élevée : 1.4
        # ciblage 'adapté' au tour ou attaque la plus élevée : 1.67
        # ciblage 'adapté' au tour ou attaque la plus faible : 1.85

        # protéger les Mecanics.aura du Zapp ?
        board = self.controller.board
        if board.size == 0:
            return None
        elif board.size == 1:
            return board.cards[0]

        nb_turn = self.game.nb_turn
        sorted_board = sorted(board.cards, reverse=True,
                key=lambda x: (
                not x.POISONOUS,
                x.CLEAVE,
                x.DIVINE_SHIELD,
                x.OVERKILL,
                #x.event & Event.ADD_ENCHANTMENT_ON,
                x.AURA,
                x.FRENZY,
                nb_turn <= 5 and nb_turn - x.attack == 1,
                nb_turn <= 5 and nb_turn - x.health == 0,
                -x.attack,
                ))
        return sorted_board[0]
