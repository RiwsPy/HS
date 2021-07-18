# coding : utf-8

import random
from enums import Race, State, Event, CardName, Type, BATTLE_SIZE
import script_functions
from utils import *
from action import *

# habitué sans-visage (partiel)
class Murozond:
    def Murozond(self):
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
class Habitue_sans_visage:
    def Habitue_sans_visage(self, card):
        # comment se passe la gestion lors de la revente, la copie est enlevée de la taverne ou est-ce 
        # l'habitué ?
        #TODO
        key_number = card.dbfId
        if key_number[-2:] == '_p':
            key_number = key_number[:-2]
        self.set_card(key_number, copy=False)

class Habitue_sans_visage_p:
    def Habitue_sans_visage_p(self, crd):
        #TODO
        key_number = crd.dbfId
        if key_number[-2:] != '_p':
            if key_number + '_p' in self.card_db():
                key_number = key_number + '_p'

        self.set_card(key_number, copy=False)

class Nomi:
    def Nomi(self, card):
        # l'event s'active seulement après un cri de guerre, ce n'est donc pas un PLAY
        # mais un event AFTER_PLAY (nomi buff les elems générés par l'élémentaire de stase,
        # après que ce dernier soit joué)
        # enchantment_id : 64167
        if self != card and card.race & Race.ELEMENTAL:
            self.owner.owner.bonus_nomi += self.double_if_premium(1)

class Tranchetripe:
    def end_turn(self, enchantment_id='60562'):
        nb = len(self.owner.cards.filter_hex(race=Race.DRAGON))
        for _ in range(nb):
            self.buff(enchantment_id, self)

class Tranchetripe_p:
    end_turn= lambda self: Tranchetripe.end_turn(self, '60650')

class Captaine_Larrrrdeur:
    def buy(self, source):
        if source.race & Race.PIRATE:
            self.controller.gold += 1

class Captaine_Larrrrdeur_p:
    def buy(self, source):
        if source.race & Race.PIRATE:
            self.controller.gold += 2

class Devoreur_dames:
    def battlecry(self):
        minion = self.choose_one_of_them(\
            self.my_zone.cards.filter(race=Race.DEMON).exclude(self))
        if minion:
            self.controller.gold += 3
            self.buff("61080", self, attack=minion.attack, max_health=minion.health)
            self.controller.bob.hand.append(minion)

class Devoreur_dames_p:
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

class Apprentie_de_Kangor:
    def Apprentie_de_Kangor(self):
        try:
            for repop in self.mech_die[:2]:
                script_functions.invocation(self, repop, 1, self.position)
        except AttributeError:
            pass

class Apprentie_de_Kangor_p:
    def Apprentie_de_Kangor_p(self):
        try:
            for repop in self.mech_die[:4]:
                script_functions.invocation(self, repop, 1, self.position)
        except AttributeError:
            pass

class Mal_Ganis:
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = Mal_Ganis.aura
            self.apply_met_on_all_children(Mal_Ganis.aura, self.controller)

    def aura(self, target):
        if self is not target:
            if target.race & Race.DEMON:
                target.buff("2203", target, aura=True)
            elif target is self.controller:
                target.buff("-2203", target, aura=True)

class Mal_Ganis_p:
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = Mal_Ganis_p.aura
            self.apply_met_on_all_children(Mal_Ganis_p.aura, self.controller)

    def aura(self, target):
        if self is not target:
            if target.race & Race.DEMON:
                target.buff("58429", target, aura=True)
            elif target is self.controller:
                target.buff("-2203", target, aura=True)

class Brise_siege:
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = Brise_siege.aura
            self.apply_met_on_all_children(Brise_siege.aura, self.controller)

    def aura(self, target):
        if target.race & Race.DEMON and target is not self:
            self.buff('54842', target, aura=True)

class Brise_siege_p:
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = Brise_siege_p.aura
            self.apply_met_on_all_children(Brise_siege_p.aura, self.controller)

    def aura(self, target):
        if target.race & Race.DEMON and target is not self:
            self.buff('58419', target, aura=True)

class Chef_de_guerre_murloc:
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = Chef_de_guerre_murloc.aura
            self.apply_met_on_all_children(Chef_de_guerre_murloc.aura, self.controller)

    def aura(self, target):
        if target.race & Race.MURLOC and target is not self:
            self.buff('535', target, aura=True)

class Chef_de_guerre_murloc_p:
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = Chef_de_guerre_murloc_p.aura
            self.apply_met_on_all_children(Chef_de_guerre_murloc_p.aura, self.controller)

    def aura(self, target):
        if target.race & Race.MURLOC and target is not self:
            self.buff('57406', target, aura=True)

class Capitaine_des_mers:
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = Capitaine_des_mers.aura
            self.apply_met_on_all_children(Capitaine_des_mers.aura, self.controller)

    def aura(self, target):
        if target.race & Race.PIRATE and target is not self:
            self.buff('70472', target, aura=True)

class Capitaine_des_mers_p:
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = Capitaine_des_mers_p.aura
            self.apply_met_on_all_children(Capitaine_des_mers_p.aura, self.controller)

    def aura(self, target):
        if target.race & Race.PIRATE and target is not self:
            self.buff('62238', target, aura=True)

class Mythrax:
    def end_turn(self, enchantment_id='65669'):
        nb = len(self.my_zone.one_minion_by_type())
        for _ in range(nb):
            self.buff("65669", self)

class Mythrax_p:
    end_turn= lambda self: Mythrax.end_turn(self, '65672')

