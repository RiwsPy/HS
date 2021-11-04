# coding : utf-8

import random
from enums import FIELD_SIZE, CardName, Type, Zone, Race
from utils import *
from action import *
from entity import Entity, Minion
from sequence import Sequence

class battlecry_select_one_minion_and_buff_it(Minion):
    # buff battlecry, only minions of the same synergy can be targeted
    def play_start(self, sequence: Sequence):
        super().play_start(sequence)
        if sequence.is_valid:
            minion = self.choose_one_of_them(
                self.controller.board.cards.filter(race=self.synergy))
            sequence.add_target(minion)

    def battlecry(self, sequence: Sequence):
        for minion in sequence.targets:
            self.buff(self.enchantment_dbfId, minion)


class deathrattle_repop(Minion):
    nb_repop = 1
    def deathrattle(self, sequence):
        repop_id = self.invoc(sequence, self.repop_dbfId)
        if repop_id:
            sequence._repops.append(repop_id)


class hit_by_repop(Minion):
    nb_repop = 1
    def hit(self, sequence):
        if self is sequence.target and sequence.damage_value > 0:
            deathrattle_repop.deathrattle(self, sequence)


class battlecry_select_all_and_buff_them(Minion):
    nb_strike = 1
    def battlecry(self, sequence):
        minions = self.controller.board.cards.filter(race=self.synergy).exclude(self)
        self.buff(self.enchantment_dbfId, *minions)


class aura_buff_race(Minion):
    def summon_on(self, sequence):
        if sequence.source.controller is self.controller and\
                sequence.source.race == self.race:
            self.buff(self.enchantment_dbfId, sequence.source)

    def summon_start(self, sequence):
        super().summon_start(sequence)
        if sequence.is_valid:
            for minion in self.controller.board.cards:
                if minion.race == self.race:
                    self.buff(self.enchantment_dbfId, minion)


class battlecry_buff_myself(Minion):
    nb_strike = 1
    def battlecry(self, sequence):
        self.buff(self.enchantment_dbfId, self)


class BGS_043(Minion):
    # Murozond
    nb_strike = 1
    def battlecry(self, sequence):
        pass
"""
    board_adv = self.owner.owner.last_opponent.real_board
    if board_adv and not self.owner.owner.hand.is_full:
        card_key_number = random.choice(board_adv).dbfId
        if card_key_number[-2:] == '_p':
            card_key_number = card_key_number[:-2]
        for card in self.bob.hand:
            if card.dbfId == card_key_number:
                self.owner.owner.hand.append(card)
                return card
        return self.owner.owner.hand.create_card_in(card_key_number)
    return None

def Murozond_p(self):
    board_adv = [crd
        for crd in self.owner.owner.last_opponent.real_board
            if crd.dbfId != '513_p']

    if board_adv and not self.owner.owner.hand.is_full:
        card_key_number = random.choice(board_adv).dbfId
        if card_key_number[-2:] != '_p':
            if card_key_number + '_p' in card.card_db():
                card_key_number = card_key_number + '_p'
        card = self.owner.owner.hand.create_card_in(card_key_number)
        if card_key_number[-2:] == '_p':
            card_key_number = card_key_number[:-2]

        card_from_bob = []
        for minion in self.bob.hand: # retrait des 3 cartes de la main de bob, sûr ?
            if minion.dbfId == card_key_number:
                self.owner.owner.hand.remove(minion)
                card_from_bob.append(minion)
                if len(card_from_bob) > 2:
                    break
        card.card_in = card_from_bob
        return card
    return None
"""


class MTB_BaconUps_110(BGS_043):
    # Murozond premium
    nb_strike = 2


class BGS_113(Minion):
    # Habitue_sans_visage
    def battlecry(self, sequence):
        # comment se passe la gestion lors de la revente, la copie est enlevée de la taverne ou est-ce 
        # l'habitué ?
        pass
TB_BaconUps_305= BGS_113 # Habitue_sans_visage premium


class BGS_104(Minion):
    # Nomi
    #TODO: à compléter, n'affecte pas les serviteurs déjà présents dans la taverne
    bonus_value = 1
    def play_off(self, sequence):
        # s'active après le battlecry de l'élémentaire de stase
        source = sequence.source
        if self.controller is source.controller and source.race.ELEMENTAL:
            self.buff(self.enchantment_dbfId,
                self.controller,
                bonus_value=self.__class__.bonus_value)


class TB_BaconUps_201(BGS_104):
    # Nomi premium
    bonus_value = 2


class BGS_036(Minion):
    # Tranchetripe
    def turn_off(self, sequence):
        self.buff(self.enchantment_dbfId, self,
            max_health=self.bonus_value,
            attack=self.bonus_value)

    @property
    def bonus_value(self) -> int:
        return len(self.my_zone.cards.filter(race='DRAGON'))


class TB_BaconUps_106(Minion):
    # Tranchetripe premium
    @property
    def bonus_value(self) -> int:
        return len(self.my_zone.cards.filter(race='DRAGON'))*2


class BGS_072(Minion):
    # Captaine_Larrrrdeur
    bonus_value = 1

    def buy_off(self, source):
        if source.race.PIRATE:
            self.controller.gold += self.__class__.bonus_value


class TB_BaconUps_133(BGS_072):
    # Captaine_Larrrrdeur premium
    bonus_value = 2


class BGS_059(battlecry_select_one_minion_and_buff_it):
    # Dévoreur d'âmes
    def battlecry(self, sequence):
        for minion in sequence.targets:
            if minion.my_zone is self.my_zone:
                self.controller.bob.hand.append(minion)
                self.controller.gold += 3
                self.buff(self.enchantment_dbfId, self, attack=minion.attack, max_health=minion.health)


class TB_BaconUps_119(BGS_059):
    # Dévoreur d'âmes premium
    def battlecry(self, sequence):
        for minion in sequence.targets:
            if minion.my_zone is self.my_zone:
                self.controller.bob.hand.append(minion)
                self.controller.gold += 6
                self.buff(self.enchantment_dbfId, self, attack=minion.attack*2, max_health=minion.health*2)


class BGS_012(Minion):
    # Apprentie de Kangor
    nb_repop = 2
    def deathrattle(self, sequence):
        for repop in self.controller.graveyard.entities.filter(race='MECHANICAL')[:self.__class__.nb_repop]:
            self.invoc(sequence, repop.dbfId)


