# coding : utf-8

import random
from base.db_card import Card_data
from base.enums import BOARD_SIZE, CardName, Zone, ADAPT_ENCHANTMENT
from base.utils import *
from base.action import *
from base.entity import Minion
from base.sequence import Sequence
from .base import *



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


class BGS_104(Minion):
    # Nomi
    #TODO: à compléter, n'affecte pas les serviteurs déjà présents dans la taverne
    bonus_value = 1
    def play_off(self, sequence: Sequence):
        # s'active après le battlecry de l'élémentaire de stase
        if sequence.is_ally(self) and sequence.source.race.ELEMENTAL:
            self.buff(
                self.controller,
                bonus_value=self.bonus_value
            )


class TB_BaconUps_201(BGS_104):
    # Nomi premium
    bonus_value = 2


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


class BGS_072(Minion):
    # Captaine_Larrrrdeur
    bonus_value = 1

    def buy_off(self, source):
        if source.race.PIRATE:
            self.controller.gold += self.bonus_value


class TB_BaconUps_133(BGS_072):
    # Captaine_Larrrrdeur premium
    bonus_value = 2


class BGS_059(battlecry_select_one_minion_and_buff_it):
    # Dévoreur d'âmes
    bonus_mult = 1
    @repeat_effect
    def battlecry(self, sequence: Sequence):
        target = sequence.target
        if target.my_zone is self.my_zone:
            self.controller.bob.hand.append(target)
            self.controller.gold += 3*self.bonus_mult
            self.buff(
                self,
                attack=target.attack*self.bonus_mult,
                max_health=target.health*self.bonus_mult)


class TB_BaconUps_119(BGS_059):
    # Dévoreur d'âmes premium
    bonus_mult = 2


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


class GVG_021(aura_buff_race):
    # Mal'Ganis
    def summon_start(self, sequence: Sequence):
        super().summon_start(sequence)
        if sequence.is_valid:
            self.buff(self.controller, -2203)
TB_BaconUps_060= GVG_021 # Mal'Ganis premium

EX1_185= aura_buff_race # Brise-siège
TB_BaconUps_053= EX1_185 # Brise-siège premium
EX1_507= aura_buff_race # Chef de guerre murloc
TB_BaconUps_008= EX1_507 # Chef de guerre murloc premium
NEW1_027= aura_buff_race # Capitaine des mers du Sud
TB_BaconUps_136= NEW1_027 # Capitaine des mers du Sud premium


class BGS_111(Minion):
    # Champion d'Y'Shaarj
    valid_for_myself = True
    def combat_on(self, sequence: Sequence):
        if sequence.target.TAUNT and sequence.is_ally(self):
            self.buff(self)
TB_BaconUps_301= BGS_111 # Champion d'Yshaarj premium
BGS_110= BGS_111 # Bras de l'empire
TB_BaconUps_302= BGS_110 # Bras de l'empire premium


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


class LOE_077(Minion):
    # Brann
    #TODO: l'effet d'un Brann doré se cumule-t-il avec celui d'un Brann non doré ?
    # (parti du principe que non)
    # Même questionnement pour Baron Vaillefendre
    def battlecry_on(self, sequence: Sequence):
        sequence.double_effect = True


class TB_BaconUps_045(LOE_077):
    # Brann premium
    def battlecry_on(self, sequence: Sequence):
        sequence.triple_effect = True


class FP1_031(Minion):
    # Baron_Vaillefendre
    def deathrattle_on(self, sequence: Sequence):
        sequence.double_effect = True


class TB_BaconUps_055(Minion):
    # Baron_Vaillefendre premium
    def deathrattle_on(self, sequence: Sequence):
        sequence.triple_effect = True


class DAL_575(Minion):
    # Khadgar
    # les cartes invoquées sont buffées par les summon_on avant d'être copiées
    nb_strike = 1


class TB_BaconUps_034(DAL_575):
    # Khadgar premium
    nb_strike = 2


class BGS_066(Minion):
    # Raflelor
    @repeat_effect
    def turn_off(self, sequence: Sequence):
        self.buff(self)

    @property
    def nb_strike(self) -> int:
        return len(self.my_zone.cards.filter(is_premium=True))
TB_BaconUps_130= BGS_066 # Raflelor premium


class ULD_217(Minion):
    # Micromomie
    def turn_off(self, sequence: Sequence):
        self.buff(
            self.owner.cards.exclude(self).random_choice()
        )
TB_BaconUps_250= ULD_217 # Micromomie premium
ICC_029= ULD_217 # Plaiedécailles cobalt
TB_BaconUps_120= ICC_029 # Plaiedécailles cobalt premium


class BGS_105(Minion):
    # Chambellan Executus
    bonus_value = 1

    @repeat_effect
    def turn_off(self, sequence: Sequence):
        self.buff(
            self.my_zone[0],
            attack=self.bonus_value,
            max_health=self.bonus_value)

    @property
    def nb_strike(self) -> int:
        return self.controller.played_cards[self.nb_turn].filter(type='MINION', race='ELEMENTAL')+1

class TB_BaconUps_207(BGS_105):
    # Chambellan Executus premium
    bonus_value = 2


