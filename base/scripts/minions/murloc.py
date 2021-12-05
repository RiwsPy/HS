from base.entity import Minion
from base.enums import CardName, Zone
from base.scripts.base import *
import random
from base.utils import repeat_effect
from base.sequence import Sequence


class BG21_008(Minion):
    # Boss écailles-salines
    def play_off(self, sequence: Sequence):
        if sequence.source.race.MURLOC and sequence.is_ally(self):
            targets = self.my_zone.cards.filter(race='MURLOC').exclude(self).shuffle()
            for target in targets[:2]:
                self.buff(target)
BG21_008_G= BG21_008 # Boss écailles-salines premium


class BG21_010(battlecry_buff_myself):
    # Gonflalairon
    @property
    def nb_strike(self):
        return len(self.owner.cards.filter(race='MURLOC').exclude(self))
BG21_010_G= BG21_010 # Gonflalairon premium


class BG21_009(Minion):
    #SI:septique
    nb_strike = 1

    @repeat_effect
    def avenge(self, sequence: Sequence):
        targets = self.my_zone.cards.filter(race='MURLOC', POISONOUS=False, is_alive=True)
        if targets:
            self.buff(random.choice(targets))


class BG21_009_G(BG21_009):
    #SI:septique
    nb_strike = 2


class BG21_011(Minion):
    # Lanceur de crustacés
    def play_start(self, sequence: Sequence):
        super().play_start(sequence)
        if sequence.is_valid:
            sequence.add_target(
                self.controller.field.cards.filter(race=self.synergy).\
                    exclude(battlegroundsPremiumDbfId=None).choice(self.controller)
            )

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        target = sequence.target
        if target:
            target.set_premium()
BG21_011_G= BG21_011 # Lanceur de crustacés premium


class EX1_062(Minion):
    # Vieux troubloeil
    bonus_value = 1
    @property
    def attack(self):
        bonus = 0
        if self.my_zone.zone_type == Zone.PLAY:
            for entity in self.owner.cards + getattr(self.owner.opponent, 'cards', []):
                if entity.race.MURLOC and entity is not self:
                    bonus += self.bonus_value
        return super().attack + bonus

    @attack.setter
    def attack(self, value):
        self._attack = value


class TB_BaconUps_036(EX1_062):
    # Vieux troubloeil premium
    bonus_value = 2

VAN_EX1_506a= Minion # éclaireur murloc
TB_BaconUps_003t= Minion # éclaireur murloc premium

BT_010= battlecry_select_all_and_buff_them # Navigateur gangraileron
TB_BaconUps_124= BT_010 # Navigateur gangraileron premium
EX1_103= battlecry_select_all_and_buff_them # Voyant froide lumière
TB_BaconUps_064= EX1_103 # Voyant froide lumière premium

UNG_073= battlecry_select_one_minion_and_buff_it # Chasseur rochecave
TB_BaconUps_061= UNG_073 # Chasseur rochecave premium


class BGS_030(battlecry_select_all_and_buff_them):
    # Roi Bagargouille
    deathrattle= battlecry_select_all_and_buff_them.battlecry
TB_BaconUps_100= BGS_030 # Roi Bagargouille premium


class EX1_506(Minion):
    # chasse-marée

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.invoc(sequence, self.repopDbfId)
TB_BaconUps_003= EX1_506 # chasse-marée premium

class BGS_020(Minion):
    # Guetteur primaileron
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        if self.my_zone.cards.filter(race='MURLOC').exclude(self):
            self.controller.draw(
                self.discover(
                    self.controller.deck.filter(race='MURLOC'),
                    nb=3
                )
            )


class TB_BaconUps_089(BGS_020):
    # Guetteur primaileron premium
    nb_strike = 2


EX1_507= aura_buff_race # Chef de guerre murloc
TB_BaconUps_008= EX1_507 # Chef de guerre murloc premium


class EX1_509(Minion):
    # Mande-flots murloc
    def summon_on(self, sequence: Sequence):
        if sequence.source.race.MURLOC:
            self.buff(self)
TB_BaconUps_011= EX1_509 # Mande-flots murloc premium

DAL_077= battlecry_select_one_minion_and_buff_it # Aileron toxique
TB_BaconUps_152= DAL_077 # Aileron toxique premium
