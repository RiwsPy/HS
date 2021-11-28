from base.entity import Minion
from base.enums import CardName
import random
from .base import *
from base.utils import repeat_effect
from base.sequence import Sequence


class AT_121(Minion):
    # Favori de la foule
    def play_on(self, sequence: Sequence):
        if sequence.source.BATTLECRY:
            self.buff(self)
TB_BaconUps_037= AT_121 # Favori de la foule premium


class BGS_080(Minion):
    # Goliath brisemer 
    def overkill(self, sequence: Sequence):
        for minion in self.my_zone.cards.filter(race='PIRATE').exclude(self):
            self.buff(minion)
TB_BaconUps_142= BGS_080 # Goliath brisemer premium



class BAR_073(Minion):
    # Forgeronne des Tarides
    def frenzy(self, sequence: Sequence):
        for minion in self.my_zone.cards.exclude(self):
            self.buff(minion)
TB_BaconUps_320= BAR_073 # Forgeronne des Tarides premium


class BGS_124(Minion):
    # Lieutenant Garr
    def play_off(self, sequence: Sequence):
        if self is not sequence.source and sequence.source.race.ELEMENTAL:
            for _ in self.my_zone.cards.filter(race='ELEMENTAL'):
                self.buff(self)
TB_BaconUps_163= BGS_124 # Lieutenant Garr premium


class BGS_112(Minion):
    # Héraut qiraji
    def die_on(self, sequence: Sequence):
        if sequence.source.TAUNT and sequence.is_ally(self):
            for minion in sequence.source.adjacent_neighbors():
                sequence(self.buff, self.enchantmentDbfId, minion)
TB_BaconUps_303= BGS_112 # Héraut qiraji premium


class BGS_200(Minion):
    # Gardienne d'antan
    nb_strike = 1

    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        self.controller.draw(CardName.COIN)


class TB_BaconUps_256(BGS_200):
    # Gardienne d'antan premium
    nb_strike = 2



class BGS_201(Minion):
    # Ritualiste tourmenté
    def combat_on(self, sequence: Sequence):
        if self is sequence.target:
            for minion in self.adjacent_neighbors():
                self.buff(minion)
TB_BaconUps_257= BGS_201


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


class GVG_027(Minion):
    # Sensei de fer
    def turn_off(self, sequence: Sequence):
        self.buff(
            self.my_zone.cards.filter(race='MECHANICAL').exclude(self).random_choice()
        )
TB_BaconUps_044= GVG_027 # Sensei de fer premium


class BGS_033(Minion):
    # Dragon infâmélique
    def turn_on(self, sequence: Sequence):
        if self.controller.win_last_match:
            self.buff(self)
TB_BaconUps_104= BGS_033 # Dragon infâmélique premium


class BG20_210(Minion):
    # Maraudeur des ruines
    def turn_off(self, sequence: Sequence):
        if self.my_zone.size <= 6:
            self.buff(self)
BG20_210_G= BG20_210 # Maraudeur des ruines premium


class BGS_027(Minion):
    # Micro-machine
    def turn_on(self, sequence: Sequence):
        sequence(self.buff, self)
TB_BaconUps_094= BGS_027 # Micro-machine premium


class BGS_113(Minion):
    # Habitue_sans_visage
    @repeat_effect
    def battlecry(self, sequence: Sequence):
        # comment se passe la gestion lors de la revente, la copie est enlevée de la taverne ou est-ce 
        # l'habitué ?
        pass
TB_BaconUps_305= BGS_113 # Habitue_sans_visage premium


class GVG_106(Minion):
    # Brik-a-bot
    def die_off(self, sequence: Sequence):
        if sequence.is_ally(self) and sequence.source.race.MECHANICAL:
            self.buff(self)
TB_BaconUps_046= GVG_106 # Brik-a-bot premium


class EX1_509(Minion):
    # Mande-flots murloc
    def summon_on(self, sequence: Sequence):
        if sequence.source.race.MURLOC:
            self.buff(self)
TB_BaconUps_011= EX1_509 # Mande-flots murloc premium


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


ICC_038= minion_without_script # Protectrice vertueuse
TB_BaconUps_147= minion_without_script # Protectrice vertueuse premium


class BGS_028(Minion):
    # Lapin-échasseur
    #TODO sequence.nb_strike à changer (obsolète) 
    def play_start(self, sequence: Sequence):
        super().play_start(sequence)
        played_lapin = 0
        for minion_list in self.controller.played_cards.values():
            played_lapin += minion_list.count(CardName.LAPIN)
            played_lapin += minion_list.count(CardName.LAPIN_P)
        sequence.nb_strike = played_lapin

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.buff(self)
TB_BaconUps_077= BGS_028 # Lapin-échasseur premium