class BGS_009(Minion):
    # Massacreuse croc radieux
    def turn_off(self, sequence: Sequence):
        for minion in self.my_zone.cards.one_minion_by_race():
            self.buff(minion)
TB_BaconUps_082= BGS_009  # Massacreuse croc radieux premium


class BGS_115(Minion):
    # Élémenplus
    nb_strike = 1

    @repeat_effect
    def sell_end(self, sequence: Sequence):
        self.controller.draw(64040)


class TB_BaconUps_156(Minion):
    # Élémenplus premium
    nb_strike = 2


class BG20_301(Minion):
    # Bronze couenne
    nb_strike = 2

    @repeat_effect
    def sell_end(self, sequence: Sequence):
        self.controller.draw(CardName.BLOOD_GEM)


class BG20_301_G(BG20_301):
    # Bronze couenne premium
    nb_strike = 4


class BG20_100(Minion):
    # Géomancien de Tranchebauge
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.controller.draw(CardName.BLOOD_GEM)


class BG20_100_G(BG20_100):
    # Géomancien de Tranchebauge premium
    nb_strike = 2


class BGS_037(Minion):
    # Régisseur du temps
    def sell_start(self, sequence: Sequence):
        super().sell_start(sequence)
        if sequence.is_valid:
            sequence(self.buff, self.enchantmentDbfId, *self.my_zone.opponent.cards)
TB_BaconUps_107= BGS_037 # Régisseur du temps premium


class BGS_049(Minion):
    # Parieuse convaincante
    bonus_value = 3
    def sell_start(self, sequence: Sequence):
        sequence.cost = self.bonus_value
        super().sell_start(sequence)


class TB_BaconUps_127(BGS_049):
    # Parieuse convaincante premium
    bonus_value = 6


class ICC_858(Minion):
    # Bolvar sang-de-feu
    valid_for_myself = True
    def loss_shield_off(self, sequence: Sequence):
        if sequence.is_ally(self):
            self.buff(self)
TB_BaconUps_047= ICC_858 # Bolvar sang-de-feu premium
BGS_067= ICC_858 # Massacreur drakonide
TB_BaconUps_117= BGS_067 # Massacreur drakonide premium


class BGS_004(Minion):
    # Tisse-colère
    def play_off(self, sequence: Sequence):
        if sequence.is_ally(self) and sequence.source.race.DEMON:
            self.damage(self.controller, 1)
            self.buff(self)
TB_BaconUps_079= BGS_004 # Tisse-colère premium


class BGS_100(Minion):
    # Mini Rag
    nb_strike = 1

    @repeat_effect
    def play_off(self, sequence: Sequence):
        if sequence.source.race.ELEMENTAL:
            self.buff(
                self.my_zone.cards.random_choice(),
                attack=sequence.source.level,
                max_health=sequence.source.level)


class TB_BaconUps_200(BGS_100):
    # Mini Rag premium
    nb_strike = 2


class BGS_081(Minion):
    # Pillard pirate
    def play_on(self, sequence: Sequence):
        if sequence.source.race.PIRATE and sequence.is_ally(self):
            self.buff(self)
TB_BaconUps_143= BGS_081 # Pillard pirate premium


class BGS_041(Minion):
    # Kalecgos
    def play_off(self, sequence: Sequence):
        if sequence.source.BATTLECRY and sequence.is_ally(self):
            for minion in self.my_zone.cards.filter(race='DRAGON'):
                self.buff(minion)
TB_BaconUps_109=BGS_041  # Kalecgos premium


class BGS_075(Minion):
    # Saurolisque enragé
    def play_off(self, sequence: Sequence):
        if sequence.source.DEATHRATTLE and sequence.is_ally(self):
            self.buff(self)
TB_BaconUps_125= BGS_075 # Saurolisque enragé premium


class BGS_127(Minion):
    # Roche en fusion
    def play_off(self, sequence: Sequence):
        if sequence.source.race.ELEMENTAL and sequence.is_ally(self):
            self.buff(self)
TB_Baconups_202= BGS_127 # Roche en fusion premium


class BGS_120(Minion):
    # Elémentaire de fête
    nb_strike = 1

    @repeat_effect
    def play_off(self, sequence: Sequence):
        if sequence.source.race.ELEMENTAL and sequence.is_ally(self):
            self.buff(
                self.my_zone.cards.filter(race='ELEMENTAL').exclude(self).random_choice()
            )


class TB_BaconUps_160(Minion):
    # Elémentaire de fête premium
    nb_strike = 2


class BGS_204(Minion):
    # Démon démesuré
    def play_off(self, sequence: Sequence):
        if sequence.is_ally(self) and sequence.source.race.DEMON:
            self.buff(self)
TB_BaconUps_304= BGS_204 # Démon démesuré premium


class BGS_017(Minion):
    # Chef de meute
    def summon_off(self, sequence: Sequence):
        source = sequence.source
        if sequence.is_ally(self) and source.race.BEAST:
            self.buff(source)
TB_BaconUps_086= BGS_017 # Chef de meute premium
BGS_021= BGS_017 # Maman ourse
TB_BaconUps_090= BGS_017 # Maman ourse premium


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


