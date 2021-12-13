from base.entity import Minion
from base.enums import CardName
from base.scripts.base import *
import random
from base.utils import repeat_effect
from base.sequence import Sequence


class BG21_024(Minion):
    # Graiss-o-bot
    def loss_shield_off(self, sequence: Sequence):
        if sequence.source.my_zone is self.my_zone:
            self.buff(sequence.source)
BG21_024_G= BG21_024 # Graiss-o-bot premium


BOT_312t= Minion # Microbot
TB_BaconUps_032t= Minion # Microbot premium


class BG21_023(Minion):
    # Méca-tank
    nb_strike = 1

    @repeat_effect
    def avenge(self, sequence: Sequence):
        opponent_board = self.my_zone.opponent[:]
        random.shuffle(opponent_board)
        opponent_board.sort(key=lambda x: x.health)
        target = opponent_board[-1]
        self.damage(target, 5)


class BG21_023_G(BG21_023):
    # Méca-tank premium
    nb_strike = 2


class BG20_401(Minion):
    # Mécareau divin
    def loss_shield_off(self, sequence: Sequence):
        if sequence.is_ally(self):
            self.DIVINE_SHIELD = True
BG20_401_G= BG20_401 # Mécareau divin premium


class BG21_025(deathrattle_repop):
    # Casseur Oméga
    nb_repop = 5
    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        super().deathrattle(sequence)
        nb_minion_repop = len(sequence._repops)
        for minion in self.controller.board.cards.filter(race='MECHANICAL'):
            for _ in range(self.nb_repop - nb_minion_repop):
                self.buff(minion)
BG21_025_G= BG21_025 # Casseur Oméga premium


BOT_911= Minion # Ennuy-o-module
TB_BaconUps_099= Minion # Ennuy-o-module premium
BG21_022= Minion # Robo-toutou
BG21_022_G= Minion # Robo-toutou premium
BOT_537t= Minion  # Robosaure
TB_BaconUps_039t= Minion # Robosaure premium 
BOT_218t= Minion # Robot gardien
TB_BaconUps_041t= Minion # Robot gardien premium
skele21= Minion # Golem endommagé
TB_BaconUps_006t= Minion # Golem endommagé premium


class GVG_113(Minion):
    # Faucheur 4000
    pass

class TB_BaconUps_153(Minion):
    # Faucheur 4000 premium
    pass


class BOT_312(deathrattle_repop):
    # Menace répliquante
    nb_repop = 3
TB_BaconUps_032= BOT_312 # Menace répliquante premium


# TODO: flexibilité à revoir
class BOT_312e(add_stat):
    # Menace répliquante (enchantment)
    nb_repop = BOT_312.nb_repop
    deathrattle = BOT_312.deathrattle


# TODO: flexibilité à revoir
class TB_BaconUps_032e(add_stat):
    # Menace répliquante premium (enchantement)
    nb_repop = TB_BaconUps_032.nb_repop
    deathrattle = TB_BaconUps_032.deathrattle


class BOT_606(Minion):
    # Gro'Boum
    nb_strike = 1

    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        if self.controller.opponent.board.cards:
            self.damage(
                self.controller.opponent.board.cards.random_choice(),
                4,
                overkill=False)


class TB_BaconUps_028(BOT_606):
    # Gro'Boum premium
    nb_strike = 2


GVG_055= battlecry_select_one_minion_and_buff_it # Cliqueteur percevrille
TB_BaconUps_069= GVG_055 # Cliqueteur percevrille premium
GVG_048= battlecry_select_all_and_buff_them # Bondisseur dent de métal
TB_BaconUps_066= GVG_048 # Bondisseur dent de métal premium

EX1_556= deathrattle_repop # Golem des moissons
TB_BaconUps_006= EX1_556 # Golem des moissons premium
BOT_537= deathrattle_repop # Mecanoeuf
TB_BaconUps_038e= BOT_537 # Mecanoeuf premium


class BGS_071(Minion):
    # Déflect-o-bot
    def summon_off(self, sequence: Sequence):
        if self.in_fight_sequence and\
                sequence.source.race.MECHANICAL:
            self.buff(self)
TB_BaconUps_123= BGS_071 # Déflect-o-bot premium


class ULD_217(Minion):
    # Micromomie
    def turn_off(self, sequence: Sequence):
        self.buff(
            self.owner.cards.exclude(self).random_choice()
        )
TB_BaconUps_250= ULD_217 # Micromomie premium


class BGS_012(Minion):
    # Apprentie de Kangor
    nb_repop = 2

    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        for repop in self.controller.graveyard.entities.filter(race='MECHANICAL')[:self.nb_repop]:
            self.invoc(sequence, repop.dbfId)


class TB_BaconUps_087(BGS_012):
    # Apprentie de Kangor premium
    nb_repop = 4


class GVG_027(Minion):
    # Sensei de fer
    def turn_off(self, sequence: Sequence):
        self.buff(
            self.my_zone.cards.filter(race='MECHANICAL').exclude(self).random_choice()
        )
TB_BaconUps_044= GVG_027 # Sensei de fer premium


class BGS_027(Minion):
    # Micro-machine
    def turn_on(self, sequence: Sequence):
        sequence(self.buff, self)
TB_BaconUps_094= BGS_027 # Micro-machine premium


class GVG_106(Minion):
    # Brik-a-bot
    def die_off(self, sequence: Sequence):
        if sequence.is_ally(self) and sequence.source.race.MECHANICAL:
            self.buff(self)
TB_BaconUps_046= GVG_106 # Brik-a-bot premium


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


class BGS_006(deathrattle_repop):
    # Vieux déchiqueteur de Sneed
    nb_repop = 1

    @property
    def repopDbfId(self):
        cards = self.game.minion_can_collect.filter(elite=True).exlude(self.dbfId)
        return random.choice(cards)


class TB_BaconUps_080(BGS_006):
    # Vieux déchiqueteur de Sneed premium
    nb_repop = 2


BOT_218= hit_by_repop # Rover de sécurité
TB_BaconUps_041= BOT_218 # Rover de sécurité premium