class Heraut_qiraji:
    def die(self, source, killer, enchantment_id='68225'):
        if source.state & State.TAUNT:
            for minion in source.adjacent_neighbors():
                self.buff(enchantment_id, minion)

class Heraut_qiraji_p:
    die= lambda self, source, killer: Heraut_qiraji.die(self, source, killer, '68226')

class Gardienne_dantan:
    def deathrattle(self, position):
        self.controller.hand.create_card_in(CardName.COIN)

class Gardienne_dantan_p:
    def deathrattle(self, position):
        for _ in range(2):
            Gardienne_dantan.deathrattle(self, position)

class Champion_dYshaarj:
    def defend_ally(self, defenser, enchantment_id='65659'):
        if defenser.state & State.TAUNT:
            self.buff(enchantment_id, self)

class Champion_dYshaarj_p:
    defend_ally= lambda self, defenser: Champion_dYshaarj.defend_ally(self, defenser, '65667')

class Bras_de_lempire:
    def defend_ally(self, defenser, enchant_id='65670'):
        if defenser.state & State.TAUNT:
            self.buff(enchant_id, defenser)

class Bras_de_lempire_p:
    defend_ally= lambda self, defenser: Bras_de_lempire.defend_ally(self, defenser, '65674')

class Ritualiste_tourmente:
    def defend_ally(self, defenser, enchant_id='66838'):
        if self is defenser:
            self.buff(enchant_id, *self.adjacent_neighbors())

class Ritualiste_tourmente_p:
    def defend_ally(self, defenser, enchant_id='66839'):
        Ritualiste_tourmente.defend_ally(self, defenser, enchant_id)

class Nat_Pagle:
    def die(self, source, killer):
        # n'est pas une découverte à 1 car peut se découvrir lui-même
        if self is source:
            lst = self.controller.bob.local_hand
            if lst:
                self.controller.hand.append(random.choice(lst))

class Nat_Pagle_p:
    def die(self, source, killer):
        for _ in range(2):
            Nat_Pagle.die(self, source, killer)

class Amiral_de_leffroi:
    def atk_ally(self, attacker, enchantment_id='62227'):
        if attacker.race & Race.PIRATE:
            for minion in self.my_zone.cards:
                self.buff(enchantment_id, minion)

class Amiral_de_leffroi_p:
    atk_ally= lambda self, attacker: Amiral_de_leffroi.atk_ally(self, attacker, '62229')

class Capitaine_Grondeventre:
    def atk_ally(self, attacker, enchantment_id='62256'):
        if attacker.race & Race.PIRATE and self is not attacker:
            self.buff(enchantment_id, attacker)

class Capitaine_Grondeventre_p:
    atk_ally= lambda self, attacker: Capitaine_Grondeventre.atk_ally(self, attacker, '62258')

def Brann(self):
    self.owner.add_aura(self, boost_battlecry=self.double_if_premium(1))

def Baron_Vaillefendre(self):
    self.owner.add_aura(self, boost_deathrattle=self.double_if_premium(1))

class Khadgar:
    def play_aura(self):
        pass

class Raflelor:
    def end_turn(self, enchantment_id='62193'):
        #TODO : partiel ?
        for minion in self.my_zone.cards:
            if hasattr(minion, 'battlegroundsNormalDbfId'):
                self.buff(enchantment_id, self)

class Raflelor_p:
    end_turn= lambda self: Raflelor.end_turn(self, '62195')

class Micromomie:
    def end_turn(self, enchantment_id='54810'):
        minions = self.owner.cards.exclude(self)
        if minions:
            self.buff(enchantment_id, random.choice(minions))

class Micromomie_p:
    end_turn = lambda self: Micromomie.end_turn(self, '64344')

class Sensei_de_fer:
    def end_turn(self, enchantment_id='2220'):
        lst = self.my_zone.cards.filter_hex(race=Race.MECH).exclude(self)
        if lst:
            self.buff(enchantment_id, random.choice(lst))

class Sensei_de_fer_p:
    end_turn= lambda self: Sensei_de_fer.end_turn(self, '58399')

class Chambellan_Executus:
    def end_turn(self, enchantment_id='65180'):
        target = self.my_zone[0]
        self.buff(enchantment_id, target)
        for _ in self.controller.played_minions[self.nb_turn].filter_hex(race=Race.ELEMENTAL):
            self.buff(enchantment_id, target)

class Chambellan_Executus_p:
    end_turn= lambda self: Chambellan_Executus.end_turn(self, '-65180')

class Maraudeur_des_ruines:
    def end_turn(self, enchantment_id='73088'):
        if len(self.owner.cards) <= 6:
            self.buff(enchantment_id, self)

class Maraudeur_des_ruines_p:
    end_turn= lambda self: Maraudeur_des_ruines.end_turn(self, '73090')

class Micro_machine:
    begin_turn = lambda x: x.buff('2_e', x)

class Micro_machine_p:
    begin_turn = lambda x: x.buff('60057', x)

class Dragon_infamelique:
    def begin_turn(self, enchantment_id='60553'):
        if self.my_zone.win_last_match:
            self.buff(enchantment_id, self)

class Dragon_infamelique_p:
    begin_turn= lambda self: Dragon_infamelique.begin_turn(self, '60646')

class Plaiedecaille_cobalt:
    def end_turn(self, enchantment_id='42441'):
        lst = self.my_zone.cards.exclude(self)
        if lst:
            self.buff(enchantment_id, random.choice(lst))

class Plaiedecaille_cobalt_p:
    end_turn= lambda self: Plaiedecaille_cobalt.end_turn(self, '61443')