class BGS_071(Minion):
    # Déflect-o-bot
    def summon_off(self, sequence: Sequence):
        if self.in_fight_sequence and\
                sequence.source.race.MECHANICAL:
            self.buff(self)


class TB_BaconUps_123(BGS_071):
    # Déflect-o-bot premium
    pass


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


class EX1_531(Minion):
    # Hyène_charognarde
    # la hyène est buff après l'activation du râle
    def die_off(self, sequence: Sequence):
        if sequence.is_ally(self) and sequence.source.race.BEAST:
            self.buff(self)
TB_BaconUps_043= EX1_531 # Hyène_charognarde premium


class TB_BaconShop_HP_105t(Minion):
    # Poisson
    # le dbfId 78747 match pour le poisson premium (et non Carpe) néanmoins IG
    # le minion s'appelle bien Poisson de N'Zoth, soit le dbfId originel 67213
    # TODO: à surveiller
    nb_strike = 1

    @repeat_effect
    def die_off(self, sequence: Sequence):
        source = sequence.source
        if source.DEATHRATTLE and sequence.is_ally(self):
            for entity in [source] + source.entities:
                if hasattr(entity, 'deathrattle'):
                    self.buff(self, -105, deathrattle_met=entity.deathrattle)

TB_BaconShop_HP_105t_SKIN_A= TB_BaconShop_HP_105t # Carpe de NZoth


class TB_BaconUps_307(TB_BaconShop_HP_105t):
    # Poisson premium
    nb_strike = 2


class BGS_035(Minion):
    # Trotte-bougie
    def die_off(self, sequence: Sequence):
        if sequence.source.race.DRAGON and not sequence.is_ally(self):
            self.buff(self)
TB_BaconUps_105= BGS_035 # Trotte-bougie premium


### BATTLECRY ###

class BGS_116(Minion):
    # Anomalie actualisante
    bonus_value = 1
    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.buff(
            self.controller,
            remain_use=self.bonus_value)


class TB_BaconUps_167(BGS_116):
    # Anomalie actualisante premium
    bonus_value = 2


class BGS_069(battlecry_buff_myself):
    # Amalgadon
    @property
    def nb_strike(self) -> int:
        return len(self.my_zone.cards.exclude(self).one_minion_by_race())

    @property
    def enchantmentDbfId(self) -> Card_data:
        return self.all_cards[random.choice(ADAPT_ENCHANTMENT)]

    @enchantmentDbfId.setter
    def enchantmentDbfId(self, value) -> None:
        self._enchantmentDbfId = value


class TB_BaconUps_121(BGS_069):
    # Amalgadon premium
    @property
    def nb_strike(self) -> int:
        return super().nb_strike*2


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


class BGS_123(Minion):
    # Tempête de la taverne
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.controller.draw(
            self.discover(
                self.controller.deck.filter(race='ELEMENTAL'),
                nb=1)
        )


class TB_BaconUps_162(BGS_123):
    # Tempête de la taverne premium
    nb_strike = 2


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


class BGS_048(battlecry_select_one_minion_and_buff_it):
    # Gaillarde des mers du Sud
    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.buff(sequence.target)

    @property
    def nb_strike(self) -> int:
        return len(self.controller.bought_minions[self.nb_turn].filter(race='PIRATE')) +1
TB_BaconUps_140= BGS_048 # Gaillarde des mers du Sud premium


class ICC_807(Minion):
    # Pillard dure-écaille

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        for minion in self.my_zone.cards.filter(TAUNT=True):
            self.buff(minion)
TB_BaconUps_072= ICC_807 # Pillard dure-écaille premium


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
CFM_315= EX1_506 # chat de gouttière
TB_BaconUps_093= CFM_315 # chat de gouttière premium


class BGS_061(deathrattle_repop):
    # Forban
    pass
TB_BaconUps_141= BGS_061 # Forban premium
KAR_005= BGS_061 # Gentille grand-mère
TB_BaconUps_004= BGS_061 # Gentille grand-mère premium
EX1_556= BGS_061 # Golem des moissons
TB_BaconUps_006= BGS_061 # Golem des moissons premium
BGS_014= BGS_061 # Emprisonneur
TB_BaconUps_113= BGS_061 # Emprisonneur premium
BOT_537= BGS_061 # Mecanoeuf
TB_BaconUps_038e= BGS_061 # Mecanoeuf premium


class BGS_055(Minion):
    # Mousse du pont
    bonus_value = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.controller.levelup_cost_mod -= self.bonus_value


class TB_BaconUps_126(BGS_055):
    # Mousse du pont premium
    bonus_value = 2


class EX1_093(Minion):
    # Défenseur d'Argus

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        for minion in self.adjacent_neighbors():
            self.buff(minion)
TB_BaconUps_009= EX1_093 # Défenseur d'Argus premium


class LOOT_013(Minion):
    # Homoncule_sans_gene

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.damage(self.controller, 2)
TB_BaconUps_148= LOOT_013 # Homoncule_sans_gene premium


class UNG_073(battlecry_select_one_minion_and_buff_it):
    # Chasseur rochecave
    pass
