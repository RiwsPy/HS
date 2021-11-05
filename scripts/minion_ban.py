from entity import Minion
from enums import CardName
import random

class AT_121(Minion):
    # Favori de la foule
    def play_on(self, sequence):
        if sequence.source.BATTLECRY:
            self.buff(self.enchantment_dbfId, self)
TB_BaconUps_037= AT_121 # Favori de la foule premium


class BGS_080(Minion):
    # Goliath brisemer 
    def overkill(self, sequence):
        for minion in self.my_zone.cards.filter(race='PIRATE').exclude(self):
            self.buff(self.enchantment_dbfId, minion)
TB_BaconUps_142= BGS_080 # Goliath brisemer premium


class TRL_232(Minion):        
    # Navrecorne cuiracier
    def overkill(self, sequence):
        self.invoc(sequence, self.repop_dbfId)
TB_BaconUps_051= TRL_232 # Navrecorne cuiracier premium


class BAR_073(Minion):
    # Forgeronne des Tarides
    def frenzy(self, sequence):
        for minion in self.my_zone.cards.exclude(self):
            self.buff(self.enchantment_dbfId, minion)
TB_BaconUps_320= BAR_073 # Forgeronne des Tarides premium


class BGS_124(Minion):
    # Lieutenant Garr
    def play_off(self, sequence):
        if self is not sequence.source and sequence.source.race.ELEMENTAL:
            for _ in self.my_zone.cards.filter(race='ELEMENTAL'):
                self.buff(self.enchantment_dbfId, self)
TB_BaconUps_163= BGS_124 # Lieutenant Garr premium


class BGS_202(Minion):
    # Mythrax
    def turn_off(self, sequence):
        nb = len(self.my_zone.cards.one_minion_by_type())
        for _ in range(nb):
            self.buff(self.enchantment_dbfId, self)
TB_BaconUps_258= BGS_202 # Mythrax premium


class BGS_112(Minion):
    # Héraut qiraji
    def die_on(self, sequence):
        if sequence.source.TAUNT and sequence.source.controller is self.controller:
            for minion in sequence.source.adjacent_neighbors():
                sequence(self.buff, self.enchantment_dbfId, minion)
TB_BaconUps_303= BGS_112 # Héraut qiraji premium


class BGS_200(Minion):
    # Gardienne d'antan
    nb_strike = 1
    def deathrattle(self, sequence):
        self.controller.hand.create_card_in(CardName.COIN)


class TB_BaconUps_256(BGS_200):
    # Gardienne d'antan premium
    nb_strike = 2



class BGS_201(Minion):
    # Ritualiste tourmenté
    def combat_on(self, sequence):
        if self in sequence.targets:
            self.buff(self.enchantment_dbfId, *self.adjacent_neighbors())
TB_BaconUps_257= BGS_201


class BGS_046(Minion):
    # Nat Pagle
    nb_strike = 1
    def attack_end(self, sequence):
        # n'est pas une découverte à 1 car peut se découvrir lui-même
        for minion in sequence.targets:
            if not minion.is_alive:
                lst = self.controller.bob.local_hand
                if lst:
                    self.controller.hand.append(random.choice(lst))


class TB_BaconUps_132(BGS_046):
    # Nat Pagle premium
    nb_strike = 2


class GVG_027(Minion):
    # Sensei de fer
    def turn_off(self, sequence):
        lst = self.my_zone.cards.filter(race='MECHANICAL').exclude(self)
        if lst:
            self.buff(self.enchantment_dbfId, random.choice(lst))
TB_BaconUps_044= GVG_027 # Sensei de fer premium


class BGS_033(Minion):
    # Dragon infâmélique
    def turn_on(self, sequence):
        if self.controller.win_last_match:
            self.buff(self.enchantment_dbfId, self)
TB_BaconUps_104= BGS_033 # Dragon infâmélique premium


class BG20_210(Minion):
    # Maraudeur des ruines
    def turn_off(self, sequence):
        if self.my_zone.size <= 6:
            self.buff(self.enchantment_dbfId, self)
BG20_210_G= BG20_210 # Maraudeur des ruines premium


class BGS_027(Minion):
    # Micro-machine
    def turn_on(self, sequence):
        sequence(self.buff, self.enchantment_dbfId, self)
TB_BaconUps_094= BGS_027 # Micro-machine premium