class Massacreuse_croc_radieux:
    def end_turn(self, enchantment_id='59709'):
        for minion in self.owner.one_minion_by_type():
            self.buff(enchantment_id, minion)

class Massacreuse_croc_radieux_p:
    end_turn= lambda self: Massacreuse_croc_radieux.end_turn(self, '59712')

class Élémenplus:
    def sell(self, source):
        if self is source and self.controller.type == Type.HERO:
            self.controller.hand.create_card_in("64040")

class Élémenplus_p:
    def sell(self, source):
        for _ in range(2):
            Élémenplus.sell(self, source)

class Bronze_couenne:
    def sell(self, source):
        if self is source and self.controller.type == Type.HERO:
            self.controller.hand.create_card_in("70136", "70136")

class Bronze_couenne_p:
    def sell(self, source):
        for _ in range(2):
            Bronze_couenne.sell(self, source)

class Geomancien_de_Tranchebauge:
    def battlecry(self):
        self.controller.hand.create_card_in("70136")

class Geomancien_de_Tranchebauge_p:
    def battlecry(self):
        for _ in range(2):
            Geomancien_de_Tranchebauge.battlecry(self)

class Regisseur_du_temps:
    def sell(self, source, enchantment_id='60639'):
        if self is source and self.controller.type == Type.HERO:
            self.buff(enchantment_id, *self.controller.opponent.board.cards)

class Regisseur_du_temps_p:
    sell = lambda self, source: Regisseur_du_temps.sell(self, source, '60664')

class Parieuse_convaincante:
    def sell(self, source):
        if self is source and self.controller.type == Type.HERO:
            self.controller.gold += 2

class Parieuse_convaincante_p:
    def sell(self, source):
        if self is source and self.controller.type == Type.HERO:
            self.controller.gold += 5

class Bolvar_sang_de_feu:
    loss_shield= lambda self: self.buff('46580', self)

class Bolvar_sang_de_feu_p:
    loss_shield= lambda self: self.buff('58406', self)

class Massacreur_drakonide:
    loss_shield= lambda self: self.buff('61074', self)

class Massacreur_drakonide_p:
    loss_shield= lambda self: self.buff('61076', self)

class Tisse_colere:
    def after_play(self, source, enchantment_id='59671'):
        if self is not source and source.race & Race.DEMON:
            self.buff(enchantment_id, self)
            self.controller.health -= 1

class Tisse_colere_p:
    after_play= lambda self, source: Tisse_colere.after_play(self, source, '59678')

class Mande_flots_murloc:
    def invoc(self, source, enchantment_id='1719'):
        if self is not source and source.race & Race.MURLOC:
            if self.controller.fight:
                kwargs = {'duration': 1}
            else:
                kwargs = {}
            self.buff(enchantment_id, self, **kwargs)

class Mande_flots_murloc_p:
    invoc= lambda self, source: Mande_flots_murloc.invoc(self, source, '58139')

class Mini_Rag:
    def after_play(self, source, enchantment_id='64075'):
        if source.race & Race.ELEMENTAL and source is not self:
            self.buff(enchantment_id,
                random.choice(self.my_zone.cards),
                attack=source.level,
                max_health=source.level)

class Mini_Rag_p:
    def after_play(self, source, enchantment_id='64075'):
        for _ in range(2):
            Mini_Rag.after_play(self, source, enchantment_id)

class Pillard_pirate:
    def play(self, source, enchantment_id='62738'):
        if source.race & Race.PIRATE and self is not source:
            self.buff(enchantment_id, self)

class Pillard_pirate_p:
    play= lambda self, source: Pillard_pirate.play(self, source, '62740')

class Kalecgos:
    def after_play(self, source, enchantment_id='60644'):
        if self is not source and source.event & Event.BATTLECRY:
            for minion in self.my_zone.cards:
                if minion.race & Race.DRAGON:
                    self.buff(enchantment_id, minion)

class Kalecgos_p:
    after_play= lambda self, source: Kalecgos.after_play(self, source, '60668')

class Lieutenant_garr:
    def after_play(self, source, enchantment_id='64082'):
        if self is not source and source.race & Race.ELEMENTAL:
            for minion in self.my_zone.cards:
                if minion.race & Race.ELEMENTAL:
                    self.buff(enchantment_id, self)

class Lieutenant_garr_p:
    after_play= lambda self, source: Lieutenant_garr.after_play(self, source, '64083')

class Favori_de_la_foule:
    def play(self, source, enchantment_id='2750'):
        if self is not source and source.event & Event.BATTLECRY:
            self.buff(enchantment_id, self)

class Favori_de_la_foule_p:
    play= lambda self, source: Favori_de_la_foule.play(self, source, '58384')

class Saurolisque_enrage:
    def after_play(self, source, enchantment_id='62164'):
        if source.event & Event.DEATHRATTLE and source is not self:
            self.buff(enchantment_id, self)

class Saurolisque_enrage_p:
    after_play= lambda self, source: Saurolisque_enrage.after_play(self, source, '62166')

class Roche_en_fusion:
    def after_play(self, source, enchantment_id='64298'):
        if source.race & Race.ELEMENTAL and source is not self:
            self.buff(enchantment_id, self)

class Roche_en_fusion_p:
    after_play= lambda self, source: Roche_en_fusion.after_play(self, source, '64301')

class Elementaire_de_fete:
    def after_play(self, source, enchantment_id='64057'):
        if source.race & Race.ELEMENTAL and source is not self:
            minions = self.my_zone.cards.filter(race=Race.ELEMENTAL).exclude(self)
            if minions:
                self.buff(enchantment_id, random.choice(minions))

