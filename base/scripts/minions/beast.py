from base.entity import Minion
from base.enums import CardName, BOARD_SIZE
import random
from base.utils import repeat_effect
from base.sequence import Sequence
from base.db_card import Card_list
from base.scripts.base import *


class BG21_000(Minion):
    # Saute-mouton
    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        target = self.controller.board.cards.filter(race='BEAST', is_alive=True).random_choice()
        self.buff(
            target
        )
BG21_000_G= BG21_000 # Saute-mouton premium


class BG21_002(Minion):
    # Pote à plumes
    def avenge(self, sequence: Sequence):
        for minion in self.owner.cards.filter(race='BEAST'):
            self.buff(minion)
BG21_002_G= BG21_002 # Pote à plumes premium


class BG21_001(Minion):
    # Crocilisque claires-écailles
    def avenge(self, sequence: Sequence):
        self.buff(
            self.my_zone.cards.filter(race='BEAST').exclude(self).random_choice()
        )
    deathrattle = avenge
BG21_001_G= BG21_001 # Crocilisque claires-écailles premium


BG21_003= battlecry_select_one_minion_and_buff_it # Crotale résurrecteur
BG21_003_G= BG21_003

BG19_010= deathrattle_repop # Rat d'égout
BG19_010_G= BG19_010 # Rat d'égout premium


class LOOT_078(Minion):
    # Hydre des cavernes
    pass

class TB_BaconUps_151(LOOT_078):
    # Hydre des cavernes
    pass

CFM_315t= Minion # chat tigré
TB_BaconUps_093t= Minion # chat tigré premium
CFM_316t= Minion # Rat
TB_BaconUps_027t= Minion # Rat premium
OG_216a= Minion # Araignée
TB_BaconUps_026t= Minion # Araignée premium
BG19_010t= Minion # Demi-carapace
BG19_010_Gt= Minion # Demi-carapace premium
EX1_534t= Minion # Hyène
TB_BaconUps_049t= Minion # Hyène premium
TRL_232t= Minion # Rejeton cuiracier
TB_BaconUps_051t= Minion # Rejeton cuiracier premium
FP1_010= Minion # Maexxna
TB_BaconUps_155= Minion # Maexxna premium


class CFM_316(deathrattle_repop):
    # Clan des rats
    @property
    def nb_repop(self):
        return min(self.attack, BOARD_SIZE)
TB_BaconUps_027= CFM_316


class EX1_534(deathrattle_repop):
    # Crinière des savanes
    nb_repop = 2
TB_BaconUps_049= EX1_534 # Crinière des savanes premium


class BGS_008(deathrattle_repop):
    # Boagnarok
    nb_repop = 2

    @property
    def repopDbfId(self) -> int:
        # TODO: test, minion_can_collect + DEATHRATTLE non configuré
        return self.game.minion_can_collect.filter(DEATHRATTLE=True).exlude(self.dbfId).random_choice()


class TB_BaconUps_057(BGS_008):
    # Boagnarok premium
    nb_repop = 4


class BGS_018(Minion):
    # Goldrinn
    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        for minion in self.my_zone.cards.filter(race='BEAST'):
            self.buff(minion)
TB_BaconUps_085= BGS_018 # Goldrinn premium



DS1_070= battlecry_select_one_minion_and_buff_it # Maître-chien
TB_BaconUps_068= DS1_070 # Maître-chien premium


class CFM_315(Minion):
    # chat de gouttière

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.invoc(sequence, self.repopDbfId)
TB_BaconUps_093= CFM_315 # chat de gouttière premium



class EX1_531(Minion):
    # Hyène_charognarde
    def die_off(self, sequence: Sequence):
        if sequence.is_ally(self) and sequence.source.race.BEAST:
            self.buff(self)
TB_BaconUps_043= EX1_531 # Hyène_charognarde premium


class BGS_078(Minion):
    # Ara monstrueux
    nb_strike = 1

    @repeat_effect
    def combat_end(self, sequence: Sequence):
        minions_with_deathrattle = Card_list()
        for minion in self.my_zone.cards.filter(is_alive=True).exclude(self):
            for entity in [minion] + minion.entities:
                if entity.DEATHRATTLE:
                    minions_with_deathrattle.append(minion)
                    break

        if minions_with_deathrattle:
            target = random.choice(minions_with_deathrattle)
            Sequence('DEATHRATTLE', target).start_and_close()


class TB_BaconUps_135(BGS_078):
    # Ara monstrueux premium
    nb_strike = 2


class BGS_017(Minion):
    # Chef de meute
    def summon_off(self, sequence: Sequence):
        source = sequence.source
        if sequence.is_ally(self) and source.race.BEAST:
            self.buff(source)
TB_BaconUps_086= BGS_017 # Chef de meute premium
BGS_021= BGS_017 # Maman ourse
TB_BaconUps_090= BGS_017 # Maman ourse premium


class BGS_075(Minion):
    # Saurolisque enragé
    def play_off(self, sequence: Sequence):
        if sequence.source.DEATHRATTLE and sequence.is_ally(self):
            self.buff(self)
TB_BaconUps_125= BGS_075 # Saurolisque enragé premium


class TRL_232(Minion):        
    # Navrecorne cuiracier
    def overkill(self, sequence: Sequence):
        self.invoc(sequence, self.repopDbfId)
TB_BaconUps_051= TRL_232 # Navrecorne cuiracier premium

KAR_005= deathrattle_repop # Gentille grand-mère
TB_BaconUps_004= KAR_005 # Gentille grand-mère premium

KAR_005a= Minion # Grand méchant loup
TB_BaconUps_004t= Minion # Grand méchant loup premium

CFM_816= battlecry_select_one_minion_and_buff_it # Sensei virmen
TB_BaconUps_074= CFM_816 # Sensei virmen premium

class OG_216(deathrattle_repop):
    # Loup contaminé
    nb_repop = 2
TB_BaconUps_026= OG_216 # Loup contaminé premium
