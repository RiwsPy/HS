from base.entity import Spell
from base.sequence import Sequence

#TODO: automatic die for card.SECRET ?
# > empêche l'utilisation du nb_strike car le self.die() serait activé plusieurs fois

class TB_BaconShop_HP_008a(Spell):
    # Pièce d'or
    def cast(self, sequence: Sequence): # self = card_id
        self.controller.gold += 1


class TB_BaconShop_HP_047t(Spell):
    # Carte de recrutement
    def cast(self, sequence: Sequence):
        self.controller.discover(self, nb=3, lvl_min=self.quest_value, lvl_max=self.quest_value)
TB_BaconShop_HP_101t2= TB_BaconShop_HP_047t # Trophée
TB_BaconShop_Triples_01= TB_BaconShop_HP_047t # Récompense de triple


class TB_Bacon_Secrets_08(Spell):
    # Vengeance
    def die_off(self, sequence: Sequence):
        if sequence.is_ally(self) and self.controller.board.size > 0:
            self.buff(
                self.enchantment_dbfId,
                self.controller.board.cards.random_choice()
            )
            self.die()


class TB_Bacon_Secrets_07(Spell):
    # Matrice d'autodéfense
    def combat_on(self, sequence: Sequence):
        if sequence.target.controller is self.controller and not sequence.target.DIVINE_SHIELD:
            sequence.target.DIVINE_SHIELD = True
            self.die()


class TB_Bacon_Secrets_13(Spell):
    # Esprit combatif
    def turn_on(self, sequence: Sequence):
        if self.controller.board.size > 0:
            for minion in self.controller.board.cards:
                self.buff(self.enchantment_dbfId, minion)
            self.die()


class TB_Bacon_Secrets_04(Spell):
    # Portrait caché
    def combat_on(self, sequence: Sequence): # repop juste à droite de la carte
        if not self.controller.board.is_full:
            target = sequence.target
            if target.controller is self.controller:
                clone_card = target.clone()
                target.my_zone.append(clone_card, position=target.position+1)
                self.die()


class TB_Bacon_Secrets_12(Spell):
    # Bloc de glace
    def hit_on(self, sequence: Sequence):
        if sequence.target is self.controller and\
                self.in_fight_sequence and\
                sequence.damage_value >= self.controller.health:
            self.buff(self.enchantment_dbfId, self.controller)
            self.die()


class TB_Bacon_Secrets_01(Spell):
    # piège frappe-venin
    nb_repop = 1
    def combat_on(self, sequence: Sequence):
        if not self.controller.board.is_full and\
                sequence.target.controller is self.controller:
            self.invoc(sequence, self.repop_dbfId)
            self.die()


class TB_Bacon_Secrets_02(Spell):
    # piège à serpents
    # nb_strike will repeat self.die()
    def combat_on(self, sequence: Sequence):
        if not self.controller.board.is_full and\
                sequence.target.controller is self.controller:
            for _ in range(3):
                self.invoc(sequence, self.repop_dbfId)
            self.die()


# cumulable avec Khadgar ?
# Cumul avec Reborn ? (oui)
class TB_Bacon_Secrets_10(Spell):
    # Rédemption
    # Resurrecting effects such as Redemption don't move the dead minion. They summon a new copy of it.
    # Positionnement du repop ? A la place du mort ou à la fin du board ?
    def die_off(self, sequence: Sequence):
        if sequence.is_ally and not self.controller.board.is_full:
            new_minion = self.create_card(sequence.source.dbfId)
            new_minion.health = 1
            self.controller.board.append(new_minion)
            self.die()


class TRL_509t(Spell):
    # Banane
    # Note : la banane contrairement à la gemme de sang peut se lancer sur les minions de la taverne
    def play_start(self, sequence: Sequence):
        minion = self.controller.field.cards.choice(self.controller)
        if minion:
            sequence.add_target(minion)
        else:
            sequence.is_valid = False
        
    def cast(self, sequence: Sequence):
        self.buff(self.enchantment_dbfId, sequence.target)


class BGS_Treasures_000(TRL_509t):
    # Grande banane
    pass


class BG20_GEM(TRL_509t):
    # Gemme de sang
    def play_start(self, sequence: Sequence):
        player = self.controller
        if player.is_bot:
            minion = self.bot_play()
        else:
            minion = player.board.cards.choice(player)

        if minion:
            sequence.add_target(minion)
        else:
            sequence.is_valid = False

    def bot_play(self):
        # au tour 3, les résultats sont meilleurs avec la méthode random.

        # random method : 1.8
        # ciblage de l'attaque la plus faible : 1.85
        # ciblage de l'attaque la plus élevée : 1.4
        # ciblage 'adapté' au tour ou attaque la plus élevée : 1.67
        # ciblage 'adapté' au tour ou attaque la plus faible : 1.85

        # protéger les Mechanics.aura du Zapp ?
        # prise en compte de l'influence du Contrebandier dragonnet ou Maître des réalités ?
        board = self.controller.board
        if board.size == 0:
            return None
        elif board.size == 1:
            return board.cards[0]

        nb_turn = self.nb_turn
        sorted_board = sorted(board.cards, reverse=True,
                key=lambda x: (
                not x.POISONOUS,
                x.CLEAVE,
                x.DIVINE_SHIELD,
                x.OVERKILL,
                hasattr(x, 'enhance_on') and x.race.QUILBOAR,
                hasattr(x, 'enhance_off') and x.race.QUILBOAR,
                x.AURA,
                x.FRENZY,
                nb_turn <= 5 and nb_turn - x.attack == 1,
                nb_turn <= 5 and nb_turn - x.health == 0,
                -x.attack,
                ))
        return sorted_board[0]