class Elementaire_de_fete_p:
    def after_play(self, source):
        for _ in range(2):
            Elementaire_de_fete.after_play(self, source)

class Demon_demesure:
    def after_play(self, source, enchantment_id='66230'):
        if self is not source and source.race & Race.DEMON:
            self.buff(enchantment_id, self)

class Demon_demesure_p:
    after_play= lambda self, source: Demon_demesure.after_play(self, source, '66238')

class Maman_ourse:
    invoc= lambda self, source: Chef_de_Meute.invoc(self, source, '60037')

class Maman_ourse_p:
    invoc= lambda self, source: Chef_de_Meute.invoc(self, source, '60039')

class Chef_de_Meute:
    def invoc(self, source, enchantment_id='59970'):
        if source.race & Race.BEAST and self is not source:
            self.buff(enchantment_id, source)

class Chef_de_Meute_p:
    invoc= lambda self, source: Chef_de_Meute.invoc(self, source, '59972')

class Gardien_des_Glyphes:
    def atk_ally(self, attacker):
        if self is attacker:
            self.buff("61030", self, attack=self.attack)

class Gardien_des_Glyphes_p:
    def atk_ally(self, attacker):
        if self is attacker:
            self.buff("61030", self, attack=self.attack*2)

class Dragonnet_rouge:
    def first_strike(self):
        nb_dragon_in_board = len(self.my_zone.cards.filter_hex(race=Race.DRAGON))

        self.append_action(
            damage_fight,
            self,
            self.my_zone.opponent,
            nb_dragon_in_board,
            overkill=False)

class Dragonnet_rouge_p:
    def first_strike(self):
        for _ in range(2):
            Dragonnet_rouge.first_strike(self)

class Ara_monstrueux:
    def after_atk_myself(self):
        minion_with_deathrattle = self.my_zone.cards.filter_hex(event=Event.DEATHRATTLE).filter(is_alive=True)

        if minion_with_deathrattle:
            target = random.choice(minion_with_deathrattle)
            target.active_local_event(Event.DEATHRATTLE, position=target.position+1)

class Ara_monstrueux_p:
    def after_atk_myself(self):
        for _ in range(2):
            Ara_monstrueux.after_atk_myself(self)

class Deflect_o_bot:
    def invoc(self, repop, enchantment_id='61931'):
        if self.controller.fight and repop.race & Race.MECH:
            self.buff(enchantment_id, self)

class Deflect_o_bot_p:
    invoc= lambda self, repop: Deflect_o_bot.invoc(self, repop, '61933')

class Jongleur_d_ame:
    def die(self, source, killer):
        if source.race & Race.DEMON:
            self.append_action(
                damage_fight,
                self,
                self.my_zone.opponent,
                3,
                overkill=False)

class Jongleur_d_ame_p:
    def die(self, source, killer):
        for _ in range(2):
            Jongleur_d_ame(self, source)

class Hyene_charognarde:
    def die(self, source, killer, enchantment_id='1633'):
        if source.owner is self.owner and source.race & Race.BEAST:
            self.buff(enchantment_id, self)

class Hyene_charognarde_p:
    die = lambda self, source, killer:\
        Hyene_charognarde.die(self, source, killer, '58396')

class Brik_a_bot:
    def die(self, source, killer, enchantment_id='2241'):
        if source.race & Race.MECH:
            self.buff(enchantment_id, self)

class Brik_a_bot_p:
    die= lambda self, source, killer: Brik_a_bot.die(self, source, killer, '58404')

class Poisson:
    def die(self, source, killer):
        if source.event & Event.DEATHRATTLE and\
            source.my_zone is self.my_zone:

            self.buff('-2_e', self, method=source.method, event=Event.DEATHRATTLE)

class Poisson_p:
    die= Poisson.die

class Trotte_bougie:
    def die(self, source, killer, enchantment_id='60560'):
        if source.race & Race.DRAGON:
            self.buff(enchantment_id, self)

class Trotte_bougie_p:
    die= lambda self, source, killer: Trotte_bougie.die(self, source, killer, '60648')

### BATTLECRY ###

class Anomalie_actualisante:
    def battlecry(self):
        if self.controller.bob.nb_free_roll < 1:
            self.controller.bob.nb_free_roll = 1

class Anomalie_actualisante_p:
    def battlecry(self):
        if self.controller.bob.nb_free_roll < 2:
            self.controller.bob.nb_free_roll = 2

class Amalgadon:
    def battlecry(self):
        nb = len(self.my_zone.one_minion_by_type())-1 # exclude self
        for _ in range(nb):
            self.add_adapt()

class Amalgadon_p:
    def battlecry(self):
        for _ in range(2):
            Amalgadon.battlecry(self)

class Guetteur_primaileron:
    def battlecry(self):
        if self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self):
            minion_id = self.discover(
                self.controller.bob.local_hand.filter_hex(race=Race.MURLOC),
                nb=3)
            self.controller.hand.append(minion_id)

class Guetteur_primaileron_p:
    def battlecry(self):
        for _ in range(2):
            Guetteur_primaileron.battlecry(self)

class Tempete_de_la_taverne:
    def battlecry(self):
        minion_id = self.discover(
            self.controller.bob.local_hand.filter_hex(race=Race.ELEMENTAL),
            nb=1)
        self.controller.hand.append(minion_id)

class Tempete_de_la_taverne_p:
    def battlecry(self):
        for _ in range(2):
            Tempete_de_la_taverne.battlecry(self)

