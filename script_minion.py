# coding : utf-8

import random
from enums import Race, State, Event, CardName, Type, BATTLE_SIZE
import script_functions
from utils import *
from action import *

class BGS_043:
    # Murozond
    def battlecry(self):
        pass
"""
    board_adv = self.owner.owner.last_opponent.real_board
    if board_adv and self.owner.owner.hand.can_add_card():
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

    if board_adv and self.owner.owner.hand.can_add_card():
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

class MTB_BaconUps_110:
    # Murozond premium
    def battlecry(self):
        pass

class BGS_113:
    # Habitue_sans_visage
    def battlecry(self):
        # comment se passe la gestion lors de la revente, la copie est enlevée de la taverne ou est-ce 
        # l'habitué ?
        pass

class TB_BaconUps_305:
    # Habitue_sans_visage premium
    def battecry(self):
        pass

class BGS_104:
    # Nomi
    def play(self, card):
        # l'event s'active seulement après un cri de guerre, ce n'est donc pas un PLAY
        # mais un event AFTER_PLAY (nomi buff les elems générés par l'élémentaire de stase,
        # après que ce dernier soit joué)
        # enchantment_id : 64167
        if self != card and card.race & Race.ELEMENTAL:
            self.owner.owner.bonus_nomi += self.double_if_premium(1)

class TB_BaconUps_201:
    # Nomi premium
    def play(self, card):
        pass

class BGS_036:
    # Tranchetripe
    def end_turn(self, enchantment_id='60562'):
        nb = len(self.owner.cards.filter_hex(race=Race.DRAGON))
        for _ in range(nb):
            self.buff(enchantment_id, self)

class TB_BaconUps_106:
    # Tranchetripe premium
    end_turn= lambda self: BGS_036.end_turn(self, '60650')

class BGS_072:
    # Captaine_Larrrrdeur
    def buy(self, source):
        if source.race & Race.PIRATE:
            self.controller.gold += 1

class TB_BaconUps_133:
    # Captaine_Larrrrdeur premium
    def buy(self, source):
        if source.race & Race.PIRATE:
            self.controller.gold += 2

class BGS_059:
    # Dévoreur d'âmes
    def battlecry(self):
        minion = self.choose_one_of_them(\
            self.my_zone.cards.filter(race=Race.DEMON).exclude(self))
        if minion:
            self.controller.gold += 3
            self.buff("61080", self, attack=minion.attack, max_health=minion.health)
            self.controller.bob.hand.append(minion)

class TB_BaconUps_119:
    # Dévoreur d'âmes premium
    def battlecry(self):
        minion = self.choose_one_of_them(\
            self.my_zone.cards.filter(race=Race.DEMON).exclude(self))
        if minion:
            self.controller.gold += 6
            self.buff("61080", self, attack=minion.attack*2, max_health=minion.health*2)
            self.controller.bob.hand.append(minion)

def Apprentie_reinit(self):
    #TODO: check graveyard ?
    self.mech_die = []

def Apprentie_kill(self, victim):
    if victim.race & Race.MECH:
        try:
            self.mech_die.append(victim.dbfId)
        except AttributeError:
            pass

class BGS_012:
    # Apprentie de Kangor
    def deathrattle(self, position):
        try:
            for repop in self.mech_die[:2]:
                script_functions.invocation(self, repop, 1, self.position)
        except AttributeError:
            pass

class TB_BaconUps_087:
    # Apprentie de Kangor premium
    def deathrattle(self, position):
        try:
            for repop in self.mech_die[:4]:
                script_functions.invocation(self, repop, 1, self.position)
        except AttributeError:
            pass

class GVG_021:
    # Mal'Ganis
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = GVG_021.aura
            self.apply_met_on_all_children(GVG_021.aura, self.controller)

    def aura(self, target):
        if self is not target:
            if target.race & Race.DEMON:
                target.buff("2203", target, aura=True)
            elif target is self.controller:
                target.buff("-2203", target, aura=True)

class TB_BaconUps_060:
    # Mal'Ganis premium
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = TB_BaconUps_060.aura
            self.apply_met_on_all_children(TB_BaconUps_060.aura, self.controller)

    def aura(self, target):
        if self is not target:
            if target.race & Race.DEMON:
                target.buff("58429", target, aura=True)
            elif target is self.controller:
                target.buff("-2203", target, aura=True)

class EX1_185:
    # Brise-siège
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = EX1_185.aura
            self.apply_met_on_all_children(EX1_185.aura, self.controller)

    def aura(self, target):
        if target.race & Race.DEMON and target is not self:
            self.buff('54842', target, aura=True)

class TB_BaconUps_053:
    # Brise-siège premium
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = TB_BaconUps_053.aura
            self.apply_met_on_all_children(TB_BaconUps_053.aura, self.controller)

    def aura(self, target):
        if target.race & Race.DEMON and target is not self:
            self.buff('58419', target, aura=True)

class EX1_507:
    # Chef de guerre murloc
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = EX1_507.aura
            self.apply_met_on_all_children(EX1_507.aura, self.controller)

    def aura(self, target):
        if target.race & Race.MURLOC and target is not self:
            self.buff('535', target, aura=True)

class TB_BaconUps_008:
    # Chef de guerre murloc premium
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = TB_BaconUps_008.aura
            self.apply_met_on_all_children(TB_BaconUps_008.aura, self.controller)

    def aura(self, target):
        if target.race & Race.MURLOC and target is not self:
            self.buff('57406', target, aura=True)

class NEW1_027:
    # Capitaine des mers du Sud
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = NEW1_027.aura
            self.apply_met_on_all_children(NEW1_027.aura, self.controller)

    def aura(self, target):
        if target.race & Race.PIRATE and target is not self:
            self.buff('70472', target, aura=True)

class TB_BaconUps_136:
    # Capitaine des mers du Sud premium
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = TB_BaconUps_136.aura
            self.apply_met_on_all_children(TB_BaconUps_136.aura, self.controller)

    def aura(self, target):
        if target.race & Race.PIRATE and target is not self:
            self.buff('62238', target, aura=True)

class BGS_202:
    # Mythrax
    def end_turn(self, enchantment_id='65669'):
        nb = len(self.my_zone.one_minion_by_type())
        for _ in range(nb):
            self.buff("65669", self)

class TB_BaconUps_258:
    # Mythrax premium
    end_turn= lambda self: BGS_202.end_turn(self, '65672')

class BGS_112:
    # Héraut qijari
    def die(self, source, killer, enchantment_id='68225'):
        if source.state & State.TAUNT:
            for minion in source.adjacent_neighbors():
                self.buff(enchantment_id, minion)

class TB_BaconUps_303:
    # Héraut qijari premium
    die= lambda self, source, killer: BGS_112.die(self, source, killer, '68226')

class BGS_200:
    # Gardienne d'antan
    def deathrattle(self, position):
        self.controller.hand.create_card_in(CardName.COIN)

class TB_BaconUps_256:
    # Gardienne d'antan premium
    def deathrattle(self, position):
        for _ in range(2):
            BGS_200.deathrattle(self, position)

class BGS_111:
    # Champion d'Yshaarj
    def defend_ally(self, defenser, enchantment_id='65659'):
        if defenser.state & State.TAUNT:
            self.buff(enchantment_id, self)

class TB_BaconUps_301:
    # Champion d'Yshaarj premium
    defend_ally= lambda self, defenser: BGS_111.defend_ally(self, defenser, '65667')

class BGS_110:
    # Bras de l'empire
    def defend_ally(self, defenser, enchant_id='65670'):
        if defenser.state & State.TAUNT:
            self.buff(enchant_id, defenser)

class TB_BaconUps_302:
    # Bras de l'empire premium
    defend_ally= lambda self, defenser: BGS_110.defend_ally(self, defenser, '65674')

class BGS_201:
    # Ritaliste tourmenté
    def defend_ally(self, defenser, enchant_id='66838'):
        if self is defenser:
            self.buff(enchant_id, *self.adjacent_neighbors())

class TB_BaconUps_257:
    # Ritaliste tourmenté premium
    def defend_ally(self, defenser, enchant_id='66839'):
        BGS_201.defend_ally(self, defenser, enchant_id)

class BGS_046:
    # Nat Pagle
    def die(self, source, killer):
        # n'est pas une découverte à 1 car peut se découvrir lui-même
        if self is source:
            lst = self.controller.bob.local_hand
            if lst:
                self.controller.hand.append(random.choice(lst))

class TB_BaconUps_132:
    # Nat Pagle premium
    def die(self, source, killer):
        for _ in range(2):
            BGS_046.die(self, source, killer)

class BGS_047:
    # Amiral de l'effroi Eliza
    def atk_ally(self, attacker, enchantment_id='62227'):
        if attacker.race & Race.PIRATE:
            for minion in self.my_zone.cards:
                self.buff(enchantment_id, minion)

class TB_BaconUps_134:
    # Amiral de l'effroi Eliza premium
    atk_ally= lambda self, attacker: BGS_047.atk_ally(self, attacker, '62229')

class BGS_056:
    # Capitaine Grondéventre
    def atk_ally(self, attacker, enchantment_id='62256'):
        if attacker.race & Race.PIRATE and self is not attacker:
            self.buff(enchantment_id, attacker)

class TB_BaconUps_139:
    # Capitaine Grondéventre premium
    atk_ally= lambda self, attacker: BGS_056.atk_ally(self, attacker, '62258')

class LOE_077:
    # Brann
    def play_aura(self):
        pass
        #self.owner.add_aura(self, boost_battlecry=self.double_if_premium(1))

class TB_BaconUps_045:
    # Brann
    def play_aura(self):
        pass
        #self.owner.add_aura(self, boost_battlecry=self.double_if_premium(1))

class FP1_031:
    # Baron_Vaillefendre
    def play_aura(self):
        pass
        #self.owner.add_aura(self, boost_deathrattle=self.double_if_premium(1))

class TB_BaconUps_055:
    # Baron_Vaillefendre premium
    def play_aura(self):
        pass
        #self.owner.add_aura(self, boost_deathrattle=self.double_if_premium(1))

class DAL_575:
    # Khadgar
    def play_aura(self):
        pass

class TB_BaconUps_034:
    # Khadgar premium
    def play_aura(self):
        pass


class BGS_066:
    # Raflelor
    def end_turn(self, enchantment_id='62193'):
        #TODO : partiel ?
        for minion in self.my_zone.cards:
            if hasattr(minion, 'battlegroundsNormalDbfId'):
                self.buff(enchantment_id, self)

class TB_BaconUps_130:
    # Raflelor premium
    end_turn= lambda self: BGS_066.end_turn(self, '62195')

class ULD_217:
    # Micromomie
    def end_turn(self, enchantment_id='54810'):
        minions = self.owner.cards.exclude(self)
        if minions:
            self.buff(enchantment_id, random.choice(minions))

class TB_BaconUps_250:
    # Micromomie premium
    end_turn = lambda self: ULD_217.end_turn(self, '64344')

class GVG_027:
    # Sensei de fer
    def end_turn(self, enchantment_id='2220'):
        lst = self.my_zone.cards.filter_hex(race=Race.MECH).exclude(self)
        if lst:
            self.buff(enchantment_id, random.choice(lst))

class TB_BaconUps_044:
    # Sensei de fer premium
    end_turn= lambda self: GVG_027.end_turn(self, '58399')

class BGS_105:
    # Chambellan Executus
    def end_turn(self, enchantment_id='65180'):
        target = self.my_zone[0]
        self.buff(enchantment_id, target)
        for _ in self.controller.played_minions[self.nb_turn].filter_hex(race=Race.ELEMENTAL):
            self.buff(enchantment_id, target)

class TB_BaconUps_207:
    # Chambellan Executus premium
    end_turn= lambda self: BGS_105.end_turn(self, '-65180')

class BG20_210:
    # Maraudeur des ruines
    def end_turn(self, enchantment_id='73088'):
        if len(self.owner.cards) <= 6:
            self.buff(enchantment_id, self)

class BG20_210_G:
    # Maraudeur des ruines premium
    end_turn= lambda self: BG20_210.end_turn(self, '73090')

class BGS_027:
    # Micro-machine
    begin_turn = lambda x: x.buff('2_e', x)

class TB_BaconUps_094:
    # Micro-machine premium
    begin_turn = lambda x: x.buff('60057', x)

class BGS_033:
    # Dragon infâmélique
    def begin_turn(self, enchantment_id='60553'):
        if self.my_zone.win_last_match:
            self.buff(enchantment_id, self)

class TB_BaconUps_104:
    # Dragon infâmélique premium
    begin_turn= lambda self: BGS_033.begin_turn(self, '60646')

class ICC_029:
    # Plaie d'écailles cobalt
    def end_turn(self, enchantment_id='42441'):
        lst = self.my_zone.cards.exclude(self)
        if lst:
            self.buff(enchantment_id, random.choice(lst))

class TB_BaconUps_120:
    # Plaie d'écailles cobalt premium
    end_turn= lambda self: ICC_029.end_turn(self, '61443')

class BGS_009:
    # Massacreuse croc radieux
    def end_turn(self, enchantment_id='59709'):
        for minion in self.owner.one_minion_by_type():
            self.buff(enchantment_id, minion)

class TB_BaconUps_082:
    # Massacreuse croc radieux premium
    end_turn= lambda self: BGS_009.end_turn(self, '59712')

class BGS_115:
    # Élémenplus
    def sell(self, source):
        if self is source and self.controller.type == Type.HERO:
            self.controller.hand.create_card_in("64040")

class TB_BaconUps_156:
    # Élémenplus premium
    def sell(self, source):
        for _ in range(2):
            BGS_115.sell(self, source)

class BG20_301:
    # Bronze couenne
    def sell(self, source):
        if self is source and self.controller.type == Type.HERO:
            self.controller.hand.create_card_in("70136", "70136")

class BG20_301_G:
    # Bronze couenne premium
    def sell(self, source):
        for _ in range(2):
            BG20_301.sell(self, source)

class BG20_100:
    # Geomancien de Tranchebauge
    def battlecry(self):
        self.controller.hand.create_card_in("70136")

class BG20_100_G:
    # Geomancien de Tranchebauge premium
    def battlecry(self):
        for _ in range(2):
            BG20_100.battlecry(self)

class BGS_037:
    # Régisseur du temps
    def sell(self, source, enchantment_id='60639'):
        if self is source and self.controller.type == Type.HERO:
            self.buff(enchantment_id, *self.controller.opponent.board.cards)

class TB_BaconUps_107:
    # Régisseur du temps premium
    sell = lambda self, source: BGS_037.sell(self, source, '60664')

class BGS_049:
    # Parieuse convaincante
    def sell(self, source):
        if self is source and self.controller.type == Type.HERO:
            self.controller.gold += 2

class TB_BaconUps_127:
    # Parieuse convaincante premium
    def sell(self, source):
        if self is source and self.controller.type == Type.HERO:
            self.controller.gold += 5

class ICC_858:
    # Bolvar sang-de-feu
    loss_shield= lambda self: self.buff('46580', self)

class TB_BaconUps_047:
    # Bolvar sang-de-feu premium
    loss_shield= lambda self: self.buff('58406', self)

class BGS_067:
    # Massacreur drakonide
    loss_shield= lambda self: self.buff('61074', self)

class TB_BaconUps_117:
    # Massacreur drakonide premium
    loss_shield= lambda self: self.buff('61076', self)

class BGS_004:
    # Tisse-colère
    def after_play(self, source, enchantment_id='59671'):
        if self is not source and source.race & Race.DEMON:
            self.buff(enchantment_id, self)
            self.controller.health -= 1

class TB_BaconUps_079:
    # Tisse-colère premium
    after_play= lambda self, source: BGS_004.after_play(self, source, '59678')

class EX1_509:
    # Mande-flots murloc
    def invoc(self, source, enchantment_id='1719'):
        if self is not source and source.race & Race.MURLOC:
            if self.controller.fight:
                kwargs = {'duration': 1}
            else:
                kwargs = {}
            self.buff(enchantment_id, self, **kwargs)

class TB_BaconUps_011:
    # Mande-flots murloc premium
    invoc= lambda self, source: EX1_509.invoc(self, source, '58139')

class BGS_100:
    # Mini-Rag
    def after_play(self, source, enchantment_id='64075'):
        if source.race & Race.ELEMENTAL and source is not self:
            self.buff(enchantment_id,
                random.choice(self.my_zone.cards),
                attack=source.level,
                max_health=source.level)

class TB_BaconUps_200:
    # Mini-Rag premium
    def after_play(self, source, enchantment_id='64075'):
        for _ in range(2):
            BGS_100.after_play(self, source, enchantment_id)

class BGS_081:
    # Pillard pirate
    def play(self, source, enchantment_id='62738'):
        if source.race & Race.PIRATE and self is not source:
            self.buff(enchantment_id, self)

class TB_BaconUps_143:
    # Pillard pirate premium
    play= lambda self, source: BGS_081.play(self, source, '62740')

class BGS_041:
    # Kalecgos
    def after_play(self, source, enchantment_id='60644'):
        if self is not source and source.event & Event.BATTLECRY:
            for minion in self.my_zone.cards:
                if minion.race & Race.DRAGON:
                    self.buff(enchantment_id, minion)

class TB_BaconUps_109:
    # Kalecgos premium
    after_play= lambda self, source: BGS_041.after_play(self, source, '60668')

class BGS_124:
    # Lieutenant Garr
    def after_play(self, source, enchantment_id='64082'):
        if self is not source and source.race & Race.ELEMENTAL:
            for minion in self.my_zone.cards:
                if minion.race & Race.ELEMENTAL:
                    self.buff(enchantment_id, self)

class TB_BaconUps_163:
    # Lieutenant Garr premium
    after_play= lambda self, source: BGS_124.after_play(self, source, '64083')

class Favori_de_la_foule:
    # Favori de la foule
    def play(self, source, enchantment_id='2750'):
        if self is not source and source.event & Event.BATTLECRY:
            self.buff(enchantment_id, self)

class Favori_de_la_foule_p:
    # Favori de la foule premium
    play= lambda self, source: Favori_de_la_foule.play(self, source, '58384')

class BGS_075:
    # Saurolisque enragé
    def after_play(self, source, enchantment_id='62164'):
        if source.event & Event.DEATHRATTLE and source is not self:
            self.buff(enchantment_id, self)

class TB_BaconUps_125:
    # Saurolisque enragé premium
    after_play= lambda self, source: BGS_075.after_play(self, source, '62166')

class BGS_127:
    # Roche en fusion
    def after_play(self, source, enchantment_id='64298'):
        if source.race & Race.ELEMENTAL and source is not self:
            self.buff(enchantment_id, self)

class TB_Baconups_202:
    # Roche en fusion premium
    after_play= lambda self, source: BGS_127.after_play(self, source, '64301')

class BGS_120:
    # Elémentaire de fête
    def after_play(self, source, enchantment_id='64057'):
        if source.race & Race.ELEMENTAL and source is not self:
            minions = self.my_zone.cards.filter(race=Race.ELEMENTAL).exclude(self)
            if minions:
                self.buff(enchantment_id, random.choice(minions))

class TB_BaconUps_160:
    # Elémentaire de fête premium
    def after_play(self, source):
        for _ in range(2):
            BGS_120.after_play(self, source)

class BGS_204:
    # Démon démesuré
    def after_play(self, source, enchantment_id='66230'):
        if self is not source and source.race & Race.DEMON:
            self.buff(enchantment_id, self)

class TB_BaconUps_304:
    # Démon démesuré premium
    after_play= lambda self, source: BGS_204.after_play(self, source, '66238')

class BGS_021:
    # Maman ourse
    invoc= lambda self, source: BGS_017.invoc(self, source, '60037')

class TB_BaconUps_090:
    # Maman ourse premium
    invoc= lambda self, source: BGS_017.invoc(self, source, '60039')

class BGS_017:
    # Chef de meute
    def invoc(self, source, enchantment_id='59970'):
        if source.race & Race.BEAST and self is not source:
            self.buff(enchantment_id, source)

class TB_BaconUps_086:
    # Chef de meute premium
    invoc= lambda self, source: BGS_017.invoc(self, source, '59972')

class BGS_045:
    # Gardien des glyphes
    def atk_ally(self, attacker):
        if self is attacker:
            self.buff("61030", self, attack=self.attack)

class TB_BaconUps_115:
    # Gardien des glyphes premium
    def atk_ally(self, attacker):
        if self is attacker:
            self.buff("61030", self, attack=self.attack*2)

class BGS_019:
    # Dragonnet rouge
    def first_strike(self):
        nb_dragon_in_board = len(self.my_zone.cards.filter_hex(race=Race.DRAGON))

        self.append_action(
            damage_fight,
            self,
            self.my_zone.opponent,
            nb_dragon_in_board,
            overkill=False)

class TB_BaconUps_102:
    # Dragonnet rouge premium
    def first_strike(self):
        for _ in range(2):
            BGS_019.first_strike(self)

class BGS_078:
    # Ara monstrueux
    def after_atk_myself(self):
        minion_with_deathrattle = self.my_zone.cards.filter_hex(event=Event.DEATHRATTLE).filter(is_alive=True)

        if minion_with_deathrattle:
            target = random.choice(minion_with_deathrattle)
            target.active_local_event(Event.DEATHRATTLE, position=target.position+1)

class TB_BaconUps_135:
    # Ara monstrueux premium
    def after_atk_myself(self):
        for _ in range(2):
            BGS_078.after_atk_myself(self)

class BGS_071:
    # Déflect-o-bot
    def invoc(self, repop, enchantment_id='61931'):
        if self.controller.fight and repop.race & Race.MECH:
            self.buff(enchantment_id, self)

class TB_BaconUps_123:
    # Déflect-o-bot premium
    invoc= lambda self, repop: BGS_071.invoc(self, repop, '61933')

class BGS_002:
    # Jongleur d'âmes
    def die(self, source, killer):
        if source.race & Race.DEMON:
            self.append_action(
                damage_fight,
                self,
                self.my_zone.opponent,
                3,
                overkill=False)

class TB_BaconUps_075:
    # Jongleur d'âmes premium
    def die(self, source, killer):
        for _ in range(2):
            BGS_002.die(self, source, killer)

class EX1_531:
    # Hyene_charognarde
    def die(self, source, killer, enchantment_id='1633'):
        if source.owner is self.owner and source.race & Race.BEAST:
            self.buff(enchantment_id, self)

class TB_BaconUps_043:
    # Hyene_charognarde premium
    die = lambda self, source, killer:\
        EX1_531.die(self, source, killer, '58396')

class GVG_106:
    # Brik-a-bot
    def die(self, source, killer, enchantment_id='2241'):
        if source.race & Race.MECH:
            self.buff(enchantment_id, self)

class TB_BaconUps_046:
    # Brik-a-bot premium
    die= lambda self, source, killer: GVG_106.die(self, source, killer, '58404')

class TB_BaconShop_HP_105t:
    # Poisson
    def die(self, source, killer):
        if source.event & Event.DEATHRATTLE and\
            source.my_zone is self.my_zone:

            self.buff('-2_e', self, method=source.method, event=Event.DEATHRATTLE)

class TB_BaconUps_307:
    # Poisson premium
    die= TB_BaconShop_HP_105t.die

class BGS_035:
    # Trotte-bougie
    def die(self, source, killer, enchantment_id='60560'):
        if source.race & Race.DRAGON:
            self.buff(enchantment_id, self)

class TB_BaconUps_105:
    # Trotte-bougie premium
    die= lambda self, source, killer: BGS_035.die(self, source, killer, '60648')

### BATTLECRY ###

class BGS_116:
    # Anomalie actualisante
    def battlecry(self):
        if self.controller.bob.nb_free_roll < 1:
            self.controller.bob.nb_free_roll = 1

class TB_BaconUps_167:
    # Anomalie actualisante premium
    def battlecry(self):
        if self.controller.bob.nb_free_roll < 2:
            self.controller.bob.nb_free_roll = 2

class BGS_069:
    # Amalgadon
    def battlecry(self):
        nb = len(self.my_zone.one_minion_by_type())-1 # exclude self
        for _ in range(nb):
            self.add_adapt()

class TB_BaconUps_121:
    # Amalgadon premium
    def battlecry(self):
        for _ in range(2):
            BGS_069.battlecry(self)

class BGS_020:
    # Guetteur primaileron
    def battlecry(self):
        if self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self):
            minion_id = self.discover(
                self.controller.bob.local_hand.filter_hex(race=Race.MURLOC),
                nb=3)
            self.controller.hand.append(minion_id)

class TB_BaconUps_089:
    # Guetteur primaileron premium
    def battlecry(self):
        for _ in range(2):
            BGS_020.battlecry(self)

class BGS_123:
    # Tempête de la taverne
    def battlecry(self):
        minion_id = self.discover(
            self.controller.bob.local_hand.filter_hex(race=Race.ELEMENTAL),
            nb=1)
        self.controller.hand.append(minion_id)

class TB_BaconUps_162:
    # Tempête de la taverne premium
    def battlecry(self):
        for _ in range(2):
            BGS_123.battlecry(self)

class BGS_010:
    # Maitre de guerre annihileen
    def battlecry(self, enchantment_id='59715'):
        bonus = self.controller.max_health - self.controller.health
        self.buff(enchantment_id, self, health=bonus)

class TB_BaconUps_083:
    # Maitre de guerre annihileen premium
    def battlecry(self):
        for _ in range(2):
            BGS_010.battlecry(self)

class BGS_048:
    # Gaillarde des mers du Sud
    def battlecry(self, enchantment_id='62261'):
        minion = self.choose_one_of_them(self.my_zone.cards.filter_hex(race=Race.PIRATE).exclude(self))
        if minion:
            bonus = len(self.controller.bought_minions[self.nb_turn].filter_hex(race=Race.PIRATE))
            for _ in range(bonus):
                self.buff(enchantment_id, minion)

class TB_BaconUps_140:
    # Gaillarde des mers du Sud premium
    battlecry= lambda self: BGS_048.battlecry(self, '62260')

class ICC_807:
    # Pillard dure écaille
    def battlecry(self, enchantment_id="43023"):
        for minion in self.my_zone.cards.filter_hex(state=State.TAUNT):
            self.buff(enchantment_id, minion)

class TB_BaconUps_072:
    # Pillard dure écaille premium
    battlecry= lambda self: ICC_807.battlecry(self, '59509')

class BGS_030:
    # Roi Bagargouille
    def battlecry(self, enchantment_id='60393'):
        for minion in self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self):
            self.buff(enchantment_id, minion)

    def deathrattle(self, position, enchantment_id='60393'):
        for minion in self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self):
            self.buff(enchantment_id, minion, duration=1)

class TB_BaconUps_100:
    # Roi Bagargouille premium
    battlecry= lambda self: BGS_030.battlecry(self, '60397')
    deathrattle= lambda self, position: BGS_030.battlecry(self, position, '60397')

class EX1_506:
    # chasse-marée
    battlecry= lambda self: self.invoc('68469', self.position+1)

class TB_BaconUps_003:
    # chasse-marée premium
    battlecry= lambda self: self.invoc('57339', self.position+1)

class CFM_315:
    # chat de gouttière
    battlecry= lambda self: self.invoc('40425', self.position+1)

class TB_BaconUps_093:
    # chat de gouttière premium
    battlecry= lambda self: self.invoc('60054', self.position+1)

class BGS_061:
    # Forban
    def deathrattle(self, position):
        self.invoc('62213', position)

class TB_BaconUps_141:
    # Forban premium
    def deathrattle(self, position):
        self.invoc('62215', position)

class KAR_005:
    # Gentille grand-mère
    def deathrattle(self, position):
        self.invoc('39161', position)

class TB_BaconUps_004:
    # Gentille grand-mère premium
    def deathrattle(self, position):
        self.invoc('57341', position)

class EX1_556:
    # Golem des moissons
    def deathrattle(self, position):
        self.invoc('471', position)

class TB_BaconUps_006:
    # Golem des moissons premium
    def deathrattle(self, position):
        self.invoc('57408', position)

class BGS_014:
    # Emprisonneur
    def deathrattle(self, position):
        self.invoc('2779', position)

class TB_BaconUps_113:
    # Emprisonneur premium
    def deathrattle(self, position):
        self.invoc('58373', position)

class BOT_537:
    # Mecanoeuf
    def deathrattle(self, position):
        self.invoc("49168", position)

class TB_BaconUps_038e:
    # Mecanoeuf premium
    def deathrattle(self, position):
        self.invoc("58389", position)

class BGS_055:
    # Mousse du pont
    def battlecry(self):
        self.controller.bob.level_up_cost -= 1

class TB_BaconUps_126:
    # Mousse du pont premium
    def battlecry(self):
        for _ in range(2):
            BGS_055.battlecry(self)

class EX1_093:
    # Défenseur d'Argus
    def battlecry(self, enchantment_id='1103'):
        self.buff(enchantment_id, *self.adjacent_neighbors())

class TB_BaconUps_009:
    # Défenseur d'Argus premium
    battlecry= lambda self: EX1_093.battlecry(self, '57407')

class DAL_077:
    # Aileron toxique
    def battlecry(self):
        minion = self.choice_one_of_them(
            self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self)
            )
        self.buff("52297", minion)
TB_BaconUps_152= DAL_077

class LOOT_013:
    # Homoncule_sans_gene
    def battlecry(self):
        self.controller.health -= 2

class TB_BaconUps_148:
    # Homoncule_sans_gene premium
    battlecry= lambda self: LOOT_013.battlecry(self)

class CFM_816:
    # Sensei virmen
    def battlecry(self, enchantment_id='40640'):
        minion = self.controller.choose_one_of_them(
            self.my_zone.cards.filter_hex(race=Race.BEAST).exclude(self))

        self.buff(enchantment_id, minion)

class TB_BaconUps_074:
    # Sensei virmen premium
    battlecry= lambda self: CFM_816.battlecry(self, '59513')

class UNG_073:
    # Chasseur rochecave
    def battlecry(self, enchant_id='41244'):
        minion = self.choose_one_of_them(
            self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self))

        self.buff(enchant_id, minion)

class TB_BaconUps_061:
    # Chasseur rochecave premium
    battlecry= lambda x: UNG_073.battlecry(x, '59486')

class GVG_055:
    # Cliquetteur
    def battlecry(self, enchant_id='2223'):
        minion = self.choose_one_of_them(
            self.my_zone.cards.filter_hex(race=Race.MECH).exclude(self))

        self.buff(enchant_id, minion)

class TB_BaconUps_069:
    # Cliquetteur premium
    battlecry= lambda self: GVG_055.battlecry(self, '59502')

class GVG_048:
    # Bondisseur dent de métal
    def battlecry(self, enchant_id='2205'):
        minions = self.my_zone.cards.filter_hex(race=Race.MECH).exclude(self)

        self.buff(enchant_id, *minions)

class TB_BaconUps_066:
    # Bondisseur dent de métal premium
    battlecry= lambda x: GVG_048.battlecry(x, '59496')

class BT_010:
    # Navigateur gangraileron
    def battlecry(self, enchant_id='59713'):
        minions = self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self)
        self.buff(enchant_id, *minions)

class TB_BaconUps_124:
    # Navigateur gangraileron premium
    battlecry= lambda self: BT_010.battlecry(self, '61935')

class CFM_610:
    # Tisse-cristal
    def battlecry(self, enchant_id='40390'):
        minions = self.my_zone.cards.filter_hex(race=Race.DEMON).exclude(self)

        self.buff(enchant_id, *minions)

class TB_BaconUps_070:
    # Tisse-cristal premium
    battlecry= lambda self: CFM_610.battlecry(self, '59505')

class BGS_128:
    # Assistant arcanique
    def battlecry(self, enchant_id='64302'):
        minions = self.my_zone.cards.filter_hex(race=Race.ELEMENTAL).exclude(self)

        self.buff(enchant_id, *minions)

class TB_Baconups_203:
    # Assistant arcanique premium
    battlecry= lambda self: BGS_128.battlecry(self, '64304')

class BGS_053:
    # Canonnier de la voile sanglante
    def battlecry(self, enchant_id='62253'):
        minions = self.my_zone.cards.filter_hex(race=Race.PIRATE).exclude(self)

        self.buff(enchant_id, *minions)

class TB_BaconUps_138:
    # Canonnier de la voile sanglante premium
    battlecry= lambda self: BGS_053.battlecry(self, '62255')

class BGS_038:
    # Emissaire du crépuscule
    def battlecry(self, enchant_id='60627'):
        minions = self.my_zone.cards.filter_hex(race=Race.DRAGON).exclude(self)

        self.buff(enchant_id, self.choose_one_of_them(minions))

class TB_BaconUps_108:
    # Emissaire du crépuscule premium
    battlecry= lambda self: BGS_038.battlecry(self, '60666')

class EX1_103:
    # Voyant froide lumière
    def battlecry(self, enchant_id='1718'):
        minions = self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self)

        self.buff(enchant_id, *minions)

class TB_BaconUps_064:
    # Voyant froide lumière premium
    battlecry= lambda self: EX1_103.battlecry(self, '59492')

class DS1_070:
    # Maître-chien
    def battlecry(self, enchant_id='722'):
        minion = self.choose_one_of_them(
            self.my_zone.cards.filter_hex(race=Race.BEAST).exclude(self))

        self.buff(enchant_id, minion)

class TB_BaconUps_068:
    # Maître-chien premium
    battlecry= lambda self: DS1_070.battlecry(self, '59500')

class BGS_001:
    # Surveillant Nathrezim
    def battlecry(self, enchantment_id='59187'):
        minion = self.choose_one_of_them(
            self.my_zone.cards.filter_hex(race=Race.DEMON).exclude(self))

        self.buff(enchantment_id, minion)

class TB_BaconUps_062:
    # Surveillant Nathrezim premium
    battlecry= lambda self: BGS_001.battlecry(self, '59488')

class BGS_082:
    # Tasse de la ménagerie
    battlecry= lambda self: Bonus_ménagerie(self, "63488")

class TB_BaconUps_144:
    # Tasse de la ménagerie premium
    battlecry= lambda self: Bonus_ménagerie(self, "63490")

class BGS_083:
    # Théière de la ménagerie
    battlecry= lambda self: Bonus_ménagerie(self, "63491")

class TB_BaconUps_145:
    # Théière de la ménagerie premium
    battlecry= lambda self: Bonus_ménagerie(self, "63493")

def Bonus_ménagerie(self, key_effect):
    minion_list = self.owner.one_minion_by_type()
    if minion_list:
        random.shuffle(minion_list)
        self.buff(key_effect, *minion_list[:3])

class BGS_122:
    # Elementaire de stase
    def battlecry(self):
        minion_id = self.discover(
            self.controller.bob.local_hand.filter_hex(race=Race.ELEMENTAL),
            nb=1)
        if self.controller.bob.board.append(minion_id):
            minion_id.state |= State.FREEZE

class TB_BaconUps_161:
    # Elementaire de stase premium
    def battlecry(self):
        for _ in range(2):
            BGS_122.battlecry(self)

class Lapin:
    # Lapin
    def battlecry(self, enchantment_id="48470"):
        for _ in range(self.controller.nb_lapin-1):
            self.buff(enchantment_id, self)

class Lapin_p:
    # Lapin premium
    battlecry= lambda self: Lapin.battlecry(self, '59665')


##### DEATHRATTLE #####

class BGS_040:
    # Nadina
    def deathrattle(self, position):
        for minion in self.my_zone.cards.filter_hex(race=Race.DRAGON):
            minion.state |= State.DIVINE_SHIELD
TB_BaconUps_154= BGS_040

class BGS_018:
    # Goldrinn
    def deathrattle(self, position, enchantment_id='59957'):
        for minion in self.my_zone.cards.filter_hex(race=Race.BEAST):
            self.buff(enchantment_id, minion)

class TB_BaconUps_085:
    # Goldrinn premium
    deathrattle= lambda self, position: BGS_018.deathrattle(self, position, '59958')

class BGS_121:
    # Gentil djinn
    def deathrattle(self, position):
        """
        donne-t-il un elem au hasard de la taverne ou une carte elem choisie au
        hasard parmi toutes les possibilités ?
        maj 18.6 : summon que des serviteurs d'un niveau inférieur ou égal à celui de la taverne
        TODO: Gentle Djinni firstly summons an elemental, and only then puts a copy of it in hand. Therefore, if Djinni's deathrattle triggers more than once, but there is not enough space on board to summon another minion, the player will not receive a second and subsequent copy of elemental.
        : le gain ne se fait que si le repop à lieu
        """
        minions = self.controller.bob.local_hand.copy()
        random.shuffle(minions)
        for minion in minions:
            if minion.race & Race.ELEMENTAL and minion.dbfId != self.dbfId:
                if self.invoc(minion.dbfId, position):
                    self.controller.hand.append(minion)
                break

class TB_BaconUps_165:
    # Gentil djinn premium
    def deathrattle(self, position):
        for _ in range(2):
            BGS_121.deathrattle(self, position)

class TRLA_149:
    # Boagnarok
    def deathrattle(self, position):
        cards = self.game.card_can_collect.filter_hex(event=Event.DEATHRATTLE).exlude(self.dbfId)
        for _ in range(2):
            self.invoc(random.choice(cards), position)

class TB_BaconUps_057:
    # Boagnarok premium
    def deathrattle(self, position):
        for _ in range(2):
            TRLA_149.deathrattle(self, position)

class BGS_079:
    # Tranche-les-vagues
    def deathrattle(self, position):
        cards = self.game.card_can_collect.filter_hex(race=Race.PIRATE).exlude(self.dbfId)
        for _ in range(3):
            self.invoc(random.choice(cards), position)

class TB_BaconUps_137:
    # Tranche-les-vagues premium
    def deathrattle(self, position):
        for _ in range(2):
            BGS_079.deathrattle(self, position)

class BGS_006:
    # Vieux déchiqueteur de Sneed
    def deathrattle(self, position):
        cards = self.game.card_can_collect.filter(elite=True).exlude(self.dbfId)
        self.invoc(random.choice(cards), position)

class TB_BaconUps_080:
    # Vieux déchiqueteur de Sneed premium
    def deathrattle(self, position):
        for _ in range(2):
            BGS_006.deathrattle(self, position)

class BGS_080:
    # Goliath brisemer 
    def overkill(self, target, enchantment_id='62459'):
        for minion in self.my_zone.cards:
            if minion.race & Race.PIRATE and minion is not self:
                self.buff(enchantment_id, minion)

class TB_BaconUps_142:
    # Goliath brisemer premium
    overkill= lambda self, target: BGS_080.overkill(self, target, '62461')

class TRL_232:        
    # Navrecorne cuiracier
    def overkill(self, target):
        self.invoc('50359', self.position+1)

class TB_BaconUps_051:
    # Navrecorne cuiracier premium
    def overkill(self, target):
        self.invoc('60232', self.position+1)

class BGS_126:
    # Elémentaire du feu de brousse
    def overkill(self, target):
        new_target = target.adjacent_neighbors()
        if new_target:
            self.append_action(
                damage_fight,
                self,
                random.choice(new_target),
                -target.health,
                overkill=False)

class TB_BaconUps_166:
    # Elémentaire du feu de brousse premium
    def overkill(self, target):
        for new_target in target.adjacent_neighbors():
            self.append_action(
                damage_fight,
                self,
                new_target,
                -target.health,
                overkill=False)

class BGS_032:
    # Héraut de la flamme
    def overkill(self, target):
        for minion in self.my_zone.opponent:
            if minion.is_alive:
                self.append_action(
                    damage_fight,
                    self,
                    minion,
                    3)
                break

class TB_BaconUps_103:
    # Héraut de la flamme premium
    def overkill(self, target):
        for minion in self.my_zone.opponent:
            if minion.is_alive:
                self.append_action(
                    damage_fight,
                    self,
                    minion,
                    6)
                break

class BGS_044:
    # Maman des diablotins
    def hit_by(self):
        minion = random.choice(self.game.card_can_collect.filter_hex(race=Race.DEMON).exclude(self.dbfId))
        self.invoc(minion, self.position+1, enchantment_id='61393')

class TB_BaconUps_116:
    # Maman des diablotins premium
    def hit_by(self):
        for _ in range(2):
            BGS_044.hit_by(self)

class BAR_073:
    # Forgeronne des Tarides
    def hit_by(self, enchantment_id='63241'):
        if self.has_frenzy:
            self.remove_attr(state=State.FRENZY)
            for minion in self.my_zone.cards.exclude(self):
                self.buff(enchantment_id, minion)

class TB_BaconUps_320:
    # Forgeronne des Tarides premium
    hit_by= lambda self: BAR_073.hit_by(self, '71534')

class BRM_006:
    # Chef du gang des diablotins
    hit_by= lambda self: self.invoc('2779', self.position+1)

class TB_BaconUps_030:
    # Chef du gang des diablotins premium
    hit_by= lambda self: self.invoc('58373', self.position+1)

class BOT_218:
    # Rover de sécurité
    hit_by= lambda self: self.invoc("49278", self.position+1)

class TB_BaconUps_041:
    # Rover de sécurité premium
    hit_by= lambda self: self.invoc("58393", self.position+1)

class BOT_606:
    # Gro'Boum
    def deathrattle(self, position):
        self.append_action(
            damage_fight,
            self,
            self.my_zone.opponent,
            4,
            overkill=False)

class TB_BaconUps_028:
    # Gro'Boum premium
    def deathrattle(self, position):
        for _ in range(2):
            BOT_606.deathrattle(self, position)

class OG_256:
    # Rejeton de N'Zoth
    deathrattle= lambda self, position: self.buff('38796', *self.my_zone.cards)

class TB_BaconUps_025:
    # Rejeton de N'Zoth premium
    deathrattle= lambda self, position: self.buff('58169', *self.my_zone.cards)

class CFM_316:
    # Clan des rats
    def deathrattle(self, position):
        for nb in range(self.attack):
            self.invoc('41839', position+nb)

class TB_BaconUps_027:
    # Clan des rats premium
    def deathrattle(self, position):
        for nb in range(self.attack):
            self.invoc('58368', position+nb)

class OG_216:
    # Loup contaminé
    def deathrattle(self, position):
        self.invoc('38735', position)
        self.invoc('38735', position+1)

class TB_BaconUps_026:
    # Loup contaminé premium
    def deathrattle(self, position):
        self.invoc('58366', position)
        self.invoc('58366', position+1)

class EX1_534:
    # Crinière des savanes
    def deathrattle(self, position):
        for _ in range(2):
            self.invoc('1624', position)

class TB_BaconUps_049:
    # Crinière des savanes premium
    def deathrattle(self, position):
        for _ in range(2):
            self.invoc('58410', position)

class DMF_533:
    # Matrone de la piste
    def deathrattle(self, position):
        for _ in range(2):
            self.invoc('63273', position)

class TB_BaconUps_309:
    # Matrone de la piste premium
    def deathrattle(self, position):
        for _ in range(2):
            self.invoc('67729', position)

class Amalgadon_repop:
    def deathrattle(self, position):
        for _ in range(2):
            self.invoc('41067', position)

class LOOT_368:
    # Seigneur du vide
    def deathrattle(self, position):
        self.invoc("48", position)

class TB_BaconUps_059:
    # Seigneur du vide premium
    def deathrattle(self, position):
        self.invoc("57299", position)

class BOT_312:
    # Menace répliquante
    def deathrattle(self, position):
        for _ in range(3):
            self.invoc('48842', position)

class TB_BaconUps_032:
    # Menace répliquante premium
    def deathrattle(self, position):
        for _ in range(3):
            self.invoc('58377', position)

class OG_221:
    # Héroïne altruiste
    def deathrattle(self, position):
        minions = self.my_zone.cards.exclude_hex(state=State.DIVINE_SHIELD).exclude(is_alive=False)

        if minions:
            random.choice(minions).state |= State.DIVINE_SHIELD

class TB_BaconUps_014:
    # Héroïne altruiste premium
    def deathrattle(self, position):
        for _ in range(2):
            OG_221.deathrattle(self, position)

class YOD_026:
    # Serviteur diabolique
    def deathrattle(self, position):
        minions = self.my_zone.cards.filter(is_alive=True)
        if minions:
            self.buff('56113', random.choice(minions), attack=self.attack)

class TB_BaconUps_112:
    # Serviteur diabolique premium
    def deathrattle(self, position):
        for _ in range(2):
            YOD_026.deathrattle(self, position)

class FP1_024:
    # Goule instable
    def deathrattle(self, position):
        self.append_action(
            damage_fight,
            self,
            self.my_zone.opponent,
            1,
            overkill=False)
        self.append_action(
            damage_fight,
            self,
            self.my_zone,
            1,
            order=0,
            overkill=False)

class TB_BaconUps_118:
    # Goule instable premium
    def deathrattle(self, position):
        for _ in range(2):
            FP1_024.deathrattle(self, position)

class BG20_101:
    # Chauffard huran
    def hit_by(self):
        if self.has_frenzy:
            self.remove_attr(state=State.FRENZY)
            self.controller.hand.create_card_in("70136")

class BG20_101_G:
    # Chauffard huran premium
    def hit_by(self):
        if self.has_frenzy:
            self.remove_attr(state=State.FRENZY)
            self.controller.hand.create_card_in("70136", "70136")

class BG20_102:
    # Défense robuste
    def add_enchantment_on(self, enchantment, target):
        if target is self and enchantment.dbfId == CardName.BLOOD_GEM:
            self.buff('70167', self)
            self.buff('70167_x', self)

class BG20_102_G:
    # Défense robuste premium
    def add_enchantment_on(self, enchantment, target):
        if target is self and enchantment.dbfId == CardName.BLOOD_GEM:
            self.buff('70169', self)
            self.buff('70169_x', self)

class BG20_103:
    # Brute dos-hirsute
    def add_enchantment_on(self, enchantment, target):
        if target is self and enchantment.dbfId == CardName.BLOOD_GEM:
            enchantment.attack += 2
            enchantment.max_health += 2
            self.buff('92_e', self)

class BG20_103_G:
    # Brute dos-hirsute premium
    def add_enchantment_on(self, enchantment, target):
        if target is self and enchantment.dbfId == CardName.BLOOD_GEM:
            enchantment.attack += 4
            enchantment.max_health += 4
            self.buff('92_e', self)

class BG20_105:
    # Mande-épines
    def battlecry(self, position=None):
        self.controller.hand.create_card_in("70136")
    deathrattle = battlecry

class BG20_105_G:
    # Mande-épines premium
    def battlecry(self, position=None):
        for _ in range(2):
            BG20_105.battlecry(self, position)
    deathrattle = battlecry

class BG20_202:
    # Nécrolyte
    def battlecry(self):
        minion = self.choose_one_of_them(self.my_zone.cards.exclude(self))
        if minion:
            for neighbour in minion.adjacent_neighbors():
                change = False
                for enchantment in neighbour.entities[::-1]:
                    if enchantment.dbfId == CardName.BLOOD_GEM:
                        enchantment.apply(minion)
                        change = True
                if change:
                    neighbour.calc_stat_from_scratch()
            minion.calc_stat_from_scratch()

BG20_202_G= BG20_202
    
class BG20_201:
    # Porte-bannière huran
    def end_turn(self):
        for neighbour in self.adjacent_neighbors().filter_hex(race=Race.QUILBOAR):
            self.buff(CardName.BLOOD_GEM, neighbour)

class BG20_201_G:
    # Porte-bannière huran premium
    def end_turn(self):
        for _ in range(2):
            BG20_201.end_turn(self)

class BG20_104:
    # Cogneur
    def after_atk_myself(self):
        self.controller.hand.create_card_in(CardName.BLOOD_GEM)
BG20_104_G= BG20_104

class BG20_207:
    # Duo dynamique
    def add_enchantment_on(self, enchantment, target, enchantment_id='70185'):
        if target is not self and enchantment.dbfId == CardName.BLOOD_GEM and target.race & Race.QUILBOAR:
            self.buff(enchantment_id, self)

class BG20_207_G:
    # Duo dynamique premium
    add_enchantment_on= lambda self, enchantment, target: BG20_207.add_enchantment_on(self, enchantment, target, '70192')

class BG20_106:
    # Tremble-terre
    def add_enchantment_on(self, enchantment, target, enchantment_id='82_e'):
        if self is target and enchantment.dbfId == CardName.BLOOD_GEM:
            for minion in self.owner:
                if minion is not self:
                    self.buff(enchantment_id, minion)

class BG20_106_G:
    # Tremble-terre premium
    add_enchantment_on= lambda self, enchantment, target: BG20_106.add_enchantment_on(self, enchantment, target, '-82_e')

class BG20_204:
    # Chevalier dos-hirsute
    def hit_by(self):
        if self.has_frenzy:
            self.remove_attr(state=State.FRENZY)
            self.state |= State.DIVINE_SHIELD
BG20_204_G= BG20_204

class BG20_302:
    # Aggem malépine
    def add_enchantment_on(self, enchantment, target, enchantment_id='71163'):
        if self is target and enchantment.dbfId == CardName.BLOOD_GEM:
            for minion in self.my_zone.one_minion_by_type():
                self.buff(enchantment_id, minion)

class BG20_302_G:
    # Aggem malépine premium
    add_enchantment_on= lambda self, enchantment, target: BG20_302.add_enchantment_on(self, enchantment, target, '70284')

class BG20_205:
    # Agamaggan
    def play_aura(self):
        self.owner.add_aura(self, boost_blood_gem=self.double_if_premium(1))

class BG20_205_G:
    # Agamaggan premium
    def play_aura(self):
        self.owner.add_aura(self, boost_blood_gem=self.double_if_premium(1))

class BG20_303:
    # Charlga
    def end_turn(self):
        for minion in self.my_zone.cards:
            if minion is not self:
                self.buff(CardName.BLOOD_GEM, minion)

class BG20_303_G:
    # Charlga premium
    def end_turn(self):
        for _ in range(2):
            BG20_303.end_turn(self)

class BG20_206:
    # Capitaine plate défense
    def play_aura(self):
        self.owner.add_aura(self, spend_gold=1, check='Capitaine_Plate_Defense_check')

class BG20_206_G:
    # Capitaine plate défense premium
    def play_aura(self):
        self.owner.add_aura(self, spend_gold=1, check='Capitaine_Plate_Defense_check')

def Capitaine_Plate_Defense_check(self):
    while self.quest_value >= 3:
        self.quest_value -= 3
        for _ in range(self.double_if_premium(1)):
            self.owner.owner.hand.create_card_in("70136")

def wake_up(self):
    # Maeiv effect
    self.create_and_apply_enchantment('62265')
    self.owner.opponent.owner.hand.append(self)

class BG20_203:
    # Prophète du sanglier
    def after_play(self, source):
        if source.race & Race.QUILBOAR and source is not self:
            self.owner.owner.hand.create_card_in("70136")
            self.buff('90_e', self)

class BG20_203_G:
    # Prophète du sanglier premium
    def after_play(self, source):
        if source.race & Race.QUILBOAR and source is not self:
            self.owner.owner.hand.create_card_in("70136", "70136")
            self.buff('90_e', self)

class BG20_304:
    # Archidruide Amuul
    def battlecry(self):
        pass
BG20_304_G= BG20_304

class BGS_060:
    # Yo oh ogre
    pass
    """
    def Yo_oh_ogre(self):
        self.append_action_with_priority(self.prepare_attack)
    """

class TB_BaconUps_150:
    # Yo oh ogre premium
    pass

class BGS_039:
    # Lieutenant draconide
    pass

class TB_BaconUps_146:
    # Lieutenant draconide premium
    pass

class BGS_106:
    # Acolyte de C'Thun
    pass

class TB_BaconUps_255:
    # Acolyte de C'Thun premium
    pass

class VAN_EX1_506a:
    # éclaireur murloc
    pass

class TB_BaconUps_003t:
    # éclaireur murloc premium
    pass

class CFM_315t:
    # chat de gouttière
    pass

class TB_BaconUps_093t:
    # chat de gouttière premium
    pass

class BGS_061t:
    # pirate du ciel
    pass

class TB_BaconUps_141t:
    # pirate du ciel premium
    pass

class BGS_115t:
    # Goutte d'eau
    pass

class TB_BaconShop_HP_033t:
    # Amalgame
    pass

class EX1_170:
    # Cobra empereur
    pass

class EX1_554t:
    # Serpent
    pass

class KAR_005a:
    # Grand méchant loup
    pass

class TB_BaconUps_004t:
    # Grand méchant loup premium
    pass

class skele21:
    # Golem endommagé
    pass

class TB_BaconUps_006t:
    # Golem endommagé premium
    pass

class EX1_062:
    # Vieux troubloeil
    pass

class TB_BaconUps_036:
    # Vieux troubloeil premium
    pass

class BRM_006t:
    # Diablotin
    pass

class TB_BaconUps_030t:
    # Diablotin premium
    pass

class CFM_316t:
    # Rat
    pass

class TB_BaconUps_027t:
    # Rat premium
    pass

class OG_216a:
    # Araignée
    pass

class TB_BaconUps_026t:
    # Araignée premium
    pass

class BOT_312t:
    # Microbot
    pass

class TB_BaconUps_032t:
    # Microbot premium
    pass

class BGS_119:
    # Cyclone crépitant
    pass

class TB_BaconUps_159:
    # Cyclone crépitant premium
    pass

class BGS_034:
    # Gardien de bronze
    pass

class TB_BaconUps_149:
    # Gardien de bronze premium
    pass

class BOT_911:
    # Ennuy-o-module
    pass

class TB_BaconUps_099:
    # Ennuy-o-module premium
    pass

class EX1_534t:
    # Hyène
    pass

class TB_BaconUps_049t:
    # Hyène premium
    pass


class LOOT_078:
    # Hydre des cavernes
    pass

class TB_BaconUps_151:
    # Hydre des cavernes
    pass

class BOT_537t:
    # Robosaure
    pass

class TB_BaconUps_039t:
    # Robosaure premium
    pass

class BOT_218t:
    # Robot gardien
    pass

class TB_BaconUps_041t:
    # Robot gardien premium
    pass

class DMF_533t:
    # Diablotin embrasé
    pass

class TB_BaconUps_309t:
    # Diablotin embrasé premium
    pass

class TRL_232t:
    # Rejeton cuiracier
    pass

class TB_BaconUps_051t:
    # Rejeton cuiracier premium
    pass

class CS2_065:
    # Marcheur du vide
    pass

class TB_BaconUps_059t:
    # Marcheur du vide premium
    pass

class BGS_131:
    # Spore mortelle
    pass

class TB_BaconUps_251:
    # Spore mortelle premium
    pass

class GVG_113:
    # Faucheur 4000
    pass

class TB_BaconUps_153:
    # Faucheur 4000 premium
    pass

class FP1_010:
    # Maexxna
    pass

class TB_BaconUps_155:
    # Maexxna premium
    pass

class UNG_999t2t1:
    # Plante
    pass

class BGS_022:
    # Zapp Mèche-sournoise
    pass

class TB_BaconUps_091:
    # Zapp Mèche-sournoise premium
    pass