TB_BaconUps_061= UNG_073 # Chasseur rochecave premium
GVG_055= UNG_073 # Cliqueteur percevrille
TB_BaconUps_069= UNG_073 # Cliqueteur percevrille premium
CFM_816= UNG_073 # Sensei virmen
TB_BaconUps_074= UNG_073 # Sensei virmen premium
DAL_077= UNG_073 # Aileron toxique
TB_BaconUps_152= UNG_073 # Aileron toxique premium
BGS_038= UNG_073 # Emissaire du crépuscule
TB_BaconUps_108= UNG_073 # Emissaire du crépuscule premium
DS1_070= UNG_073 # Maître-chien
TB_BaconUps_068= UNG_073 # Maître-chien premium
BGS_001= UNG_073 # Surveillant Nathrezim
TB_BaconUps_062=UNG_073 # Surveillant Nathrezim premium


class GVG_048(battlecry_select_all_and_buff_them):
    # Bondisseur dent de métal
    pass
TB_BaconUps_066= GVG_048 # Bondisseur dent de métal premium
BT_010= GVG_048 # Navigateur gangraileron
TB_BaconUps_124= GVG_048 # Navigateur gangraileron premium
CFM_610= GVG_048 # Tisse-cristal
TB_BaconUps_070= GVG_048 # Tisse-cristal premium
BGS_128= GVG_048 # Assistant arcanique
TB_Baconups_203= GVG_048 # Assistant arcanique premium
BGS_053= GVG_048 # Canonnier de la voile sanglante
TB_BaconUps_138= GVG_048 # Canonnier de la voile sanglante premium
EX1_103= GVG_048 # Voyant froide lumière
TB_BaconUps_064= GVG_048 # Voyant froide lumière premium



class BGS_082(Minion):
    # Tasse de la ménagerie

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        minions = self.my_zone.cards.one_minion_by_race().shuffle()
        for minion in minions[:3]:
            self.buff(minion)
TB_BaconUps_144= BGS_082 # Tasse de la ménagerie premium
BGS_083= BGS_082 # Théière de la ménagerie
TB_BaconUps_145= BGS_082 # Théière de la ménagerie premium


class BGS_122(Minion):
    # Elementaire de stase
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        minion_dbfId = self.discover(
            self.controller.deck.filter(race='ELEMENTAL'),
            nb=1)
        try:
            minion_id = self.controller.bob.board.create_card_in(minion_dbfId)
        except BoardAppendError:
            pass
        else:
            minion_id.FREEZE = True


class TB_BaconUps_161(BGS_122):
    # Elementaire de stase premium
    nb_strike = 2


##### DEATHRATTLE #####

class BGS_040(Minion):
    # Nadina
    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        for minion in self.my_zone.cards.filter(race='DRAGON'):
            minion.DIVINE_SHIELD = True
TB_BaconUps_154= BGS_040 # Nadina premium


class BGS_018(Minion):
    # Goldrinn
    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        for minion in self.my_zone.cards.filter(race='BEAST'):
            self.buff(minion)


class TB_BaconUps_085(BGS_018):
    # Goldrinn premium
    pass


class BGS_121(deathrattle_repop):
    # Gentil djinn
    nb_repop = 1
    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        super().deathrattle(sequence)
        for repop in sequence._repops:
            # les cartes sont-elles retirées de la main de bob ?
            self.controller.draw(repop.dbfId)

    @property
    def repopDbfId(self) -> int:
        """
        donne-t-il un elem au hasard de la taverne ou une carte elem choisie au
        hasard parmi toutes les possibilités ?
        maj 18.6 : summon que des serviteurs d'un niveau inférieur ou égal à celui de la taverne
        TODO: Gentle Djinni firstly summons an elemental, and only then puts a copy of it in hand. Therefore, if Djinni's deathrattle triggers more than once, but there is not enough space on board to summon another minion, the player will not receive a second and subsequent copy of elemental.
        : le gain ne se fait que si le repop à lieu
        """
        return random.choice(self.controller.deck.filter(race='ELEMENTAL').exclude(self.dbfId)).dbfId

class TB_BaconUps_165(BGS_121):
    # Gentil djinn premium
    nb_repop = 2


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


class BGS_079(deathrattle_repop):
    # Tranche-les-vagues
    nb_repop = 3

    @property
    def repopDbfId(self) -> int:
        return self.game.minion_can_collect.filter(race='PIRATE').exlude(self.dbfId).random_choice()


class TB_BaconUps_137(BGS_079):
    # Tranche-les-vagues premium
    nb_repop = 6


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


class BGS_126(Minion):
    # Elémentaire du feu de brousse
    def combat_end(self, sequence: Sequence):
        target = sequence.target
        damage_left = -target.health
        new_target = target.adjacent_neighbors().random_choice()
        if new_target and damage_left > 0:
            self.damage(new_target, damage_left)


class TB_BaconUps_166(Minion):
    # Elémentaire du feu de brousse premium
    def combat_end(self, sequence: Sequence):
        target = sequence.target
        damage_left = -target.health
        if damage_left > 0:
            for target in target.adjacent_neighbors():
                self.damage(target, damage_left)


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