class Maitre_de_guerre_annihileen:
    def battlecry(self, enchantment_id='59715'):
        bonus = self.controller.max_health - self.controller.health
        self.buff(enchantment_id, self, health=bonus)

class Maitre_de_guerre_annihileen_p:
    def battlecry(self):
        for _ in range(2):
            Maitre_de_guerre_annihileen.battlecry(self)

class Gaillarde_des_mers_du_sud:
    def battlecry(self, enchantment_id='62261'):
        minion = self.choose_one_of_them(self.my_zone.cards.filter_hex(race=Race.PIRATE).exclude(self))
        if minion:
            bonus = len(self.controller.bought_minions[self.nb_turn].filter_hex(race=Race.PIRATE))
            for _ in range(bonus):
                self.buff(enchantment_id, minion)

class Gaillarde_des_mers_du_sud_p:
    battlecry= lambda self: Gaillarde_des_mers_du_sud.battlecry(self, '62260')

class Pillard_dure_ecaille:
    def battlecry(self, enchantment_id="43023"):
        for minion in self.my_zone.cards.filter_hex(state=State.TAUNT):
            self.buff(enchantment_id, minion)

class Pillard_dure_ecaille_p:
    battlecry= lambda self: Pillard_dure_ecaille.battlecry(self, '59509')

class Roi_Bagargouille:
    def battlecry(self, enchantment_id='60393'):
        for minion in self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self):
            self.buff(enchantment_id, minion)

    def deathrattle(self, position, enchantment_id='60393'):
        for minion in self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self):
            self.buff(enchantment_id, minion, duration=1)

class Roi_Bagargouille_p:
    battlecry= lambda self: Roi_Bagargouille.battlecry(self, '60397')
    deathrattle= lambda self, position: Roi_Bagargouille.battlecry(self, position, '60397')

class Chasse_maree_murloc:
    battlecry= lambda self: self.invoc('68469', self.position+1)

class Chasse_maree_murloc_p:
    battlecry= lambda self: self.invoc('57339', self.position+1)

class Chat_de_gouttiere:
    battlecry= lambda self: self.invoc('40425', self.position+1)

class Chat_de_gouttiere_p:
    battlecry= lambda self: self.invoc('60054', self.position+1)

class Forban:
    def deathrattle(self, position):
        self.invoc('62213', position)

class Forban_p:
    def deathrattle(self, position):
        self.invoc('62215', position)

class Gentille_grand_mere:
    def deathrattle(self, position):
        self.invoc('39161', position)

class Gentille_grand_mere_p:
    def deathrattle(self, position):
        self.invoc('57341', position)

class Golem_des_moissons:
    def deathrattle(self, position):
        self.invoc('471', position)

class Golem_des_moissons_p:
    def deathrattle(self, position):
        self.invoc('57408', position)

class Emprisonneur:
    def deathrattle(self, position):
        self.invoc('2779', position)

class Emprisonneur_p:
    def deathrattle(self, position):
        self.invoc('58373', position)

class Mecanoeuf:
    def deathrattle(self, position):
        self.invoc("49168", position)

class Mecanoeuf_p:
    def deathrattle(self, position):
        self.invoc("58389", position)

class Mousse_du_pont:
    def battlecry(self):
        self.controller.bob.level_up_cost -= 1

class Mousse_du_pont_p:
    def battlecry(self):
        for _ in range(2):
            Mousse_du_pont.battlecry(self)

class Defenseur_d_Argus:
    def battlecry(self, enchantment_id='1103'):
        self.buff(enchantment_id, *self.adjacent_neighbors())

class Defenseur_d_Argus_p:
    battlecry= lambda self: Defenseur_d_Argus.battlecry(self, '57407')

class Aileron_toxique:
    def battlecry(self):
        minion = self.choice_one_of_them(
            self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self)
            )
        self.buff("52297", minion)

class Homoncule_sans_gene:
    def battlecry(self):
        self.controller.health -= 2

class Sensei_virmen:
    def battlecry(self, enchantment_id='40640'):
        minion = self.controller.choose_one_of_them(
            self.my_zone.cards.filter_hex(race=Race.BEAST).exclude(self))

        self.buff(enchantment_id, minion)

class Sensei_virmen_p:
    battlecry= lambda self: Sensei_virmen.battlecry(self, '59513')

class Chasseur_rochecave:
    def battlecry(self, enchant_id='41244'):
        minion = self.choose_one_of_them(
            self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self))

        self.buff(enchant_id, minion)

class Chasseur_rochecave_p:
    battlecry= lambda x: Chasseur_rochecave.battlecry(x, '59486')

class Cliquetteur:
    def battlecry(self, enchant_id='2223'):
        minion = self.choose_one_of_them(
            self.my_zone.cards.filter_hex(race=Race.MECH).exclude(self))

        self.buff(enchant_id, minion)

class Cliquetteur_p:
    battlecry= lambda self: Cliquetteur.battlecry(self, '59502')

class Bondisseur_dent_de_metal:
    def battlecry(self, enchant_id='2205'):
        minions = self.my_zone.cards.filter_hex(race=Race.MECH).exclude(self)

        self.buff(enchant_id, *minions)

class Bondisseur_dent_de_metal_p:
    battlecry= lambda x: Bondisseur_dent_de_metal.battlecry(x, '59496')

class Navigateur_gangraileron:
    def battlecry(self, enchant_id='59713'):
        minions = self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self)
        self.buff(enchant_id, *minions)

class Navigateur_gangraileron_p:
    battlecry= lambda self: Navigateur_gangraileron.battlecry(self, '61935')