class TB_BaconUps_087(BGS_012):
    # Apprentie de Kangor premium
    nb_repop = 4


class GVG_021(aura_buff_race):
    # Mal'Ganis
    def summon_start(self, sequence):
        super().summon_start(sequence)
        if sequence.is_valid:
            self.buff(-2203, self.controller)

TB_BaconUps_060= GVG_021 # Mal'Ganis premium
EX1_185= aura_buff_race # Brise-siège
TB_BaconUps_053= EX1_185 # Brise-siège premium
EX1_507= aura_buff_race # Chef de guerre murloc
TB_BaconUps_008= EX1_507 # Chef de guerre murloc premium
NEW1_027= aura_buff_race # Capitaine des mers du Sud
TB_BaconUps_136= NEW1_027 # Capitaine des mers du Sud premium


class BGS_111(Minion):
    # Champion d'Yshaarj
    def combat_on(self, sequence):
        for defenser in sequence.targets:
            if defenser.TAUNT and defenser.controller is self.controller:
                self.buff(self.enchantment_dbfId, self)
TB_BaconUps_301= BGS_111 # Champion d'Yshaarj premium


class BGS_110(Minion):
    # Bras de l'empire
    def combat_on(self, sequence):
        for defenser in sequence.targets:
            if defenser.TAUNT and defenser.controller is self.controller:
                self.buff(self.enchantment_dbfId, defenser)
TB_BaconUps_302= BGS_110 # Bras de l'empire premium


class BGS_047(Minion):
    # Amiral de l'effroi Eliza
    valid_for_myself = True
    def combat_on(self, sequence):
        source = sequence.source
        if source.race.PIRATE and source.controller is self.controller:
            for minion in self.my_zone.cards:
                self.buff(self.enchantment_dbfId, minion)
TB_BaconUps_134= BGS_047 # Amiral de l'effroi Eliza premium


class BGS_056(Minion):
    # Capitaine Grondéventre
    def combat_on(self, sequence):
        source = sequence.source
        if source.race.PIRATE and source.controller is self.controller:
            self.buff(self.enchantment_dbfId, source)
TB_BaconUps_139= BGS_056 # Capitaine Grondéventre premium


class LOE_077(Minion):
    # Brann
    #TODO: l'effet d'un Brann doré se cumule-t-il avec celui d'un Brann non doré ?
    # (parti du principe que non)
    # Même questionnement pour Baron Vaillefendre
    def battlecry_on(self, sequence):
        sequence.double_effect = True


class TB_BaconUps_045(LOE_077):
    # Brann premium
    def battlecry_on(self, sequence):
        sequence.triple_effect = True


class FP1_031(Minion):
    # Baron_Vaillefendre
    def deathrattle_on(self, sequence):
        sequence.double_effect = True


class TB_BaconUps_055(Minion):
    # Baron_Vaillefendre premium
    def deathrattle_on(self, sequence):
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
    def turn_off(self, sequence):
        for minion in self.my_zone.cards:
            if hasattr(minion, 'battlegroundsNormalDbfId'):
                self.buff(self.enchantment_dbfId, self)
TB_BaconUps_130= BGS_066 # Raflelor premium


class ULD_217(Minion):
    # Micromomie
    def turn_off(self, sequence):
        minions = self.owner.cards.exclude(self)
        if minions:
            self.buff(self.enchantment_dbfId, random.choice(minions))
TB_BaconUps_250= ULD_217 # Micromomie premium


class BGS_105(Minion):
    # Chambellan Executus
    def turn_off(self, sequence):
        target = self.my_zone[0]
        self.buff(self.enchantment_dbfId, target)
        for _ in self.controller.played_cards[self.nb_turn].filter(type='MINION', race='ELEMENTAL'):
            self.buff(self.enchantment_dbfId, target)


class TB_BaconUps_207(BGS_105):
    # Chambellan Executus premium
    pass


class ICC_029(Minion):
    # Plaiedécailles cobalt
    def turn_off(self, sequence):
        lst = self.my_zone.cards.exclude(self)
        if lst:
            self.buff(self.enchantment_dbfId, random.choice(lst))
TB_BaconUps_120= ICC_029 # Plaiedécailles cobalt premium


class BGS_009(Minion):
    # Massacreuse croc radieux
    def turn_off(self, sequence):
        for minion in self.my_zone.cards.one_minion_by_type():
            self.buff(self.enchantment_dbfId, minion)
TB_BaconUps_082= BGS_009  # Massacreuse croc radieux premium


class BGS_115(Minion):
    # Élémenplus
    def sell_end(self, sequence):
        self.controller.hand.create_card_in(64040)


class TB_BaconUps_156(Minion):
    # Élémenplus premium
    def sell_end(self, sequence):
        self.controller.hand.create_card_in(64040, 64040)


class BG20_301(Minion):
    # Bronze couenne
    nb_strike = 1
    def sell_end(self, sequence):
        self.controller.hand.create_card_in(
            CardName.BLOOD_GEM,
            CardName.BLOOD_GEM)


class BG20_301_G(BG20_301):
    # Bronze couenne premium
    nb_strike = 2


class BG20_100(Minion):
    # Géomancien de Tranchebauge
    nb_strike = 1
    def battlecry(self, sequence):
        self.controller.hand.create_card_in(CardName.BLOOD_GEM)


class BG20_100_G(BG20_100):
    # Géomancien de Tranchebauge premium
    nb_strike = 2


class BGS_037(Minion):
    # Régisseur du temps
    def sell_start(self, sequence):
        super().sell_start(sequence)
        if sequence.is_valid:
            sequence(self.buff, self.enchantment_dbfId, *self.my_zone.opponent.cards)
TB_BaconUps_107= BGS_037 # Régisseur du temps premium


class BGS_049(Minion):
    # Parieuse convaincante
    bonus_value = 3
    def sell_start(self, sequence):
        sequence.cost = self.__class__.bonus_value
        super().sell_start(sequence)


class TB_BaconUps_127(BGS_049):
    # Parieuse convaincante premium
    bonus_value = 6


class ICC_858(Minion):
    # Bolvar sang-de-feu
    valid_for_myself = True
    def loss_shield_off(self, sequence):
        if self.controller is sequence.source.controller:
            self.buff(self.enchantment_dbfId, self)