class BRM_006(hit_by_repop):
    # Chef du gang des diablotins
    pass
TB_BaconUps_030= BRM_006 # Chef du gang des diablotins premium
BOT_218= BRM_006 # Rover de sécurité
TB_BaconUps_041= BRM_006 # Rover de sécurité premium


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


class OG_256(Minion):
    # Rejeton de N'Zoth
    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        for minion in self.controller.board.cards:
            self.buff(minion)
TB_BaconUps_025= OG_256


class CFM_316(deathrattle_repop):
    # Clan des rats
    @property
    def nb_repop(self):
        return min(self.attack, BOARD_SIZE)
TB_BaconUps_027= CFM_316


class OG_216(deathrattle_repop):
    # Loup contaminé
    nb_repop = 2
TB_BaconUps_026= OG_216 # Loup contaminé premium


class EX1_534(deathrattle_repop):
    # Crinière des savanes
    nb_repop = 2
TB_BaconUps_049= EX1_534 # Crinière des savanes premium


class DMF_533(deathrattle_repop):
    # Matrone de la piste
    nb_repop = 2
TB_BaconUps_309= DMF_533 # Matrone de la piste premium


class UNG_999t2e(deathrattle_repop):
    # Spores vivantes
    nb_repop = 2


class LOOT_368(deathrattle_repop):
    # Seigneur du vide
    nb_repop = 3
TB_BaconUps_059= LOOT_368 # Seigneur du vide premium


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


class OG_221(Minion):
    # Héroïne altruiste
    nb_strike = 1

    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        minion = self.controller.board.cards.exclude(DIVINE_SHIELD=True, is_alive=False).random_choice()
        if minion:
            minion.DIVINE_SHIELD = True


class TB_BaconUps_014(OG_221):
    # Héroïne altruiste premium
    nb_strike = 2


class BGS_202(Minion):
    # Mythrax
    def turn_off(self, sequence: Sequence):
        nb = len(self.my_zone.cards.one_minion_by_race())
        for _ in range(nb):
            self.buff(self)
TB_BaconUps_258= BGS_202 # Mythrax premium


class FP1_024(Minion):
    # Goule instable
    nb_strike = 1

    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        for minion in self.controller.field.cards:
            self.damage(minion, 1, overkill=False)


class TB_BaconUps_118(FP1_024):
    # Goule instable premium
    nb_strike = 2


class BG20_101(Minion):
    # Chauffard huran
    nb_strike = 1

    @repeat_effect
    def frenzy(self, sequence: Sequence):
        self.controller.draw(CardName.BLOOD_GEM)


class BG20_101_G(BG20_101):
    # Chauffard huran premium
    nb_strike = 2


class BG20_102(Minion):
    # Défense robuste
    def enhance_off(self, sequence: Sequence):
        if sequence.target is self and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT:
            self.buff(self)
BG20_102_G= BG20_102 # Défense robuste premium


class BG20_103(Minion):
    # Brute dos-hirsute
    bonus_value = 3

    def enhance_on(self, sequence: Sequence):
        if sequence.target is self and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT and\
                self.TRIGGER_VISUAL:
            sequence.source.attack += self.bonus_value
            sequence.source.max_health += self.bonus_value
            self.TRIGGER_VISUAL = False


class BG20_103_G(BG20_103):
    # Brute dos-hirsute premium
    bonus_value = 6


class BG20_105(Minion):
    # Mande-épines
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.controller.draw(CardName.BLOOD_GEM)
    deathrattle = battlecry


class BG20_105_G(BG20_105):
    # Mande-épines premium
    nb_strike = 2


class BG20_202(Minion):
    # Nécrolyte
    def play_start(self, sequence: Sequence):
        super().play_start(sequence)
        if sequence.is_valid:
            sequence.add_target(
                self.controller.board.cards.choice(self.controller)
            )

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.buff(sequence.target)
        self.buff(sequence.target)
        for neighbour in sequence.target.adjacent_neighbors():
            change = False
            for enchantment in neighbour.entities[::-1]:
                if enchantment.dbfId == CardName.BLOOD_GEM_ENCHANTMENT:
                    enchantment.apply(sequence.target)
                    change = True
            if change:
                neighbour.calc_stat_from_scratch()
        sequence.target.calc_stat_from_scratch()
BG20_202_G= BG20_202 # Nécrolyte premium


class BG20_201(Minion):
    # Porte-bannière huran
    nb_strike = 1

    @repeat_effect
    def turn_off(self, sequence: Sequence):
        for neighbour in self.adjacent_neighbors().filter(race='QUILBOAR'):
            self.buff(neighbour)


class BG20_201_G(BG20_201):
    # Porte-bannière huran premium
    nb_strike = 2


class BG20_104(Minion):
    # Cogneur
    def combat_end(self, sequence: Sequence):
        self.controller.draw(CardName.BLOOD_GEM)
BG20_104_G= BG20_104 # Cogneur premium


class BG20_207(Minion):
    # Duo dynamique
    def enhance_off(self, sequence: Sequence):
        target = sequence.target
        if self.controller is target.controller and\
                target.race.QUILBOAR and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT and\
                self is not sequence.target:
            self.buff(self)