class Tisse_cristal:
    def battlecry(self, enchant_id='40390'):
        minions = self.my_zone.cards.filter_hex(race=Race.DEMON).exclude(self)

        self.buff(enchant_id, *minions)

class Tisse_cristal_p:
    battlecry= lambda self: Tisse_cristal.battlecry(self, '59505')

class Assistant_arcanique:
    def battlecry(self, enchant_id='64302'):
        minions = self.my_zone.cards.filter_hex(race=Race.ELEMENTAL).exclude(self)

        self.buff(enchant_id, *minions)

class Assistant_arcanique_p:
    battlecry= lambda self: Assistant_arcanique.battlecry(self, '64304')

class Canonnier:
    def battlecry(self, enchant_id='62253'):
        minions = self.my_zone.cards.filter_hex(race=Race.PIRATE).exclude(self)

        self.buff(enchant_id, *minions)

class Canonnier_p:
    battlecry= lambda self: Canonnier.battlecry(self, '62255')

class Emissaire_du_crepuscule:
    def battlecry(self, enchant_id='60627'):
        minions = self.my_zone.cards.filter_hex(race=Race.DRAGON).exclude(self)

        self.buff(enchant_id, self.choose_one_of_them(minions))

class Emissaire_du_crepuscule_p:
    battlecry= lambda self: Emissaire_du_crepuscule.battlecry(self, '60666')

class Voyant_froide_lumiere:
    def battlecry(self, enchant_id='1718'):
        minions = self.my_zone.cards.filter_hex(race=Race.MURLOC).exclude(self)

        self.buff(enchant_id, *minions)

class Voyant_froide_lumiere_p:
    battlecry= lambda self: Voyant_froide_lumiere.battlecry(self, '59492')

class Maitre_chien:
    def battlecry(self, enchant_id='722'):
        minion = self.choose_one_of_them(
            self.my_zone.cards.filter_hex(race=Race.BEAST).exclude(self))

        self.buff(enchant_id, minion)

class Maitre_chien_p:
    battlecry= lambda self: Maitre_chien.battlecry(self, '59500')

class Surveillant_Nathrezim:
    def battlecry(self, enchantment_id='59187'):
        minion = self.choose_one_of_them(
            self.my_zone.cards.filter_hex(race=Race.DEMON).exclude(self))

        self.buff(enchantment_id, minion)

class Surveillant_Nathrezim_p:
    battlecry= lambda self: Surveillant_Nathrezim.battlecry(self, '59488')

class Menagerie_1:
    battlecry= lambda self: Bonus_ménagerie(self, "63488")

class Menagerie_1_p:
    battlecry= lambda self: Bonus_ménagerie(self, "63490")

class Menagerie_2:
    battlecry= lambda self: Bonus_ménagerie(self, "63491")

class Menagerie_2_p:
    battlecry= lambda self: Bonus_ménagerie(self, "63493")

def Bonus_ménagerie(self, key_effect):
    minion_list = self.owner.one_minion_by_type()
    if minion_list:
        random.shuffle(minion_list)
        self.buff(key_effect, *minion_list[:3])

class Elementaire_de_stase:
    def battlecry(self):
        minion_id = self.discover(
            self.controller.bob.local_hand.filter_hex(race=Race.ELEMENTAL),
            nb=1)
        if self.controller.bob.board.append(minion_id):
            minion_id.state |= State.FREEZE

class Elementaire_de_stase_p:
    def battlecry(self):
        for _ in range(2):
            Elementaire_de_stase.battlecry(self)

class Lapin:
    def battlecry(self, enchantment_id="48470"):
        for _ in range(self.controller.nb_lapin-1):
            self.buff(enchantment_id, self)

class Lapin_p:
    battlecry= lambda self: Lapin.battlecry(self, '59665')


##### DEATHRATTLE #####

class Nadina:
    def deathrattle(self, position):
        for minion in self.my_zone.cards.filter_hex(race=Race.DRAGON):
            minion.state |= State.DIVINE_SHIELD

class Goldrinn:
    def deathrattle(self, position, enchantment_id='59957'):
        for minion in self.my_zone.cards.filter_hex(race=Race.BEAST):
            self.buff(enchantment_id, minion)

class Goldrinn_p:
    deathrattle= lambda self, position: Goldrinn.deathrattle(self, position, '59958')

class Gentil_djinn:
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

class Gentil_djinn_p:
    def deathrattle(self, position):
        for _ in range(2):
            Gentil_djinn.deathrattle(self, position)

class Boagnarok:
    def deathrattle(self, position):
        cards = self.game.card_can_collect.filter_hex(event=Event.DEATHRATTLE).exlude(self.dbfId)
        for _ in range(2):
            self.invoc(random.choice(cards), position)

class Boagnarok_p:
    def deathrattle(self, position):
        for _ in range(2):
            Boagnarok.deathrattle(self, position)

class Tranche_les_vagues:
    def deathrattle(self, position):
        cards = self.game.card_can_collect.filter_hex(race=Race.PIRATE).exlude(self.dbfId)
        for _ in range(3):
            self.invoc(random.choice(cards), position)

class Tranche_les_vagues_p:
    def deathrattle(self, position):
        for _ in range(2):
            Tranche_les_vagues.deathrattle(self, position)

class Sneed:
    def deathrattle(self, position):
        cards = self.game.card_can_collect.filter(elite=True).exlude(self.dbfId)
        self.invoc(random.choice(cards), position)

class Sneed_p:
    def deathrattle(self, position):
        for _ in range(2):
            Sneed.deathrattle(self, position)

