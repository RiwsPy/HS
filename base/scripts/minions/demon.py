from base.entity import Minion
from base.enums import CardName
from base.scripts.base import *
import random
from base.utils import repeat_effect
from base.sequence import Sequence


class BG21_039(aura_buff_race):
    # Kathra’natir
    def summon_start(self, sequence: Sequence):
        super().summon_start(sequence)
        if sequence.is_valid:
            self.buff(self.controller, -76567)
BG21_039_G= BG21_039 # Kathra’natir premium


class BG21_007(Minion):
    # Auspice funeste impatient
    nb_strike = 1

    @repeat_effect
    def avenge(self, sequence: Sequence):
        self.controller.draw(
            self.controller.deck.filter(race='DEMON').random_choice()
        )


class BG21_007_G(BG21_007):
    # Auspice funeste impatient premium
    nb_strike = 2


class BG21_004(Minion):
    # Ur'Zul insatiable
    bonus_mult = 1
    def play_off(self, sequence: Sequence):
        if sequence.is_ally(self) and sequence.source.race.DEMON:
            target = self.my_zone.opponent.cards.exclude(DORMANT=True).random_choice()
            if target:
                self.buff(
                    self,
                    attack=target.attack*self.bonus_mult,
                    max_health=target.max_health*self.bonus_mult)
                self.controller.opponent.hand.append(target)

class BG21_004_G(BG21_004):
    # Ur'Zul insatiable premium
    bonus_mult = 2


class BG21_005(Minion):
    # Gangroptère affamé
    bonus_mult = 1
    def turn_off(self, sequence: Sequence):
        for demon, target in zip(
                self.my_zone.cards.filter(race='DEMON').shuffle(),
                self.my_zone.opponent.cards.exclude(DORMANT=True).shuffle()):
            self.buff(
                demon,
                attack=target.attack*self.bonus_mult,
                max_health=target.max_health*self.bonus_mult)
            self.controller.bob.hand.append(target)


class BG21_005_G(BG21_005):
    # Gangroptère affamé premium
    bonus_mult = 2


class BG21_029(deathrattle_repop):
    # Diablotin dégoûtant
    nb_repop = 2
BG21_029_G= BG21_029  # Diablotin dégoûtant premium


class BG21_006(Minion):
    # Entourloupeur impétueux
    nb_strike = 1

    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        self.buff(
            self.controller.board.cards.filter(is_alive=True).exclude(self).random_choice(),
            max_health=self.max_health)


class BG21_006_G(BG21_006):
    # Entourloupeur impétueux premium
    nb_strike = 2


class LOOT_368(deathrattle_repop):
    # Seigneur du vide
    nb_repop = 3
TB_BaconUps_059= LOOT_368 # Seigneur du vide premium


class DMF_533(deathrattle_repop):
    # Matrone de la piste
    nb_repop = 2
TB_BaconUps_309= DMF_533 # Matrone de la piste premium


class BGS_044(hit_by_repop):
    # Maman des diablotins
    # Note: couplé avec Khadgar, le second repop ne possède pas TAUNT
    nb_repop = 1
    def hit(self, sequence: Sequence):
        if self is sequence.target:
            super().hit(sequence)
            for minion in sequence._repops:
                self.buff(minion)

    @property
    def repopDbfId(self) -> int:
        return self.game.minion_can_collect.filter(race='DEMON').exclude(self.dbfId).random_choice()


class TB_BaconUps_116(BGS_044):
    # Maman des diablotins premium
    nb_repop = 2


BGS_001= battlecry_select_one_minion_and_buff_it # Surveillant Nathrezim
TB_BaconUps_062=BGS_001 # Surveillant Nathrezim premium

BGS_014= deathrattle_repop # Emprisonneur
TB_BaconUps_113= BGS_014 # Emprisonneur premium

BRM_006t= Minion # Diablotin
TB_BaconUps_030t= Minion # Diablotin premium
DMF_533t= Minion # Diablotin embrasé
TB_BaconUps_309t= Minion # Diablotin embrasé premium
CS2_065= Minion # Marcheur du vide
TB_BaconUps_059t= Minion # Marcheur du vide premium


class BGS_010(Minion):
    # Maitre de guerre annihiléen

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.buff(self, max_health=self.bonus_value)

    @property
    def bonus_value(self) -> int:
        return self.controller.max_health - self.controller.health


class TB_BaconUps_083(BGS_010):
    # Maitre de guerre annihiléen premium
    @property
    def bonus_value(self) -> int:
        return super().bonus_value*2


class BGS_002(Minion):
    # Jongleur d'âmes
    nb_strike = 1

    @repeat_effect
    def die_off(self, sequence: Sequence):
        if sequence.source.race.DEMON and sequence.is_ally(self):
            sequence(
                self.damage,
                self.my_zone.opponent.cards.random_choice(),
                3,
                overkill=False)


class TB_BaconUps_075(BGS_002):
    # Jongleur d'âmes premium
    nb_strike = 2


class BGS_204(Minion):
    # Démon démesuré
    def play_off(self, sequence: Sequence):
        if sequence.is_ally(self) and sequence.source.race.DEMON:
            self.buff(self)
TB_BaconUps_304= BGS_204 # Démon démesuré premium


class BGS_004(Minion):
    # Tisse-colère
    def play_off(self, sequence: Sequence):
        if sequence.is_ally(self) and sequence.source.race.DEMON:
            self.damage(self.controller, 1)
            self.buff(self)
TB_BaconUps_079= BGS_004 # Tisse-colère premium


class BGS_059(battlecry_select_one_minion_and_buff_it):
    # Dévoreur d'âmes
    bonus_mult = 1
    @repeat_effect
    def battlecry(self, sequence: Sequence):
        target = sequence.target
        if target and target.my_zone is self.my_zone:
            self.controller.bob.hand.append(target)
            self.controller.gold += 3*self.bonus_mult
            self.buff(
                self,
                attack=target.attack*self.bonus_mult,
                max_health=target.health*self.bonus_mult)


class TB_BaconUps_119(BGS_059):
    # Dévoreur d'âmes premium
    bonus_mult = 2


class BG20_210(Minion):
    # Maraudeur des ruines
    def turn_off(self, sequence: Sequence):
        if self.my_zone.size <= 6:
            self.buff(self)
BG20_210_G= BG20_210 # Maraudeur des ruines premium


class YOD_026(Minion):
    # Serviteur diabolique
    nb_strike = 1

    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        minions = self.controller.board.cards.filter(is_alive=True)
        if minions:
            self.buff(random.choice(minions), attack=self.attack)


class TB_BaconUps_112(YOD_026):
    # Serviteur diabolique premium
    nb_strike = 2


class GVG_021(aura_buff_race):
    # Mal'Ganis
    def summon_start(self, sequence: Sequence):
        super().summon_start(sequence)
        if sequence.is_valid:
            self.buff(self.controller, -2203)
TB_BaconUps_060= GVG_021 # Mal'Ganis premium


EX1_185= aura_buff_race # Brise-siège
TB_BaconUps_053= EX1_185 # Brise-siège premium


class LOOT_013(Minion):
    # Homoncule_sans_gene

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.damage(self.controller, 2)
TB_BaconUps_148= LOOT_013 # Homoncule_sans_gene premium

CFM_610= battlecry_select_all_and_buff_them # Tisse-cristal
TB_BaconUps_070= CFM_610 # Tisse-cristal premium

BRM_006= hit_by_repop # Chef du gang des diablotins
TB_BaconUps_030= BRM_006 # Chef du gang des diablotins premium