from base.entity import Minion
from base.enums import CardName
from base.scripts.base import *
import random
from base.utils import repeat_effect
from base.sequence import Sequence


class BG21_017(Minion):
    # Contrebandier saumâtre
    nb_strike = 1

    @repeat_effect
    def turn_off(self, sequence: Sequence):
        have_another_pirate = self.owner.cards.filter(race='PIRATE').exclude(self)
        if have_another_pirate:
            self.controller.draw(CardName.COIN)


class BG21_017_G(BG21_017):
    # Contrebandier saumâtre premium
    nb_strike = 2


class BG21_016(Minion):
    # Peggy les Os-de-verre
    def add_card_on_hand_off(self, sequence: Sequence):
        if sequence.is_ally(self):
            pirates = self.my_zone.cards.filter(race='PIRATE').exclude(self)
            if pirates:
                self.buff(random.choice(pirates))
BG21_016_G= BG21_016 # Peggy les Os-de-verre premium


class BG21_031(Minion):
    # Tony Deux-Défenses
    nb_strike = 1

    @repeat_effect
    def avenge(self, sequence: Sequence):
        targets = self.my_zone.cards.filter(race='PIRATE', is_premium=False, is_alive=True).exclude(self)
        if targets:
            target = random.choice(targets)
            # ???


class BG21_031_G(BG21_031):
    # Tony Deux-Défenses
    nb_strike = 2


class BG21_019(Minion):
    # Pillarde curieuse
    """
        Fonctionnement ?
        Carte au hasard prise dans la main de bob ? proba T1 > proba T2 > ... ?
        Carte non prise dans la main de bob ? > proba T1 = proba T2 = ... ? puis enlevée ?
        si carte enlevée, carte enlevée en 3 exemplaires ?
    """
    mod_quest_value = 2
    def turn_on(self, sequence: Sequence):
        self.quest_value += 1
        if self.quest_value % self.mod_quest_value == 0:
            minion_data = self.game.deck.exclude(battlegroundsPremiumDbfId=None).random_choice()
            self.controller.draw(minion_data.battlegroundsPremiumDbfId)


class BG21_019_G(BG21_019):
    # Pillarde curieuse
    mod_quest_value = 1


class BGS_061t(Minion):
    # pirate du ciel
    def summon_end(self, sequence: Sequence):
        self.combat()
TB_BaconUps_141t= BGS_061t # pirate du ciel premium


class BGS_060(Minion):
    # Yo oh ogre
    def combat_off(self, sequence: Sequence):
        if self is sequence.target:
            self.combat()
TB_BaconUps_150= BGS_060 # Yo oh ogre premium


BGS_061= deathrattle_repop # Forban
TB_BaconUps_141= BGS_061 # Forban premium

class BGS_055(Minion):
    # Mousse du pont
    bonus_value = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.controller.levelup_cost_mod -= self.bonus_value


class TB_BaconUps_126(BGS_055):
    # Mousse du pont premium
    bonus_value = 2


class BGS_048(battlecry_select_one_minion_and_buff_it):
    # Gaillarde des mers du Sud
    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.buff(sequence.target)

    @property
    def nb_strike(self) -> int:
        return len(self.controller.bought_minions[self.nb_turn].filter(race='PIRATE')) +1
TB_BaconUps_140= BGS_048 # Gaillarde des mers du Sud premium


class BGS_081(Minion):
    # Pillard pirate
    def play_on(self, sequence: Sequence):
        if sequence.source.race.PIRATE and sequence.is_ally(self):
            self.buff(self)
TB_BaconUps_143= BGS_081 # Pillard pirate premium


class BGS_049(Minion):
    # Parieuse convaincante
    bonus_value = 3
    def sell_start(self, sequence: Sequence):
        sequence.cost = self.bonus_value
        super().sell_start(sequence)


class TB_BaconUps_127(BGS_049):
    # Parieuse convaincante premium
    bonus_value = 6


class BGS_066(Minion):
    # Raflelor
    @repeat_effect
    def turn_off(self, sequence: Sequence):
        self.buff(self)

    @property
    def nb_strike(self) -> int:
        return len(self.my_zone.cards.filter(is_premium=True))
TB_BaconUps_130= BGS_066 # Raflelor premium



class BGS_047(Minion):
    # Amiral de l'effroi Eliza
    valid_for_myself = True
    def combat_on(self, sequence: Sequence):
        source = sequence.source
        if source.race.PIRATE and sequence.is_ally(self):
            for minion in self.my_zone.cards:
                self.buff(minion)
TB_BaconUps_134= BGS_047 # Amiral de l'effroi Eliza premium


class BGS_056(Minion):
    # Capitaine Grondéventre
    def combat_on(self, sequence: Sequence):
        source = sequence.source
        if source.race.PIRATE and sequence.is_ally(self):
            self.buff(source)
TB_BaconUps_139= BGS_056 # Capitaine Grondéventre premium


NEW1_027= aura_buff_race # Capitaine des mers du Sud
TB_BaconUps_136= NEW1_027 # Capitaine des mers du Sud premium


class BGS_072(Minion):
    # Captaine_Larrrrdeur
    bonus_value = 1

    def buy_off(self, source):
        if source.race.PIRATE:
            self.controller.gold += self.bonus_value


class TB_BaconUps_133(BGS_072):
    # Captaine_Larrrrdeur premium
    bonus_value = 2


class BGS_080(Minion):
    # Goliath brisemer 
    def overkill(self, sequence: Sequence):
        for minion in self.my_zone.cards.filter(race='PIRATE').exclude(self):
            self.buff(minion)
TB_BaconUps_142= BGS_080 # Goliath brisemer premium



class BGS_046(Minion):
    # Nat Pagle
    nb_strike = 1

    @repeat_effect
    def attack_end(self, sequence: Sequence):
        # n'est pas une découverte à 1 car peut se découvrir lui-même
        if not sequence.target.is_alive:
            self.controller.draw(
                self.controller.deck.random_choice()
            )


class TB_BaconUps_132(BGS_046):
    # Nat Pagle premium
    nb_strike = 2


BGS_053= battlecry_select_all_and_buff_them # Canonnier de la voile sanglante
TB_BaconUps_138= BGS_053 # Canonnier de la voile sanglante premium


class BGS_079(deathrattle_repop):
    # Tranche-les-vagues
    nb_repop = 3

    @property
    def repopDbfId(self) -> int:
        return self.game.minion_can_collect.filter(race='PIRATE').exlude(self.dbfId).random_choice()


class TB_BaconUps_137(BGS_079):
    # Tranche-les-vagues premium
    nb_repop = 6