TB_BaconUps_047= ICC_858 # Bolvar sang-de-feu premium
BGS_067= ICC_858 # Massacreur drakonide
TB_BaconUps_117= BGS_067 # Massacreur drakonide premium


class BGS_004(Minion):
    # Tisse-colère
    def play_off(self, sequence: Sequence):
        if self.controller is sequence.source.controller and sequence.source.race.DEMON:
            self.controller.health -= 1
            self.buff(self.enchantment_dbfId, self)
TB_BaconUps_079= BGS_004 # Tisse-colère premium


class EX1_509(Minion):
    # Mande-flots murloc
    def summon_on(self, sequence):
        if sequence.source.race.MURLOC:
            self.buff(self.enchantment_dbfId, self)
TB_BaconUps_011= EX1_509 # Mande-flots murloc premium


class BGS_100(Minion):
    # Mini Rag
    nb_strike = 1
    def play_off(self, sequence):
        if sequence.source.race.ELEMENTAL:
            self.buff(self.enchantment_dbfId,
                random.choice(self.my_zone.cards),
                attack=sequence.source.level,
                max_health=sequence.source.level)


class TB_BaconUps_200(BGS_100):
    # Mini Rag premium
    nb_strike = 2


class BGS_081(Minion):
    # Pillard pirate
    def play_on(self, sequence):
        if sequence.source.race.PIRATE and self.controller is sequence.source.controller:
            self.buff(self.enchantment_dbfId, self)
TB_BaconUps_143= BGS_081 # Pillard pirate premium


class BGS_041(Minion):
    # Kalecgos
    def play_off(self, sequence):
        if sequence.source.BATTLECRY and self.controller is sequence.source.controller:
            for minion in self.my_zone.cards.filter(race='DRAGON'):
                self.buff(self.enchantment_dbfId, minion)
TB_BaconUps_109=BGS_041  # Kalecgos premium


class BGS_075(Minion):
    # Saurolisque enragé
    def play_off(self, sequence):
        if sequence.source.DEATHRATTLE and\
                sequence.source.controller is self.controller:
            self.buff(self.enchantment_dbfId, self)
TB_BaconUps_125= BGS_075 # Saurolisque enragé premium


class BGS_127(Minion):
    # Roche en fusion
    def play_off(self, sequence):
        if sequence.source.race.ELEMENTAL and\
                sequence.source.controller is self.controller:
            self.buff(self.enchantment_dbfId, self)
TB_Baconups_202= BGS_127 # Roche en fusion premium


class BGS_120(Minion):
    # Elémentaire de fête
    nb_strike = 1
    def play_off(self, sequence):
        if sequence.source.race.ELEMENTAL and\
                sequence.source.controller is self.controller:
            minions = self.my_zone.cards.filter(race='ELEMENTAL').exclude(self)
            if minions:
                self.buff(self.enchantment_dbfId, random.choice(minions))


class TB_BaconUps_160(Minion):
    # Elémentaire de fête premium
    nb_strike = 2


class BGS_204(Minion):
    # Démon démesuré
    def play_off(self, sequence):
        source = sequence.source
        if self.controller is source.controller and source.race.DEMON:
            self.buff(self.enchantment_dbfId, self)
TB_BaconUps_304= BGS_204 # Démon démesuré premium


class BGS_017(Minion):
    # Chef de meute
    def summon_off(self, sequence):
        source = sequence.source
        if source.controller is self.controller and source.race.BEAST:
            self.buff(self.enchantment_dbfId, source)
TB_BaconUps_086= BGS_017 # Chef de meute premium
BGS_021= BGS_017 # Maman ourse
TB_BaconUps_090= BGS_017 # Maman ourse premium


class BGS_045(Minion):
    # Gardien des glyphes
    def combat_start(self, sequence):
        super().combat_start(sequence)
        self.buff(self.enchantment_dbfId, self)
TB_BaconUps_115= BGS_045 # Gardien des glyphes premium

class BGS_019(Minion):
    # Dragonnet rouge
    nb_strike = 1
    def fight_on(self, sequence):
        nb_dragon_in_board = len(self.my_zone.cards.filter(race='DRAGON'))
        sequence(
            self.damage,
            random.choice(self.my_zone.opponent.cards),
            nb_dragon_in_board,
            overkill=False)


class TB_BaconUps_102(BGS_019):
    # Dragonnet rouge premium
    nb_strike = 2


class BGS_078(Minion):
    # Ara monstrueux
    nb_strike = 1
    def combat_end(self, sequence):
        minions_with_deathrattle = []
        for minion in self.my_zone.cards.filter(is_alive=True).exclude(self):
            if minion.DEATHRATTLE:
                minions_with_deathrattle.append(minion)
            else:
                for entity in minion:
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
    def summon_off(self, sequence):
        if self.in_fight_sequence and\
                sequence.source.race.MECHANICAL:
            self.buff(self.enchantment_dbfId, self)


class TB_BaconUps_123(BGS_071):
    # Déflect-o-bot premium
    pass


class BGS_002(Minion):
    # Jongleur d'âmes
    nb_strike = 1
    def die_off(self, sequence):
        if sequence.source.race.DEMON and sequence.source.controller is self.controller:
            sequence(
                self.damage,
                random.choice(self.my_zone.opponent.cards),
                3,
                overkill=False)


class TB_BaconUps_075(BGS_002):
    # Jongleur d'âmes premium
    nb_strike = 2


class EX1_531(Minion):
    # Hyène_charognarde
    # la hyène est buff après l'activation du râle
    def die_off(self, sequence):
        if sequence.source.controller is self.controller and sequence.source.race.BEAST:
            self.buff(self.enchantment_dbfId, self)
TB_BaconUps_043= EX1_531 # Hyène_charognarde premium


class GVG_106(Minion):
    # Brik-a-bot
    def die_off(self, sequence):
        if sequence.source.controller is self.controller and\
                sequence.source.race.MECHANICAL:
            self.buff(self.enchantment_dbfId, self)
TB_BaconUps_046= GVG_106 # Brik-a-bot premium


class TB_BaconShop_HP_105t(Minion):
    # Poisson
    def die_off(self, sequence):
        source = sequence.source
        if source.DEATHRATTLE and\
            source.my_zone is self.my_zone:

            self.buff(-105, self, method=source.id, mechanics=["DEATHRATTLE"])

