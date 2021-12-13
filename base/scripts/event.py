from .power import *
from .spell import *
from .enchantment import *
from base.board import Board, Bob_board, Graveyard, Secret_board, Player_board
from game import Game
from base.player import Player, Bob
from base.field import Field
from base.entity import Card
from .minions import *


class no_method:
    pass


class player(Player):
    def turn_on(self, sequence):
        self.levelup_cost_mod -= 1
        self.gold = self.nb_gold_by_turn()
        self.power.enable()

        for entity in self.field.cards:
            # TODO: Effectuer deux fois ? A vérifier
            entity.calc_stat_from_scratch(heal=True)


TB_BaconShop_HERO_PH = player
BG20_HERO_101 = player
TB_BaconShop_HERO_01 = player
TB_BaconShop_HERO_08 = player
TB_BaconShop_HERO_11 = player
TB_BaconShop_HERO_12 = player
TB_BaconShop_HERO_14 = player
TB_BaconShop_HERO_15 = player
TB_BaconShop_HERO_16 = player
TB_BaconShop_HERO_17 = player
TB_BaconShop_HERO_18 = player
TB_BaconShop_HERO_21 = player
TB_BaconShop_HERO_22 = player
TB_BaconShop_HERO_25 = player
TB_BaconShop_HERO_27 = player
TB_BaconShop_HERO_28 = player
TB_BaconShop_HERO_29 = player
TB_BaconShop_HERO_33 = player
TB_BaconShop_HERO_34 = player
TB_BaconShop_HERO_35 = player
TB_BaconShop_HERO_36 = player
TB_BaconShop_HERO_37 = player
TB_BaconShop_HERO_38 = player
TB_BaconShop_HERO_39 = player
TB_BaconShop_HERO_40 = player
TB_BaconShop_HERO_41 = player
TB_BaconShop_HERO_42 = player
TB_BaconShop_HERO_43 = player
TB_BaconShop_HERO_49 = player
TB_BaconShop_HERO_50 = player
TB_BaconShop_HERO_52 = player
TB_BaconShop_HERO_53 = player
TB_BaconShop_HERO_55 = player
TB_BaconShop_HERO_56 = player
TB_BaconShop_HERO_57 = player
TB_BaconShop_HERO_59 = player
TB_BaconShop_HERO_60 = player
TB_BaconShop_HERO_62 = player
TB_BaconShop_HERO_64 = player
TB_BaconShop_HERO_67 = player
TB_BaconShop_HERO_68 = player
TB_BaconShop_HERO_70 = player
TB_BaconShop_HERO_71 = player
TB_BaconShop_HERO_72 = player
TB_BaconShop_HERO_74 = player
TB_BaconShop_HERO_75 = player
TB_BaconShop_HERO_76 = player
TB_BaconShop_HERO_78 = player
TB_BaconShop_HERO_90 = player
TB_BaconShop_HERO_91 = player
TB_BaconShop_HERO_92 = player
TB_BaconShop_HERO_93 = player
TB_BaconShop_HERO_94 = player
TB_BaconShop_HERO_95 = player
BG20_HERO_102 = player
BG20_HERO_103 = player
BG20_HERO_201 = player
BG20_HERO_202 = player  # N'Guyen
BG20_HERO_242 = player
BG20_HERO_280 = player
BG20_HERO_301 = player
TB_BaconShop_HERO_KelThuzad = player  # Kel’Thuzad