class Goliath_brisemer:
    def overkill(self, target, enchantment_id='62459'):
        for minion in self.my_zone.cards:
            if minion.race & Race.PIRATE and minion is not self:
                self.buff(enchantment_id, minion)

class Goliath_brisemer_p:
    overkill= lambda self, target: Goliath_brisemer.overkill(self, target, '62461')

class Navrecorne_cuiracier:        
    def overkill(self, target):
        self.invoc('50359', self.position+1)

class Navrecorne_cuiracier_p:
    def overkill(self, target):
        self.invoc('60232', self.position+1)

class Feu_de_brousse:
    def overkill(self, target):
        new_target = target.adjacent_neighbors()
        if new_target:
            self.append_action(
                damage_fight,
                self,
                random.choice(new_target),
                -target.health,
                overkill=False)

class Feu_de_brousse_p:
    def overkill(self, target):
        for new_target in target.adjacent_neighbors():
            self.append_action(
                damage_fight,
                self,
                new_target,
                -target.health,
                overkill=False)

class Heraut_de_la_flamme:
    def overkill(self, target):
        for minion in self.my_zone.opponent:
            if minion.is_alive:
                self.append_action(
                    damage_fight,
                    self,
                    minion,
                    3)
                break

class Heraut_de_la_flamme_p:
    def overkill(self, target):
        for minion in self.my_zone.opponent:
            if minion.is_alive:
                self.append_action(
                    damage_fight,
                    self,
                    minion,
                    6)
                break

class Maman_des_diablotins:
    def hit_by(self):
        minion = random.choice(self.game.card_can_collect.filter_hex(race=Race.DEMON).exclude(self.dbfId))
        self.invoc(minion, self.position+1, enchantment_id='61393')

class Maman_des_diablotins_p:
    def hit_by(self):
        for _ in range(2):
            Maman_des_diablotins.hit_by(self)

class Forgeronne_des_tarides:
    def hit_by(self, enchantment_id='63241'):
        if self.has_frenzy:
            self.remove_attr(state=State.FRENZY)
            for minion in self.my_zone.cards.exclude(self):
                self.buff(enchantment_id, minion)

class Forgeronne_des_tarides_p:
    hit_by= lambda self: Forgeronne_des_tarides.hit_by(self, '71534')

class Chef_du_gang_des_diablotins:
    hit_by= lambda self: self.invoc('2779', self.position+1)

class Chef_du_gang_des_diablotins_p:
    hit_by= lambda self: self.invoc('58373', self.position+1)

class Rover_de_securite:
    hit_by= lambda self: self.invoc("49278", self.position+1)

class Rover_de_securite_p:
    hit_by= lambda self: self.invoc("58393", self.position+1)

class GroBoum:
    def deathrattle(self, position):
        self.append_action(
            damage_fight,
            self,
            self.my_zone.opponent,
            4,
            overkill=False)

class Groboum_p:
    def deathrattle(self, position):
        for _ in range(2):
            GroBoum.deathrattle(self, position)

class Rejeton:
    deathrattle= lambda self, position: self.buff('38796', *self.my_zone.cards)

class Rejeton_p:
    deathrattle= lambda self, position: self.buff('58169', *self.my_zone.cards)

class Clan_des_rats:
    def deathrattle(self, position):
        for nb in range(self.attack):
            self.invoc('41839', position+nb)

class Clan_des_rats_p:
    def deathrattle(self, position):
        for nb in range(self.attack):
            self.invoc('58368', position+nb)

class Loup_contamine:
    def deathrattle(self, position):
        self.invoc('38735', position)
        self.invoc('38735', position+1)

class Loup_contamine_p:
    def deathrattle(self, position):
        self.invoc('58366', position)
        self.invoc('58366', position+1)

class Criniere_des_savanes:
    def deathrattle(self, position):
        for _ in range(2):
            self.invoc('1624', position)

class Criniere_des_savanes_p:
    def deathrattle(self, position):
        for _ in range(2):
            self.invoc('58410', position)

class Matrone_de_la_piste:
    def deathrattle(self, position):
        for _ in range(2):
            self.invoc('63273', position)

class Matrone_de_la_piste_p:
    def deathrattle(self, position):
        for _ in range(2):
            self.invoc('67729', position)

class Amalgadon_repop:
    def deathrattle(self, position):
        for _ in range(2):
            self.invoc('41067', position)

class Seigneur_du_vide:
    def deathrattle(self, position):
        self.invoc("48", position)

class Seigneur_du_vide_p:
    def deathrattle(self, position):
        self.invoc("57299", position)

class Menace_Repliquante:
    def deathrattle(self, position):
        for _ in range(3):
            self.invoc('48842', position)

class Menace_Repliquante_p:
    def deathrattle(self, position):
        for _ in range(3):
            self.invoc('58377', position)

class Héroïne_altruiste:
    def deathrattle(self, position):
        minions = self.my_zone.cards.exclude_hex(state=State.DIVINE_SHIELD).exclude(is_alive=False)

        if minions:
            random.choice(minions).state |= State.DIVINE_SHIELD

class Héroïne_altruiste_p:
    def deathrattle(self, position):
        for _ in range(2):
            Héroïne_altruiste.deathrattle(self, position)

class Serviteur_diabolique:
    def deathrattle(self, position):
        minions = self.my_zone.cards.filter(is_alive=True)
        if minions:
            self.buff('56113', random.choice(minions), attack=self.attack)

class Serviteur_diabolique_p:
    def deathrattle(self, position):
        for _ in range(2):
            Serviteur_diabolique.deathrattle(self, position)