class TB_BaconUps_307(Minion):
    # Poisson premium
    die_off= TB_BaconShop_HP_105t.die_off


class BGS_035(Minion):
    # Trotte-bougie
    def die_off(self, sequence):
        if sequence.source.race.DRAGON and sequence.source.controller is self.controller.opponent:
            self.buff(self.enchantment_dbfId, self)
TB_BaconUps_105= BGS_035 # Trotte-bougie premium


### BATTLECRY ###

class BGS_116(Minion):
    # Anomalie actualisante
    bonus_value = 1
    def battlecry(self, sequence):
        self.controller.roll_nb_free = self.__class__.bonus_value


class TB_BaconUps_167(BGS_116):
    # Anomalie actualisante premium
    bonus_value = 2


class BGS_069(Minion):
    # Amalgadon
    def battlecry(self, sequence):
        self.add_adapt()

    @property
    def nb_strike(self) -> int:
        return len(self.my_zone.cards.exclude(self).one_minion_by_type())


class TB_BaconUps_121(BGS_069):
    # Amalgadon premium
    @property
    def nb_strike(self) -> int:
        return super().nb_strike*2


class BGS_020(Minion):
    # Guetteur primaileron
    nb_strike = 1
    def battlecry(self, sequence):
        if self.my_zone.cards.filter(race='MURLOC').exclude(self):
            minion_id = self.discover(
                self.controller.bob.local_hand.filter(race='MURLOC'),
                nb=3)
            self.controller.hand.append(minion_id)


class TB_BaconUps_089(BGS_020):
    # Guetteur primaileron premium
    nb_strike = 2


class BGS_123(Minion):
    # Tempête de la taverne
    nb_strike = 1
    def battlecry(self):
        minion_id = self.discover(
            self.controller.bob.local_hand.filter(race='ELEMENTAL'),
            nb=1)
        self.controller.hand.append(minion_id)


class TB_BaconUps_162(BGS_123):
    # Tempête de la taverne premium
    nb_strike = 2


class BGS_010(Minion):
    # Maitre de guerre annihiléen
    def battlecry(self, sequence):
        self.buff(self.enchantment_dbfId, self, max_health=self.bonus_value)

    @property
    def bonus_value(self) -> int:
        return self.controller.max_health - self.controller.health


class TB_BaconUps_083(BGS_010):
    # Maitre de guerre annihiléen premium
    @property
    def bonus_value(self) -> int:
        return (self.controller.max_health - self.controller.health)*2


class BGS_048(battlecry_select_one_minion_and_buff_it):
    # Gaillarde des mers du Sud
    def battlecry(self, sequence):
        for minion in sequence.targets:
            self.buff(self.enchantment_dbfId, minion)

    @property
    def nb_strike(self) -> int:
        return len(self.controller.bought_minions[self.nb_turn].filter(race='PIRATE'))
TB_BaconUps_140= BGS_048 # Gaillarde des mers du Sud premium


class ICC_807(Minion):
    # Pillard dure-écaille
    def battlecry(self, sequence):
        for minion in self.my_zone.cards.filter(TAUNT=True):
            self.buff(self.enchantment_dbfId, minion)
TB_BaconUps_072= ICC_807 # Pillard dure-écaille premium


class BGS_030(battlecry_select_all_and_buff_them):
    # Roi Bagargouille
    deathrattle= battlecry_select_all_and_buff_them.battlecry
TB_BaconUps_100= BGS_030 # Roi Bagargouille premium


class EX1_506(Minion):
    # chasse-marée
    def battlecry(self, sequence):
        self.invoc(sequence, self.repop_dbfId)
TB_BaconUps_003= EX1_506 # chasse-marée premium
CFM_315= EX1_506 # chat de gouttière
TB_BaconUps_093= EX1_506 # chat de gouttière premium


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
    def battlecry(self, sequence):
        self.controller.levelup_cost_mod -= self.__class__.bonus_value


class TB_BaconUps_126(BGS_055):
    # Mousse du pont premium
    bonus_value = 2


class EX1_093(Minion):
    # Défenseur d'Argus
    def battlecry(self, sequence):
        self.buff(self.enchantment_dbfId, *self.adjacent_neighbors())
TB_BaconUps_009= EX1_093 # Défenseur d'Argus premium


class LOOT_013(Minion):
    # Homoncule_sans_gene
    def battlecry(self, sequence):
        self.controller.dec_health(2)
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
    def battlecry(self, sequence):
        minion_list = self.my_zone.cards.one_minion_by_type()
        if minion_list:
            random.shuffle(minion_list)
            self.buff(self.enchantment_dbfId, *minion_list[:3])
TB_BaconUps_144= BGS_082 # Tasse de la ménagerie premium
BGS_083= BGS_082 # Théière de la ménagerie
TB_BaconUps_145= BGS_082 # Théière de la ménagerie premium


class BGS_122(Minion):
    # Elementaire de stase
    nb_strike = 1
    def battlecry(self, sequence):
        minion_id = self.discover(
            self.controller.bob.local_hand.filter(race='ELEMENTAL'),
            nb=1)
        self.controller.bob.board.append(minion_id)
        if minion_id in self.controller.bob.board.cards:
            minion_id.FREEZE = True


class TB_BaconUps_161(BGS_122):
    # Elementaire de stase premium
    nb_strike = 2


class BGS_028(Minion):
    # Lapin-échasseur
    def play_start(self, sequence):
        super().play_start(sequence)
        played_lapin = 0
        for minion_list in self.controller.played_cards.values():
            played_lapin += minion_list.count(CardName.LAPIN)
            played_lapin += minion_list.count(CardName.LAPIN_P)
        sequence.nb_strike = played_lapin

    def battlecry(self, sequence):
        self.buff(self.enchantment_dbfId, self)
TB_BaconUps_077= BGS_028 # Lapin-échasseur premium


##### DEATHRATTLE #####

class BGS_040(Minion):
    # Nadina
    def deathrattle(self, sequence):
        for minion in self.my_zone.cards.filter(race='DRAGON'):
            minion.DIVINE_SHIELD = True
TB_BaconUps_154= BGS_040 # Nadina premium