BG20_207_G= BG20_207 # Duo dynamique premium


class BG20_106(Minion):
    bonus_value = 2
    # Tremble-terre
    def enhance_off(self, sequence: Sequence):
        if sequence.target is self and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT:
            for minion in self.my_zone.cards.exlude(self):
                self.buff(minion, attack=self.bonus_value)


class BG20_106_G(BG20_106):
    # Tremble-terre premium
    bonus_value = 4


class BG20_204(Minion):
    # Chevalier dos-hirsute
    def frenzy(self, sequence: Sequence):
        self.DIVINE_SHIELD = True

BG20_204_G= BG20_204


class BG20_302(Minion):
    # Aggem malépine
    def enhance_off(self, sequence: Sequence):
        if sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT and\
                self is sequence.target:
            for minion in self.my_zone.cards.one_minion_by_race():
                self.buff(minion)
BG20_302_G= BG20_302 # Aggem malépine premium


class BG20_205(Minion):
    # Agamaggan
    bonus_value = 1
    def enhance_on(self, sequence: Sequence):
        if sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT and\
                sequence.is_ally(self):
            sequence.source.attack += self.bonus_value
            sequence.source.max_health += self.bonus_value

class BG20_205_G(Minion):
    # Agamaggan premium
    bonus_value = 2


class BG20_303(Minion):
    # Charlga
    nb_strike = 1

    @repeat_effect
    def turn_off(self):
        for minion in self.my_zone.cards:
            self.buff(minion)


class BG20_303_G(BG20_303):
    # Charlga premium
    nb_strike = 2


class BG20_206(Minion):
    # Capitaine Plate-Défense
    #TODO: sequence + optimisation
    mod_quest_value = 4
    def unknown(self, sequence: Sequence):
        for _ in range(sequence.gold_spend):
            self.quest_value += 1
            if self.quest_value % self.mod_quest_value == 0:
                self.controller.draw(CardName.BLOOD_GEM)


class BG20_206_G(BG20_206):
    # Capitaine Plate-Défense premium
    nb_strike = 2

    @repeat_effect
    def unknown(self, sequence: Sequence):
        for _ in range(sequence.gold_spend):
            self.quest_value += 1
            if self.quest_value % self.mod_quest_value == 0:
                self.controller.draw(CardName.BLOOD_GEM)
                self.controller.draw(CardName.BLOOD_GEM)


class BG20_203(Minion):
    # Prophète du sanglier
    def play_off(self, sequence: Sequence):
        if sequence.source.race.QUILBOAR and\
                sequence.is_ally(self) and\
                self.TRIGGER_VISUAL:
            self.controller.draw(CardName.BLOOD_GEM)
            self.TRIGGER_VISUAL = False


class BG20_203_G(BG20_203):
    # Prophète du sanglier premium
    def play_off(self, sequence: Sequence):
        if sequence.source.race.QUILBOAR and\
                sequence.is_ally(self) and\
                self.TRIGGER_VISUAL:
            self.controller.draw(CardName.BLOOD_GEM)
            self.controller.draw(CardName.BLOOD_GEM)
            self.TRIGGER_VISUAL = False


class BG20_304(Minion):
    # Archidruide Hamuul
    #TODO
    #note: c'est considéré une actualisation : le pouvoir de Ysera s'active
    @repeat_effect
    def battlecry(self, sequence: Sequence):
        pass
BG20_304_G= BG20_304


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


class BGS_060(Minion):
    # Yo oh ogre
    def combat_off(self, sequence: Sequence):
        if self is sequence.target:
            self.combat()
TB_BaconUps_150= BGS_060 # Yo oh ogre premium


BGS_039= minion_without_script # Lieutenant draconide
TB_BaconUps_146= minion_without_script # Lieutenant draconide premium
BGS_106= minion_without_script # Acolyte de C'Thun
TB_BaconUps_255= minion_without_script # Acolyte de C'Thun premium
VAN_EX1_506a= minion_without_script # éclaireur murloc
TB_BaconUps_003t= minion_without_script # éclaireur murloc premium
CFM_315t= minion_without_script # chat tigré
TB_BaconUps_093t= minion_without_script # chat tigré premium


class BGS_061t(Minion):
    # pirate du ciel
    def summon_end(self, sequence: Sequence):
        self.combat()
TB_BaconUps_141t= BGS_061t # pirate du ciel premium


class BGS_115t(Minion):
    # Goutte d'eau
    pass

class TB_BaconShop_HP_033t(Minion):
    # Amalgame
    pass

class EX1_170(Minion):
    # Cobra empereur
    pass

class EX1_554t(Minion):
    # Serpent
    pass

class KAR_005a(Minion):
    # Grand méchant loup
    pass

class TB_BaconUps_004t(Minion):
    # Grand méchant loup premium
    pass

class skele21(Minion):
    # Golem endommagé
    pass

class TB_BaconUps_006t(Minion):
    # Golem endommagé premium
    pass


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


class BRM_006t(Minion):
    # Diablotin
    pass

class TB_BaconUps_030t(Minion):
    # Diablotin premium
    pass