class Goule_instable:
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

class Goule_instable_p:
    def deathrattle(self, position):
        for _ in range(2):
            Goule_instable.deathrattle(self, position)

class Chauffard_huran:
    def hit_by(self):
        if self.has_frenzy:
            self.remove_attr(state=State.FRENZY)
            self.controller.hand.create_card_in("70136")

class Chauffard_huran_p:
    def hit_by(self):
        if self.has_frenzy:
            self.remove_attr(state=State.FRENZY)
            self.controller.hand.create_card_in("70136", "70136")

class Defense_robuste:
    def add_enchantment_on(self, enchantment, target):
        if target is self and enchantment.dbfId == CardName.BLOOD_GEM:
            self.buff('70167', self)
            self.buff('70167_x', self)

class Defense_robuste_p:
    def add_enchantment_on(self, enchantment, target):
        if target is self and enchantment.dbfId == CardName.BLOOD_GEM:
            self.buff('70169', self)
            self.buff('70169_x', self)

class Brute_dos_hirsute:
    def add_enchantment_on(self, enchantment, target):
        if target is self and enchantment.dbfId == CardName.BLOOD_GEM:
            enchantment.attack += 2
            enchantment.max_health += 2
            self.buff('92_e', self)

class Brute_dos_hirsute_p:
    def add_enchantment_on(self, enchantment, target):
        if target is self and enchantment.dbfId == CardName.BLOOD_GEM:
            enchantment.attack += 4
            enchantment.max_health += 4
            self.buff('92_e', self)

class Mande_epines:
    def battlecry(self, position=None):
        self.controller.hand.create_card_in("70136")
    deathrattle = battlecry

class Mande_epines_p:
    def battlecry(self, position=None):
        for _ in range(2):
            Mande_epines.battlecry(self, position)
    deathrattle = battlecry

class Necrolyte:
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

class Porte_banniere_huran:
    def end_turn(self):
        for neighbour in self.adjacent_neighbors().filter_hex(race=Race.QUILBOAR):
            self.buff(CardName.BLOOD_GEM, neighbour)

class Porte_banniere_huran_p:
    def end_turn(self):
        for _ in range(2):
            Porte_banniere_huran.end_turn(self)

class Cogneur:
    def after_atk_myself(self):
        self.controller.hand.create_card_in(CardName.BLOOD_GEM)

class Duo_dynamique:
    def add_enchantment_on(self, enchantment, target, enchantment_id='70185'):
        if target is not self and enchantment.dbfId == CardName.BLOOD_GEM and target.race & Race.QUILBOAR:
            self.buff(enchantment_id, self)

class Duo_dynamique_p:
    add_enchantment_on= lambda self, enchantment, target: Duo_dynamique.add_enchantment_on(self, enchantment, target, '70192')

class Tremble_terre:
    def add_enchantment_on(self, enchantment, target, enchantment_id='82_e'):
        if self is target and enchantment.dbfId == CardName.BLOOD_GEM:
            for minion in self.owner:
                if minion is not self:
                    self.buff(enchantment_id, minion)

class Tremble_terre_p:
    add_enchantment_on= lambda self, enchantment, target: Tremble_terre.add_enchantment_on(self, enchantment, target, '-82_e')

class Chevalier_dos_hirsute:
    def hit_by(self):
        if self.has_frenzy:
            self.remove_attr(state=State.FRENZY)
            self.state |= State.DIVINE_SHIELD

class Aggem_malepine:
    def add_enchantment_on(self, enchantment, target, enchantment_id='71163'):
        if self is target and enchantment.dbfId == CardName.BLOOD_GEM:
            for minion in self.my_zone.one_minion_by_type():
                self.buff(enchantment_id, minion)

class Aggem_malepine_p:
    add_enchantment_on= lambda self, enchantment, target: Aggem_malepine.add_enchantment_on(self, enchantment, target, '70284')

class Agamaggan:
    def Agamaggan(self):
        self.owner.add_aura(self, boost_blood_gem=self.double_if_premium(1))

class Charlga:
    def end_turn(self):
        for minion in self.my_zone.cards:
            if minion is not self:
                self.buff(CardName.BLOOD_GEM, minion)

class Charlga_p:
    def end_turn(self):
        for _ in range(2):
            Charlga.end_turn(self)

class Capitaine_Plate_Defense:
    def Capitaine_Plate_Defense(self):
        self.owner.add_aura(self, spend_gold=1, check='Capitaine_Plate_Defense_check')

def Capitaine_Plate_Defense_check(self):
    while self.quest_value >= 3:
        self.quest_value -= 3
        for _ in range(self.double_if_premium(1)):
            self.owner.owner.hand.create_card_in("70136")

def wake_up(self):
    # Maeiv effect
    self.create_and_apply_enchantment('315_e')
    self.owner.opponent.owner.hand.append(self)

class Prophete_du_sanglier:
    def after_play(self, source):
        if source.race & Race.QUILBOAR and source is not self:
            self.owner.owner.hand.create_card_in("70136")
            self.buff('90_e', self)

class Prophete_du_sanglier_p:
    def after_play(self, source):
        if source.race & Race.QUILBOAR and source is not self:
            self.owner.owner.hand.create_card_in("70136", "70136")
            self.buff('90_e', self)

class Yo_oh_ogre:
    pass
    """
    def Yo_oh_ogre(self):
        self.append_action_with_priority(self.prepare_attack)
    """

class Lieutenant_draconide:
    pass

class Acolyte_CThun:
    pass