class BGS_018(Minion):
    # Goldrinn
    def deathrattle(self, sequence):
        for minion in self.my_zone.cards.filter(race='BEAST'):
            self.buff(self.enchantment_dbfId, minion)


class TB_BaconUps_085(BGS_018):
    # Goldrinn premium
    pass


class BGS_121(deathrattle_repop):
    # Gentil djinn
    nb_repop = 1
    def deathrattle(self, sequence):
        super().deathrattle(sequence)
        for repop in sequence._repops:
            # les cartes sont-elles retirées de la main de bob ?
            self.controller.hand.create_card_in(repop)

    @property
    def repop_dbfId(self) -> int:
        """
        donne-t-il un elem au hasard de la taverne ou une carte elem choisie au
        hasard parmi toutes les possibilités ?
        maj 18.6 : summon que des serviteurs d'un niveau inférieur ou égal à celui de la taverne
        TODO: Gentle Djinni firstly summons an elemental, and only then puts a copy of it in hand. Therefore, if Djinni's deathrattle triggers more than once, but there is not enough space on board to summon another minion, the player will not receive a second and subsequent copy of elemental.
        : le gain ne se fait que si le repop à lieu
        """
        return random.choice(self.controller.bob.local_hand.filter(race='ELEMENTAL').exclude(self.dbfId)).dbfId

class TB_BaconUps_165(BGS_121):
    # Gentil djinn premium
    nb_repop = 2


class TRLA_149(deathrattle_repop):
    # Boagnarok
    nb_repop = 2

    @property
    def repop_dbfId(self):
        cards = self.game.card_can_collect.filter(DEATHRATTLE=True).exlude(self.dbfId)
        return random.choice(cards)


class TB_BaconUps_057(TRLA_149):
    # Boagnarok premium
    nb_repop = 4


class BGS_079(deathrattle_repop):
    # Tranche-les-vagues
    nb_repop = 3

    @property
    def repop_dbfId(self):
        cards = self.game.card_can_collect.filter(race='PIRATE').exlude(self.dbfId)
        return random.choice(cards)


class TB_BaconUps_137(BGS_079):
    # Tranche-les-vagues premium
    nb_repop = 6


class BGS_006(deathrattle_repop):
    # Vieux déchiqueteur de Sneed
    nb_repop = 1

    @property
    def repop_dbfId(self):
        cards = self.game.card_can_collect.filter(elite=True).exlude(self.dbfId)
        return random.choice(cards)


class TB_BaconUps_080(BGS_006):
    # Vieux déchiqueteur de Sneed premium
    nb_repop = 2


class BGS_126(Minion):
    # Elémentaire du feu de brousse
    def combat_end(self, sequence):
        for target in sequence.targets:
            damage_left = -target.health
            new_targets = target.adjacent_neighbors()
            if new_targets and damage_left > 0:
                new_target = random.choice(new_targets)
                self.damage(new_target, damage_left)


class TB_BaconUps_166(Minion):
    # Elémentaire du feu de brousse premium
    def combat_end(self, sequence):
        for target in sequence.targets:
            damage_left = -target.health
            if damage_left > 0:
                for target in target.adjacent_neighbors():
                    self.damage(target, damage_left)


class BGS_032(Minion):
    bonus_value = 3
    # Héraut de la flamme
    def overkill(self, sequence):
        for minion in self.my_zone.opponent:
            if minion.is_alive:
                self.append_action(
                    self.damage,
                    minion,
                    self.__class__.bonus_value)
                break


class TB_BaconUps_103(BGS_032):
    # Héraut de la flamme premium
    bonus_value = 6


class BGS_044(hit_by_repop):
    # Maman des diablotins
    # Note: couplé avec Khadgar, le second repop ne possède pas TAUNT
    nb_repop = 1
    def hit(self, sequence):
        if self is sequence.target:
            super().hit(sequence)
            for minion in sequence._repops:
                self.buff(self.enchantment_dbfId, minion)

    @property
    def repop_dbfId(self):
        return random.choice(self.game.card_can_collect.filter(race='DEMON').exclude(self.dbfId))


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
    def deathrattle(self, sequence):
        self.append_action(
            self.damage,
            random.choice(self.controller.opponent.board.cards),
            4,
            overkill=False)


class TB_BaconUps_028(BOT_606):
    # Gro'Boum premium
    nb_strike = 2


class OG_256(Minion):
    # Rejeton de N'Zoth
    def deathrattle(self, sequence):
        self.buff(self.enchantment_dbfId, *sequence.controller.board.cards)
TB_BaconUps_025= OG_256


class CFM_316(deathrattle_repop):
    # Clan des rats
    @property
    def nb_repop(self):
        return min(self.attack, FIELD_SIZE)
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


class OG_221(Minion):
    # Héroïne altruiste
    nb_strike = 1
    def deathrattle(self, sequence):
        minions = self.controller.board.cards.exclude(DIVINE_SHIELD=True, is_alive=False)
        if minions:
            random.choice(minions).DIVINE_SHIELD = True


class TB_BaconUps_014(OG_221):
    # Héroïne altruiste premium
    nb_strike = 2


class YOD_026(Minion):
    # Serviteur diabolique
    nb_strike = 1

    def deathrattle(self, sequence):
        minions = self.controller.board.cards.filter(is_alive=True)
        if minions:
            self.buff(self.enchantment_dbfId, random.choice(minions), attack=self.attack)


class TB_BaconUps_112(YOD_026):
    # Serviteur diabolique premium
    nb_strike = 2


class FP1_024(Minion):
    # Goule instable
    nb_strike = 1

    def deathrattle(self, sequence):
        for minion in self.controller.board.opponent.cards:
            self.append_action(
                self.damage,
                minion,
                1,
                overkill=False)
        for minion in self.controller.board.cards:
            self.append_action(
                self.damage,
                minion,
                1,
                order=0,
                overkill=False)


class TB_BaconUps_118(FP1_024):
    # Goule instable premium
    nb_strike = 2


class BG20_101(Minion):
    # Chauffard huran
    nb_strike = 1
    def frenzy(self, sequence):
        self.controller.hand.create_card_in(CardName.BLOOD_GEM)


class BG20_101_G(BG20_101):
    # Chauffard huran premium
    nb_strike = 2