class CFM_316t(Minion):
    # Rat
    pass

class TB_BaconUps_027t(Minion):
    # Rat premium
    pass

class OG_216a(Minion):
    # Araignée
    pass

class TB_BaconUps_026t(Minion):
    # Araignée premium
    pass

class BOT_312t(Minion):
    # Microbot
    pass

class TB_BaconUps_032t(Minion):
    # Microbot premium
    pass

class BGS_119(Minion):
    # Cyclone crépitant
    pass

class TB_BaconUps_159(Minion):
    # Cyclone crépitant premium
    pass

class BGS_034(Minion):
    # Gardien de bronze
    pass

class TB_BaconUps_149(Minion):
    # Gardien de bronze premium
    pass

class BOT_911(Minion):
    # Ennuy-o-module
    pass

class TB_BaconUps_099(Minion):
    # Ennuy-o-module premium
    pass


class EX1_534t(Minion):
    # Hyène
    pass


class TB_BaconUps_049t(Minion):
    # Hyène premium
    pass


class LOOT_078(Minion):
    # Hydre des cavernes
    pass

class TB_BaconUps_151(LOOT_078):
    # Hydre des cavernes
    pass


class BOT_537t(Minion):
    # Robosaure
    pass

class TB_BaconUps_039t(Minion):
    # Robosaure premium
    pass

class BOT_218t(Minion):
    # Robot gardien
    pass

class TB_BaconUps_041t(Minion):
    # Robot gardien premium
    pass

class DMF_533t(Minion):
    # Diablotin embrasé
    pass

class TB_BaconUps_309t(Minion):
    # Diablotin embrasé premium
    pass

class TRL_232t(Minion):
    # Rejeton cuiracier
    pass

class TB_BaconUps_051t(Minion):
    # Rejeton cuiracier premium
    pass

class CS2_065(Minion):
    # Marcheur du vide
    pass

class TB_BaconUps_059t(Minion):
    # Marcheur du vide premium
    pass

class BGS_131(Minion):
    # Spore mortelle
    pass

class TB_BaconUps_251(Minion):
    # Spore mortelle premium
    pass

class GVG_113(Minion):
    # Faucheur 4000
    pass

class TB_BaconUps_153(Minion):
    # Faucheur 4000 premium
    pass

class FP1_010(Minion):
    # Maexxna
    pass

class TB_BaconUps_155(Minion):
    # Maexxna premium
    pass

class UNG_999t2t1(Minion):
    # Plante
    pass


class BGS_022(Minion):
    # Zapp Mèche-sournoise
    def search_fight_target(self):
        opponent_board = self.my_zone.opponent.cards.\
            exclude(is_alive=False, DORMANT=True)

        if not opponent_board:
            return None

        sorted_board = sorted(opponent_board, key=lambda x: x.attack)
        for nb, card in enumerate(sorted_board):
            if card.attack != sorted_board[0].attack:
                break

        return random.choice(sorted_board[:nb])


class TB_BaconUps_091(BGS_022):
    # Zapp Mèche-sournoise premium
    pass


class BG21_022(Minion):
    # Robo-toutou
    pass


class BG21_022_G(Minion):
    # Robo-toutou premium
    pass


class BG21_008(Minion):
    # Boss écailles-salines
    def play_off(self, sequence: Sequence):
        if sequence.source.race.MURLOC and sequence.is_ally(self):
            targets = self.my_zone.cards.filter(race='MURLOC').exclude(self).shuffle()
            for target in targets[:2]:
                self.buff(target)
BG21_008_G= BG21_008 # Boss écailles-salines premium


class BG19_010(deathrattle_repop):
    # Rat d'égout
    pass
BG19_010_G= BG19_010 # Rat d'égout premium


class BG19_010t(Minion):
    # Demi-carapace
    pass


class BG19_010_Gt(Minion):
    # Demi-carapace premium
    pass


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


class BG21_000(Minion):
    # Saute-mouton
    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        target = self.controller.board.cards.filter(race='BEAST', is_alive=True).random_choice()
        self.buff(
            target
        )
BG21_000_G= BG21_000 # Saute-mouton premium


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


class BG21_021(battlecry_select_one_minion_and_buff_it):
    # Enfumeur
    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.buff(
            sequence.target,
            attack=self.bonus_value,
            max_health=self.bonus_value
        )

    @property
    def bonus_value(self) -> int:
        return self.controller.level


class BG21_021_G(BG21_021):
    # Enfumeur premium
    @property
    def bonus_value(self) -> int:
        return self.controller.level*2


class BG21_037(Minion):
    # Fendeur de gemmes
    nb_strike = 1

    @repeat_effect
    def loss_shield_off(self, sequence: Sequence):
        if sequence.is_ally(self):
            self.controller.draw(CardName.BLOOD_GEM)


class BG21_037_G(BG21_037):
    # Fendeur de gemmes premium
    # TODO: une fois doré, les gemmes sont dorées également (même effet, juste visuel ?)
    nb_strike = 2


class BG21_010(battlecry_buff_myself):
    # Gonflalairon
    @property
    def nb_strike(self):
        return len(self.owner.cards.filter(race='MURLOC').exclude(self))


