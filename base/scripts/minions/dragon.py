from base.entity import Minion
from base.enums import CardName
from base.scripts.base import *
from base.utils import repeat_effect
from base.sequence import Sequence


class BG21_013(Minion):
    # Contrebandier dragonnet
    # Partiellement faux : Pouvoir de Vol'Jin
    #TODO: test
    valid_for_myself = True
    def enhance_on(self, sequence: Sequence):
        self.quest_value = getattr(sequence.target, 'attack', None)

    def enhance_off(self, sequence: Sequence):
        if self.quest_value is not None and sequence.target.race.DRAGON and\
                sequence.target.controller is self.controller and\
                self.quest_value < sequence.target.attack:
            self.buff(sequence.target)
BG21_013_G= BG21_013 # Contrebandier dragonnet premium


class BG21_015(Minion):
    # Tarecgosa
    #TODO: rendre compatible avec le bonus de Nadina ou Héroïne altruiste
    def enhance_on(self, sequence: Sequence):
        if self.in_fight_sequence and sequence.target is self:
            try:
                del sequence.source.duration
            except AttributeError:
                pass


class BG21_015_G(BG21_015):
    # Tarecgosa premium
    def enhance_on(self, sequence: Sequence):
        if self.in_fight_sequence and sequence.target is self:
            super().enhance_on(sequence)
            #TODO: copy


class BG21_012(Minion):
    # Pyrogéniture de Prestor
    bonus_value = 3

    def combat_on(self, sequence: Sequence):
        if sequence.source.my_zone is self.my_zone and\
                sequence.source.race.DRAGON:
            sequence(self.damage, sequence.target, self.bonus_value)


class BG21_012_G(BG21_012):
    # Pyrogéniture de Prestor
    bonus_value = 6


class BG21_014(Minion):
    # Super promo-Drake
    bonus_value = 1
    @repeat_effect
    def fight_on(self, sequence: Sequence):
        for minion in self.adjacent_neighbors():
            self.buff(minion,
                attack=self.bonus_value,
                max_health=self.bonus_value)

    @property
    def nb_strike(self) -> int:
        return len(self.my_zone.filter(race='DRAGON'))


class BG21_014_G(BG21_014):
    # Super promo-Drake premium
    bonus_value = 2


BGS_034= Minion # Gardien de bronze
TB_BaconUps_149= Minion # Gardien de bronze premium


class BG21_027(Minion):
    # Chromaile évolutive
    def levelup_off(self, sequence: Sequence):
        self.buff(self, attack=self.bonus_value)

    @property
    def bonus_value(self) -> int:
        return self.attack


class BG21_027_G(Minion):
    # Chromaile évolutive premium
    @property
    def bonus_value(self) -> int:
        return self.attack*2


class BGS_040(Minion):
    # Nadina
    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        for minion in self.my_zone.cards.filter(race='DRAGON'):
            minion.DIVINE_SHIELD = True
TB_BaconUps_154= BGS_040 # Nadina premium


BGS_038= battlecry_select_one_minion_and_buff_it # Emissaire du crépuscule
TB_BaconUps_108= BGS_038 # Emissaire du crépuscule premium


class BGS_045(Minion):
    # Gardien des glyphes
    def combat_start(self, sequence: Sequence):
        super().combat_start(sequence)
        if sequence.is_valid:
            self.buff(
                self,
                attack=self.bonus_value)

    @property
    def bonus_value(self) -> int:
        return self.attack


class TB_BaconUps_115(BGS_045):
    # Gardien des glyphes premium
    @property
    def bonus_value(self) -> int:
        return self.attack*2


class BGS_019(Minion):
    # Dragonnet rouge
    nb_strike = 1

    @repeat_effect
    def fight_on(self, sequence: Sequence):
        nb_dragon_in_board = len(self.my_zone.cards.filter(race='DRAGON'))
        sequence(
            self.damage,
            self.my_zone.opponent.cards.random_choice(),
            nb_dragon_in_board,
            overkill=False)


class TB_BaconUps_102(BGS_019):
    # Dragonnet rouge premium
    nb_strike = 2


class BGS_041(Minion):
    # Kalecgos
    def play_off(self, sequence: Sequence):
        if sequence.source.BATTLECRY and sequence.is_ally(self):
            for minion in self.my_zone.cards.filter(race='DRAGON'):
                self.buff(minion)
TB_BaconUps_109=BGS_041  # Kalecgos premium



class BGS_067(Minion):
    # Massacreur drakonide
    valid_for_myself = True
    def loss_shield_off(self, sequence: Sequence):
        if sequence.is_ally(self):
            self.buff(self)
TB_BaconUps_117= BGS_067 # Massacreur drakonide premium



class ICC_029(Minion):
    # Plaiedécailles cobalt
    def turn_off(self, sequence: Sequence):
        self.buff(
            self.owner.cards.exclude(self).random_choice()
        )
TB_BaconUps_120= ICC_029 # Plaiedécailles cobalt premium


class BGS_036(Minion):
    # Tranchetripe
    def turn_off(self, sequence: Sequence):
        self.buff(self,
            max_health=self.bonus_value,
            attack=self.bonus_value)

    @property
    def bonus_value(self) -> int:
        return len(self.my_zone.cards.filter(race='DRAGON'))


class TB_BaconUps_106(BGS_036):
    # Tranchetripe premium
    @property
    def bonus_value(self) -> int:
        return super().bonus_value*2


class BGS_043(Minion):
    # Murozond
    # les cartes sont retirées du pool
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        if self.my_zone.last_opponent:
            target = self.my_zone.last_opponent.cards_save[-1].random_choice()
            if target:
                dbfId = target.dbfId
                if target.is_premium:
                    dbfId = target.battlegroundsNormalDbfId
                self.controller.draw(dbfId)


class MTB_BaconUps_110(BGS_043):
    # Murozond premium
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        if self.my_zone.last_opponent:
            target = self.my_zone.last_opponent.cards_save[-1].\
                exclude(dbfId=self.dbfId).random_choice()
            if target:
                dbfId = target.dbfId
                if not target.is_premium and\
                        getattr(target, 'battlegroundsPremiumDbfId', False):
                    dbfId = target.battlegroundsPremiumDbfId
                self.controller.draw(dbfId)


class BGS_033(Minion):
    # Dragon infâmélique
    def turn_on(self, sequence: Sequence):
        if self.controller.win_last_match:
            self.buff(self)
TB_BaconUps_104= BGS_033 # Dragon infâmélique premium


class BGS_037(Minion):
    # Régisseur du temps
    def sell_start(self, sequence: Sequence):
        super().sell_start(sequence)
        if sequence.is_valid:
            sequence(self.buff, self.enchantmentDbfId, *self.my_zone.opponent.cards)
TB_BaconUps_107= BGS_037 # Régisseur du temps premium


class BGS_035(Minion):
    # Trotte-bougie
    def die_off(self, sequence: Sequence):
        if sequence.source.race.DRAGON and not sequence.is_ally(self):
            self.buff(self)
TB_BaconUps_105= BGS_035 # Trotte-bougie premium


class BGS_032(Minion):
    bonus_value = 3
    # Héraut de la flamme
    def overkill(self, sequence: Sequence):
        for minion in self.my_zone.opponent:
            if minion.is_alive:
                self.append_action(
                    self.damage,
                    minion,
                    self.bonus_value)
                break


class TB_BaconUps_103(BGS_032):
    # Héraut de la flamme premium
    bonus_value = 6

BGS_039= Minion # Lieutenant draconide
TB_BaconUps_146= Minion # Lieutenant draconide premium