class BG20_102(Minion):
    # Défense robuste
    def enhance_off(self, sequence):
        if sequence.target is self and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT:
            self.buff(self.enchantment_dbfId, self)
            self.buff(-70167, self) # ??


class BG20_102_G(BG20_102):
    # Défense robuste premium
    def enhance_off(self, sequence):
        if sequence.target is self and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT:
            self.buff(self.enchantment_dbfId, self)


class BG20_103(Minion):
    # Brute dos-hirsute
    bonus_value = 2

    def enhance_on(self, sequence):
        if sequence.target is self and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT and\
                self.temp_counter == 0:
            sequence.source.attack += self.__class__.bonus_value
            sequence.source.max_health += self.__class__.bonus_value
            self.temp_counter += 1


class BG20_103_G(BG20_103):
    # Brute dos-hirsute premium
    bonus_value = 4


class BG20_105(Minion):
    # Mande-épines
    nb_strike = 1
    def battlecry(self, sequence):
        self.controller.hand.create_card_in(CardName.BLOOD_GEM)
    deathrattle = battlecry


class BG20_105_G(BG20_105):
    # Mande-épines premium
    nb_strike = 2


class BG20_202(Minion):
    # Nécrolyte
    def play_start(self, sequence: Sequence):
        super().play_start(sequence)
        if sequence.is_valid:
            minion = self.choose_one_of_them(
                self.controller.board.cards)
            sequence.add_target(minion)

    def battlecry(self, sequence):
        for minion in sequence.targets:
            for neighbour in minion.adjacent_neighbors():
                change = False
                for enchantment in neighbour.entities[::-1]:
                    if enchantment.dbfId == CardName.BLOOD_GEM_ENCHANTMENT:
                        enchantment.apply(minion)
                        change = True
                if change:
                    neighbour.calc_stat_from_scratch()
            minion.calc_stat_from_scratch()
BG20_202_G= BG20_202 # Nécrolyte premium


class BG20_201(Minion):
    # Porte-bannière huran
    nb_strike = 1

    def turn_off(self, sequence):
        for neighbour in self.adjacent_neighbors().filter(race='QUILBOAR'):
            self.buff(CardName.BLOOD_GEM_ENCHANTMENT, neighbour)


class BG20_201_G(BG20_201):
    # Porte-bannière huran premium
    nb_strike = 2


class BG20_104(Minion):
    # Cogneur
    def combat_end(self, sequence):
        self.controller.hand.create_card_in(CardName.BLOOD_GEM)
BG20_104_G= BG20_104


class BG20_207(Minion):
    # Duo dynamique
    def enhance_off(self, sequence):
        target = sequence.target
        if self.controller is target.controller and\
                target.race.HURAN and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT and\
                self is not sequence.target:
            self.buff(self.enchantment_dbfId, self)
BG20_207_G= BG20_207 # Duo dynamique premium


class BG20_106(Minion):
    bonus_value = 2
    # Tremble-terre
    def enhance_off(self, sequence):
        if sequence.target is self and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT:
            for minion in self.my_zone.cards.exlude(self):
                self.buff(self.enchantment_dbfId, minion, attack=self.__class__.bonus_value)


class BG20_106_G(BG20_106):
    # Tremble-terre premium
    bonus_value = 4


class BG20_204(Minion):
    # Chevalier dos-hirsute
    def frenzy(self, sequence):
        self.DIVINE_SHIELD = True

BG20_204_G= BG20_204


class BG20_302(Minion):
    # Aggem malépine
    def enhance_off(self, sequence):
        if sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT and\
                self is sequence.target:
            for minion in self.my_zone.cards.one_minion_by_type():
                self.buff(self.enchantment_dbfId, minion)
BG20_302_G= BG20_302 # Aggem malépine premium


class BG20_205(Minion):
    # Agamaggan
    bonus_value = 1
    def enhance_on(self, sequence):
        if sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT and\
                self.controller is sequence.source.controller:
            sequence.source.attack += self.__class__.bonus_value
            sequence.source.max_health += self.__class__.bonus_value

class BG20_205_G(Minion):
    # Agamaggan premium
    bonus_value = 2


class BG20_303(Minion):
    # Charlga
    nb_strike = 1
    def turn_off(self):
        for minion in self.my_zone.cards:
            self.buff(CardName.BLOOD_GEM_ENCHANTMENT, minion)


class BG20_303_G(BG20_303):
    # Charlga premium
    nb_strike = 2


class BG20_206(Minion):
    # Capitaine Plate-Défense
    #TODO: sequence + optimisation
    mod_quest_value = 4
    def unknown(self, sequence):
        for _ in range(sequence.gold_spend):
            self.quest_value += 1
            if self.quest_value % self.__class__.mod_quest_value == 0:
                self.controller.hand.create_card_in(CardName.BLOOD_GEM)


class BG20_206_G(BG20_206):
    # Capitaine Plate-Défense premium
    nb_strike = 2
    def unknown(self, sequence):
        for _ in range(sequence.gold_spend):
            self.quest_value += 1
            if self.quest_value % self.__class__.mod_quest_value == 0:
                self.controller.hand.create_card_in(CardName.BLOOD_GEM)
                self.controller.hand.create_card_in(CardName.BLOOD_GEM)


def wake_up(self):
    # Maeiv effect
    self.create_and_apply_enchantment(62265)
    self.owner.opponent.owner.hand.append(self)


class BG20_203(Minion):
    # Prophète du sanglier
    def turn_on(self, sequence):
        self.quest_value = 1

    def play_off(self, sequence):
        source = sequence.source
        if source.race.QUILBOAR and\
                source.controller is self.controller and\
                self.quest_value > 0:
            self.controller.hand.create_card_in(CardName.BLOOD_GEM)
            self.quest_value -= 1


class BG20_203_G(BG20_203):
    # Prophète du sanglier premium
    def play_off(self, sequence):
        source = sequence.source
        if source.race.QUILBOAR and\
                source.controller is self.controller and\
                self.quest_value > 0:
            self.controller.hand.create_card_in(CardName.BLOOD_GEM, CardName.BLOOD_GEM)
            self.quest_value -= 1


class BG20_304(Minion):
    # Archidruide Hamuul
    #TODO
    #note: c'est considéré une actualisation : le pouvoir de Ysera s'active
    def battlecry(self, sequence):
        pass