class BG21_010_G(BG21_010):
    # Gonflalairon premium
    pass


class BG21_039(aura_buff_race):
    # Kathra’natir
    def summon_start(self, sequence: Sequence):
        super().summon_start(sequence)
        if sequence.is_valid:
            self.buff(self.controller, -76567)
BG21_039_G= BG21_039 # Kathra’natir premium


class BG21_030(Minion):
    # Mainverte en herbe
    def avenge(self, sequence: Sequence):
        for minion in self.adjacent_neighbors():
            self.buff(minion)


class BG21_030_G(BG21_030):
    # Mainverte en herbe premium
    pass


class BG21_002(Minion):
    # Pote à plumes
    def avenge(self, sequence: Sequence):
        for minion in self.owner.cards.filter(race='BEAST'):
            self.buff(minion)


class BG21_002_G(BG21_002):
    # Pote à plumes premium
    pass


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


class BG21_024(Minion):
    # Graiss-o-bot
    def loss_shield_off(self, sequence: Sequence):
        if sequence.source.my_zone is self.my_zone:
            self.buff(sequence.source)


class BG21_024(BG21_024):
    # Graiss-o-bot premium
    pass


class BG21_038(Minion):
    # Matrone ensorçaile
    nb_strike = 1

    @repeat_effect
    def avenge(self, sequence: Sequence):
        # TODO: à tester, probablement non fonctionnel
        self.controller.draw(
            self.controller.deck.filter(BATTLECRY=True).random_choice()
        )


class BG21_038_G(BG21_038):
    # Matrone ensorçaile premium
    nb_strike = 2


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


class BG21_016(Minion):
    # Peggy les Os-de-verre
    def add_card_on_hand_off(self, sequence: Sequence):
        if sequence.is_ally(self):
            pirates = self.my_zone.cards.filter(race='PIRATE').exclude(self)
            if pirates:
                self.buff(random.choice(pirates))


class BG21_016_G(BG21_016):
    # Peggy les Os-de-verre premium
    pass


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


class BG21_020(Minion):
    # Rejeton de Lumière éclatant
    bonus_value = 1
    #TODO: activer le bonus
    def avenge(self, sequence: Sequence):
        self.buff(
            self.controller,
            bonus_value=self.bonus_value)


class BG21_020_G(BG21_020):
    # Rejeton de Lumière éclatant premium
    bonus_value = 2


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


class BG21_040(Minion):
    # Âme en peine recycleuse
    bonus_value = 1
    def play_off(self, sequence: Sequence):
        if sequence.is_ally(self) and sequence.source.race.ELEMENTAL:
            self.buff(
                self.controller,
                remain_use=self.bonus_value)


class BG21_040_G(BG21_040):
    # Âme en peine recycleuse premium
    bonus_value = 2


class BG21_001(Minion):
    # Crocilisque claires-écailles
    def avenge(self, sequence: Sequence):
        self.buff(
            self.my_zone.cards.filter(race='BEAST').exclude(self).random_choice()
        )
    deathrattle = avenge


class BG21_001(BG21_001):
    # Crocilisque claires-écailles premium
    pass


class BG21_003(battlecry_select_one_minion_and_buff_it):
    # Crotale résurrecteur
    pass


class BG21_003_G(BG21_003):
    # Crotale résurrecteur premium
    pass


class BG21_036(Minion):
    # Maître des réalités
    def enhance_on(self, sequence: Sequence):
        if sequence.source.my_zone is self.my_zone and\
                sequence.source.race.ELEMENTAL and\
                (getattr(sequence.source, 'attack', 0) > 0 or\
                getattr(sequence.source, 'max_health', 0) > 0):
            sequence(self.buff, self.enchantmentDbfId, self)


class BG21_036(BG21_036):
    # Maître des réalités premium
    pass


class BG20_401(Minion):
    # Mécareau divin
    def loss_shield_off(self, sequence: Sequence):
        if sequence.is_ally(self):
            self.DIVINE_SHIELD = True


class BG20_401_G(BG20_401):
    # Mécareau divin premium
    pass


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


class BG21_011(Minion):
    # Lanceur de crustacés
    def play_start(self, sequence: Sequence):
        super().play_start(sequence)
        if sequence.is_valid:
            sequence.add_target(
                self.controller.field.cards.filter_hex(race=self.synergy).\
                    exclude(is_premium=True).choice(self.controller)
            )

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        target = sequence.target
        if target:
            pass
            # TODO
BG21_011_G= BG21_011 # Lanceur de crustacés premium


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


class TB_BaconShop_HP_022t(Minion):
    # Carnipousse
    # Le second Carnipousse ne lance pas le cri de guerre du premier
    nb_strike = 1
    def play_start(self, sequence: Sequence):
        pass

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        for cards in self.controller.played_cards.values():
            for card in cards.exclude(dbfId=self.dbfId):
                if getattr(card, 'battlecry', False):
                    card_id = self.create_card(card.dbfId)
                    card_id.owner = self.owner
                    # start sequence ??
                    #card_id.battlecry()


class TB_BaconShop_HP_022t_G(TB_BaconShop_HP_022t):
    nb_strike = 2