from base.entity import Minion
from base.enums import CardName, ADAPT_ENCHANTMENT
from base.scripts.base import *
import random
from base.utils import repeat_effect
from base.sequence import Sequence
from base.db_card import Card_data



class BG21_030(Minion):
    # Mainverte en herbe
    def avenge(self, sequence: Sequence):
        for minion in self.adjacent_neighbors():
            self.buff(minion)
BG21_030_G= BG21_030 # Mainverte en herbe premium


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


UNG_999t2t1= Minion # Plante
BGS_131= Minion # Spore mortelle
TB_BaconUps_251= Minion  # Spore mortelle premium
BGS_106= Minion # Acolyte de C'Thun
TB_BaconUps_255= Minion # Acolyte de C'Thun premium
TB_BaconShop_HP_033t= Minion # Amalgame
EX1_170= Minion # Cobra empereur
EX1_554t= Minion # Serpent


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
TB_BaconUps_091= BGS_022 # Zapp Mèche-sournoise premium


class BG20_304(Minion):
    # Archidruide Hamuul
    #TODO
    #note: c'est considéré une actualisation : le pouvoir de Ysera s'active
    @repeat_effect
    def battlecry(self, sequence: Sequence):
        pass
BG20_304_G= BG20_304


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


class OG_256(Minion):
    # Rejeton de N'Zoth
    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        for minion in self.controller.board.cards:
            self.buff(minion)
TB_BaconUps_025= OG_256


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


class EX1_093(Minion):
    # Défenseur d'Argus

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        for minion in self.adjacent_neighbors():
            self.buff(minion)
TB_BaconUps_009= EX1_093 # Défenseur d'Argus premium


class ICC_807(Minion):
    # Pillard dure-écaille

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        for minion in self.my_zone.cards.filter(TAUNT=True):
            self.buff(minion)
TB_BaconUps_072= ICC_807 # Pillard dure-écaille premium


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


class BGS_009(Minion):
    # Massacreuse croc radieux
    def turn_off(self, sequence: Sequence):
        for minion in self.my_zone.cards.one_minion_by_race():
            self.buff(minion)
TB_BaconUps_082= BGS_009  # Massacreuse croc radieux premium


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


class BGS_111(Minion):
    # Champion d'Y'Shaarj
    valid_for_myself = True
    def combat_on(self, sequence: Sequence):
        if sequence.target.TAUNT and sequence.is_ally(self):
            self.buff(self)
TB_BaconUps_301= BGS_111 # Champion d'Yshaarj premium
BGS_110= BGS_111 # Bras de l'empire
TB_BaconUps_302= BGS_110 # Bras de l'empire premium


class AT_121(Minion):
    # Favori de la foule
    def play_on(self, sequence: Sequence):
        if sequence.source.BATTLECRY:
            self.buff(self)
TB_BaconUps_037= AT_121 # Favori de la foule premium


class BAR_073(Minion):
    # Forgeronne des Tarides
    def frenzy(self, sequence: Sequence):
        for minion in self.my_zone.cards.exclude(self):
            self.buff(minion)
TB_BaconUps_320= BAR_073 # Forgeronne des Tarides premium


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
TB_BaconUps_257= BGS_201 # Ritualiste tourmenté premium


class BGS_113(Minion):
    # Habitué sans visage
    @repeat_effect
    def battlecry(self, sequence: Sequence):
        # comment se passe la gestion lors de la revente, la copie est enlevée de la taverne ou est-ce 
        # l'habitué ?
        pass
TB_BaconUps_305= BGS_113 # Habitue_sans_visage premium


ICC_038= Minion # Protectrice vertueuse
TB_BaconUps_147= Minion # Protectrice vertueuse premium


class ICC_858(Minion):
    # Bolvar sang-de-feu
    valid_for_myself = True
    def loss_shield_off(self, sequence: Sequence):
        if sequence.is_ally(self):
            self.buff(self)
TB_BaconUps_047= ICC_858 # Bolvar sang-de-feu premium