BG20_304_G= BG20_304


class BG21_027(Minion):
    # Chromaile évolutive
    def levelup_off(self, sequence):
        self.buff(self.enchantment_dbfId, self, attack=self.bonus_value)

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
    def deathrattle(self, sequence):
        minions = self.controller.board.cards.filter(is_alive=True).exclude(self)
        if minions:
            self.buff(self.enchantment_dbfId,
                random.choice(minions),
                max_health=self.max_health)


class BG21_006_G(BG21_006):
    # Entourloupeur impétueux premium
    nb_strike = 2


class BGS_060(Minion):
    # Yo oh ogre
    pass

class TB_BaconUps_150(Minion):
    # Yo oh ogre premium
    pass

class BGS_039(Minion):
    # Lieutenant draconide
    pass

class TB_BaconUps_146(Minion):
    # Lieutenant draconide premium
    pass

class BGS_106(Minion):
    # Acolyte de C'Thun
    pass

class TB_BaconUps_255(Minion):
    # Acolyte de C'Thun premium
    pass

class VAN_EX1_506a(Minion):
    # éclaireur murloc
    pass

class TB_BaconUps_003t(Minion):
    # éclaireur murloc premium
    pass

class CFM_315t(Minion):
    # chat tigré
    pass

class TB_BaconUps_093t(Minion):
    # chat tigré premium
    pass

class BGS_061t(Minion):
    # pirate du ciel
    def summon_off(self, sequence):
        # attack immediatly
        pass

class TB_BaconUps_141t(Minion):
    # pirate du ciel premium
    pass

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
                    bonus += self.__class__.bonus_value
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
    def play_off(self, sequence):
        source = sequence.source
        if source.race.MURLOC and source.controller is self.controller:
            targets = self.owner.cards.filter(race='MURLOC').exclude(self)
            random.shuffle(targets)
            for target in targets[:2]:
                self.buff(self.enchantment_dbfId, target)
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
    def enhance_off(self, sequence):
        if sequence.target.race.DRAGON and\
                sequence.target.controller is self.controller and\
                getattr(sequence.source, 'attack', 0) > 0:
            sequence(self.buff, self.enchantment_dbfId)
BG21_013_G= BG21_013 # Contrebandier dragonnet premium


class BG21_000(Minion):
    # Saute-mouton
    def deathrattle(self, sequence):
        targets = self.owner.cards.filter(race='BEAST', is_alive=True)
        if targets:
            self.buff(self.enchantment_dbfId, random.choice(targets))
BG21_000_G= BG21_000 # Saute-mouton premium


class BG21_017(Minion):
    # Contrebandier saumâtre
    nb_strike = 1
    def turn_off(self, sequence):
        have_another_pirate = self.owner.cards.filter(race='PIRATE').exclude(self)
        if have_another_pirate:
            self.controller.hand.create_card_in(CardName.COIN)


class BG21_017_G(BG21_017):
    # Contrebandier saumâtre premium
    nb_strike = 2


class BG21_021(battlecry_select_one_minion_and_buff_it):
    # Enfumeur
    def battlecry(self, sequence: Sequence):
        for minion in sequence.targets:
            self.buff(self.enchantment_dbfId, minion, attack=self.bonus_value, max_health=self.bonus_value)

    @property
    def bonus_value(self) -> int:
        return self.controller.level


class BG21_021_G(BG21_021):
    # Enfumeur premium
    @property
    def bonus_value(self) -> int:
        return self.controller.level*2


class BG21_037(Minion):
    # Briseur de gemmes
    nb_strike = 1
    def loss_shield_off(self, sequence):
        if sequence.source.controller is self.controller:
            self.controller.hand.create_card_in(CardName.BLOOD_GEM)


class BG21_037_G(BG21_037):
    # Briseur de gemmes premium
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
    def summon_start(self, sequence):
        super().summon_start(sequence)
        if sequence.is_valid:
            self.buff(-76567, self.controller)
BG21_039_G= BG21_039 # Kathra’natir premium


class BG21_030(Minion):
    # Mainverte en herbe
    def avenge(self, sequence):
        for minion in self.adjacent_neighbors():
            self.buff(self.enchantment_dbfId, minion)


class BG21_030_G(BG21_030):
    # Mainverte en herbe premium
    pass


class BG21_002(Minion):
    # Pote à plumes
    def avenge(self, sequence):
        for minion in self.owner.cards.filter(race='BEAST'):
            self.buff(self.enchantment_dbfId, minion)


class BG21_002_G(BG21_002):
    # Pote à plumes premium
    pass


class BG21_015(Minion):
    # Tarecgosa
    #TODO: rendre compatible avec le bonus de Nadina ou Héroïne altruiste
    def enhance_on(self, sequence):
        if self.in_fight_sequence and sequence.target is self:
            try:
                del sequence.source.duration
            except AttributeError:
                pass


class BG21_015_G(BG21_015):
    # Tarecgosa premium
    def enhance_on(self, sequence):
        if self.in_fight_sequence and sequence.target is self:
            super().enhance_on(sequence)
            #TODO: copy


class BG21_007(Minion):
    # Auspice funeste impatient
    nb_strike = 1
    def avenge(self, sequence):
        minion = random.choice(self.controller.bob.local_hand.filter(race='DEMON'))
        self.controller.hand.append(minion)


class BG21_007_G(BG21_007):
    # Auspice funeste impatient premium
    nb_strike = 2


class BG21_024(Minion):
    # Graiss-o-bot
    def loss_shield_off(self, sequence):
        if sequence.source.my_zone is self.my_zone:
            self.buff(self.enchantment_dbfId, sequence.source)


class BG21_024(BG21_024):
    # Graiss-o-bot premium
    pass


class BG21_038(Minion):
    # Matrone ensorçaile
    nb_strike = 1
    def avenge(self, sequence):
        # TODO: à tester, probablement non fonctionnel
        minion = random.choice(self.controller.bob.local_hand.filter(battlecry=True))
        self.controller.hand.append(minion)


class BG21_038_G(BG21_038):
    # Matrone ensorçaile premium
    nb_strike = 2


class BG21_023(Minion):
    # Méca-tank
    nb_strike = 1

    def avenge(self, sequence):
        opponent_board = self.my_zone.opponent[:]
        random.shuffle(opponent_board)
        opponent_board.sort(key=lambda x: x.health)
        target = opponent_board[-1]
        self.damage(target, 6)


class BG21_023_G(BG21_023):
    # Méca-tank premium
    nb_strike = 2


class BG21_016(Minion):
    # Peggy les Os-de-verre
    def add_card_on_hand_off(self, sequence):
        if sequence.source.controller is self.controller:
            pirates = self.my_zone.cards.filter(race='PIRATE').exclude(self)
            if pirates:
                self.buff(self.enchantment_dbfId, random.choice(pirates))


class BG21_016_G(BG21_016):
    # Peggy les Os-de-verre premium
    pass


class BG21_012(Minion):
    # Pyrogéniture de Prestor
    bonus_value = 3

    def combat_on(self, sequence):
        if sequence.source.my_zone is self.my_zone and sequence.source.race.DRAGON:
            for target in sequence.targets:
                sequence(self.damage, target, self.__class__.bonus_value)


class BG21_012_G(BG21_012):
    # Pyrogéniture de Prestor
    bonus_value = 6


class BG21_020(Minion):
    # Rejeton de Lumière éclatant
    bonus_value = 1
    #TODO: activer le bonus
    def avenge(self, sequence):
        self.buff(self.enchantment_dbfId,
            self.controller,
            bonus_value=self.__class__.bonus_value)


class BG21_020_G(BG21_020):
    # Rejeton de Lumière éclatant premium
    bonus_value = 2


class BG21_014(Minion):
    # Super promo-Drake
    bonus_value = 1
    def fight_on(self, sequence):
        nb_dragons = len(self.my_zone.filter(race='DRAGON'))
        for minion in self.adjacent_neighbors():
            for _ in range(nb_dragons):
                self.buff(self.enchantment_dbfId, minion,
                    attack=self.__class__.bonus_value,
                    max_health=self.__class__.bonus_value)


class BG21_014_G(BG21_014):
    # Super promo-Drake premium
    bonus_value = 2



class BG21_040(Minion):
    # Âme en peine recycleuse
    nb_roll = 1
    def play_off(self, sequence):
        if self.my_zone is sequence.source.my_zone and sequence.source.race.ELEMENTAL:
            self.buff(self.enchantment_dbfId, self.controller, bonus_value=self.__class__.nb_roll)


class BG21_040_G(BG21_040):
    # Âme en peine recycleuse premium
    nb_roll = 2


class BG21_001(Minion):
    # Crocilisque claires-écailles
    def avenge(self, sequence):
        targets = self.my_zone.cards.filter(race='BEAST').exclude(self)
        if targets:
            self.buff(self.enchantment_dbfId, random.choice(targets))
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
    def enhance_on(self, sequence):
        if sequence.source.my_zone is self.my_zone and\
                sequence.source.race.ELEMENTAL and\
                (getattr(sequence.source, 'attack', 0) > 0 or\
                getattr(sequence.source, 'max_health', 0) > 0):
            sequence(self.buff, self.enchantment_dbfId, self)


class BG21_036(BG21_036):
    # Maître des réalités premium
    pass


class BG20_401(Minion):
    # Mécareau divin
    def loss_shield_off(self, sequence):
        if sequence.source.controller is self.controller:
            self.DIVINE_SHIELD = True


class BG20_401_G(BG20_401):
    # Mécareau divin premium
    pass


class BG21_009(Minion):
    #SI:septique
    nb_strike = 1
    def avenge(self, sequence):
        targets = self.my_zone.cards.filter(race='MURLOC', POISONOUS=False, is_alive=True)
        if targets:
            self.buff(self.enchantment_dbfId, random.choice(targets))


class BG21_009_G(BG21_009):
    #SI:septique
    nb_strike = 2


class BG21_031(Minion):
    # Tony Deux-Défenses
    nb_strike = 1
    def avenge(self, sequence):
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
    def play_off(self, sequence):
        if sequence.source.owner and self.owner and sequence.source.race.DEMON:
            targets = self.my_zone.opponent
            if targets:
                target = random.choice(targets)
                self.buff(self.enchantment_dbfId,
                    self,
                    attack=target.attack*self.__class__.bonus_mult,
                    max_health=target.max_health*self.__class__.bonus_mult)
                self.controller.opponent.hand.append(target)

class BG21_004_G(BG21_004):
    # Ur'Zul insatiable premium
    bonus_mult = 2


class BG21_025(deathrattle_repop):
    # Casseur Oméga
    nb_repop = 5
    def deathrattle(self, sequence):
        super().deathrattle(sequence)
        nb_minion_repop = len(sequence._repops)
        for minion in self.controller.board.cards.filter(race='MECHANICAL'):
            for _ in range(self.__class__.nb_repop - nb_minion_repop):
                self.buff(self.enchantment_dbfId, minion)
BG21_025_G= BG21_025 # Casseur Oméga premium


class BG21_005(Minion):
    # Gangroptère affamé
    bonus_mult = 1
    def turn_off(self, sequence):
        for demon in self.my_zone.cards.filter(race='DEMON'):
            targets = self.my_zone.opponent
            if not targets:
                break
            target = random.choice(targets)
            self.buff(self.enchantment_dbfId,
                demon,
                attack=target.attack*self.__class__.bonus_mult,
                max_health=target.max_health*self.__class__.bonus_mult)
            self.controller.bob.hand.append(target)

class BG21_005_G(BG21_005):
    # Gangroptère affamé premium
    bonus_mult = 2


class BG21_011(Minion):
    # Lanceur de crustacés
    def play_start(self, sequence: Sequence):
        super().play_start(sequence)
        if sequence.is_valid:
            minion = self.choose_one_of_them(
                self.controller.board.cards.filter(race=self.synergy)+\
                self.controller.board.opponent.cards.filter(race=self.synergy))
            sequence.add_target(minion)

    def battlecry(self, sequence):
        for minion in sequence.targets:
            #TODO
            pass
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
    def turn_on_off(self, sequence):
        self.quest_value += 1
        if self.quest_value % self.__class__.mod_quest_value == 0:
            minion = random.choice(self.controller.bob.hand.cards)
            self.controller.hand.append(minion)
            #TODO: SET GOLD


class BG21_019_G(BG21_019):
    # Pillarde curieuse
    mod_quest_value = 1
