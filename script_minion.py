# coding : utf-8

import random
from enums import Type, State, Event, Rarity, CardName, BATTLE_SIZE
import script_functions
from utils import *
from action import *

# habitué sans-visage (partiel)
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
def Habitue_sans_visage(self, card):
    # comment se passe la gestion lors de la revente, la copie est enlevée de la taverne ou est-ce 
    # l'habitué ?
    #TODO
    key_number = card.dbfId
    if key_number[-2:] == '_p':
        key_number = key_number[:-2]
    self.set_card(key_number, copy=False)

def Habitue_sans_visage_p(self, crd):
    #TODO
    key_number = crd.dbfId
    if key_number[-2:] != '_p':
        if key_number + '_p' in self.card_db():
            key_number = key_number + '_p'

    self.set_card(key_number, copy=False)

def Nomi(self, card):
    if self != card and card.type & Type.ELEMENTAL:
        self.owner.owner.bonus_nomi += self.double_if_premium(1)

def Tranchetripe(self):
    nb = 0
    for minion in self.owner:
        if minion.type & Type.DRAGON:
            nb += 1
    self.create_and_apply_enchantment("16_e", is_premium=self.is_premium, nb=nb)

def Captaine_Larrrrdeur(self, card):
    if card.type & Type.PIRATE:
        self.owner.owner.gold += self.double_if_premium(1)

class Devoreur_dames:
    def battlecry(self):
        minion = self.choose_one_of_them(\
            self.my_zone.cards.filter(type=Type.DEMON).exclude(self))
        if minion:
            self.controller.gold += 3
            self.buff("61080", self, attack=minion.attack, max_health=minion.health)
            self.controller.bob.hand.append(minion)

class Devoreur_dames_p:
    def battlecry(self):
        minion = self.choose_one_of_them(\
            self.my_zone.cards.filter(type=Type.DEMON).exclude(self))
        if minion:
            self.controller.gold += 6
            self.buff("61080", self, attack=minion.attack*2, max_health=minion.health*2)
            self.controller.bob.hand.append(minion)

def Apprentie_reinit(self):
    self.mech_die = []

def Apprentie_kill(self, victim):
    if victim.type & Type.MECH:
        try:
            self.mech_die.append(victim.dbfId)
        except AttributeError:
            pass

def Apprentie_de_Kangor(self):
    try:
        for repop in self.mech_die[:2]:
            script_functions.invocation(self, repop, 1, self.position)
    except AttributeError:
        pass

def Apprentie_de_Kangor_p(self):
    try:
        for repop in self.mech_die[:4]:
            script_functions.invocation(self, repop, 1, self.position)
    except AttributeError:
        pass

def Mal_Ganis_a(self):
    self.owner.add_aura(self, insensible=1, method='Mal_Ganis')

def Mal_Ganis(self, target):
    if self != target and target.type & Type.DEMON:
        target.create_and_apply_enchantment("78_e", is_premium=self.is_premium, origin=self, type='aura')

def Brise_siege_a(self):
    self.owner.add_aura(self, attack=self.double_if_premium(1), restr_type=Type.DEMON)

class Chef_de_guerre_murloc:
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = Chef_de_guerre_murloc.aura
            self.apply_met_on_all_children(Chef_de_guerre_murloc.aura, self.controller)

    def aura(self, target):
        if target.type & Type.MURLOC and target is not self:
            self.buff('535', target, aura=True)

class Chef_de_guerre_murloc_p:
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = Chef_de_guerre_murloc_p.aura
            self.apply_met_on_all_children(Chef_de_guerre_murloc_p.aura, self.controller)

    def aura(self, target):
        if target.type & Type.MURLOC and target is not self:
            self.buff('57406', target, aura=True)

class Capitaine_des_mers:
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = Capitaine_des_mers.aura
            self.apply_met_on_all_children(Capitaine_des_mers.aura, self.controller)

    def aura(self, target):
        if target.type & Type.PIRATE and target is not self:
            self.buff('70472', target, aura=True)

class Capitaine_des_mers_p:
    def play_aura(self):
        if self not in self.controller.aura_active:
            self.controller.aura_active[self] = Capitaine_des_mers_p.aura
            self.apply_met_on_all_children(Capitaine_des_mers_p.aura, self.controller)

    def aura(self, target):
        if target.type & Type.PIRATE and target is not self:
            self.buff('62238', target, aura=True)

def Mythrax(self):
    self.create_and_apply_enchantment(
        "17_e",
        is_premium=self.is_premium,
        nb=len(self.owner.one_minion_by_type()))

def Heraut_qiraji(self, victim):
    if victim.state & State.TAUNT:
        for minion in victim.adjacent_neighbors():
            minion.create_and_apply_enchantment("18_e", is_premium=self.is_premium)

class Gardienne_dantan:
    def deathrattle(self, position):
        self.controller.hand.create_card_in('1001')

class Gardienne_dantan_p:
    def deathrattle(self, position):
        for _ in range(2):
            Gardienne_dantan.deathrattle(self, position)

def Champion_dYshaarj(self, ally):
    if ally.state & State.TAUNT:
        self.create_and_apply_enchantment("19_e", is_premium=self.is_premium)

class Bras_de_lempire:
    def defend_ally(self, ally, enchant_id='65670'):
        if ally.state & State.TAUNT:
            self.buff(enchant_id, ally)

class Bras_de_lempire_p:
    defend_ally= lambda self, ally: Bras_de_lempire.defend_ally(self, ally, '65674')

class Ritualiste_tourmente:
    def defend_ally(self, defenser, enchant_id='66838'):
        if self is defenser:
            self.buff(enchant_id, *self.adjacent_neighbors())

class Ritualiste_tourmente_p:
    def defend_ally(self, defenser, enchant_id='66839'):
        Ritualiste_tourmente.defend_ally(self, defenser, enchant_id)

def Nat_Pagle(self, attacker, victim):
    # n'est pas une découverte à 1 car peut se découvrir lui-même
    if self is attacker:
        for _ in range(self.double_if_premium(1)):
            lst = self.bob.local_hand
            if lst:
                card = random.choice(lst)
                self.owner.owner.hand.append(card)

def Amiral_de_leffroi(self, attacker):
    if attacker.type & Type.PIRATE:
        for minion in self.owner:
            minion.create_and_apply_enchantment("22_e", is_premium=self.is_premium)

def Capitaine_Grondeventre(self, attacker):
    if attacker.type & Type.PIRATE and self != attacker:
        attacker.create_and_apply_enchantment("23_e", is_premium=self.is_premium)

def Brann(self):
    self.owner.add_aura(self, boost_battlecry=self.double_if_premium(1))

def Baron_Vaillefendre(self):
    self.owner.add_aura(self, boost_deathrattle=self.double_if_premium(1))

class Khadgar:
    def play_aura(self):
        pass

def Raflelor(self):
    self.create_and_apply_enchantment("1_e", is_premium=self.is_premium, nb=self.owner.nb_premium_card())

class Micromomie:
    def end_turn(self, enchantment_id='54810'):
        minions = self.owner.cards.exclude(self)
        if minions:
            self.buff(enchantment_id, random.choice(minions))

class Micromomie_p:
    end_turn = lambda self: Micromomie.end_turn(self, '64344')

def Sensei_de_fer(self):
    Boost_other(self, "88_e", type=Type.MECH, nb_max=1)

def Chambellan_Executus(self):
    nb = 0
    for minion in self.controller.played_minions[self.nb_turn]:
        if minion.type & Type.ELEMENTAL:
            nb += 1
    self.owner[0].create_and_apply_enchantment("25_e", is_premium=self.is_premium, nb=nb)

def Maraudeur_des_ruines(self):
    if len(self.owner.cards) <= 6:
        self.buff('91_e', self)

def Maraudeur_des_ruines_p(self):
    if len(self.owner.cards) <= 6:
        self.buff('91p_e', self)

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

def Plaiedecaille_cobalt(self):
    Boost_other(self, "26_e", nb_max=1)

def Massacreuse_croc_radieux(self):
    for minion in self.owner.one_minion_by_type():
        minion.create_and_apply_enchantment("27_e", is_premium=self.is_premium)

class Élémenplus:
    def sell(self, source):
        if self is source and self.controller.general == General.HERO:
            self.controller.hand.create_card_in("64040")

class Élémenplus_p:
    def sell(self, source):
        for _ in range(2):
            Élémenplus.sell(self, source)

class Bronze_couenne:
    def sell(self, source):
        if self is source and self.controller.general == General.HERO:
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
        if self is source and self.controller.general == General.HERO:
            self.buff(enchantment_id, *self.controller.opponent.board.cards)

class Regisseur_du_temps_p:
    sell = lambda self, source: Regisseur_du_temps.sell(self, source, '60664')

class Parieuse_convaincante:
    def sell(self, source):
        if self is source and self.controller.general == General.HERO:
            self.controller.gold += 2

class Parieuse_convaincante_p:
    def sell(self, source):
        if self is source and self.controller.general == General.HERO:
            self.controller.gold += 5

def Bolvar_sang_de_feu(self):
    self.create_and_apply_enchantment("29_e", is_premium=self.is_premium)

def Massacreur_drakonide(self):
    self.create_and_apply_enchantment("30_e", is_premium=self.is_premium)

class Tisse_colere:
    def play(self, source, enchantment_id='59671'):
        if self != source and source.type & Type.DEMON:
            self.buff(enchantment_id, self)
            self.controller.health -= 1

class Tisse_colere_p:
    play = lambda self, source: Tisse_colere.play(self, source, '59678')

class Mande_flots_murloc:
    def invoc(self, source, enchantment_id='1719'):
        if self is not source and source.type & Type.MURLOC:
            if self.controller.fight:
                kwargs = {'duration': 1}
            else:
                kwargs = {}
            self.buff(enchantment_id, self, **kwargs)

class Mande_flots_murloc_p:
    invoc = lambda self, source: Mande_flots_murloc.invoc(self, source, '58139')

def Guetteur_Flottant(self):
    self.create_and_apply_enchantment("11_e", is_premium=self.is_premium)

def Mini_Rag(self, invoc):
    if invoc.is_type(Type.ELEMENTAL) and invoc != self:
        for _ in range(self.double_if_premium(1)):
            random.choice(self.owner).create_and_apply_enchantment(
                "31_e",
                is_premium=False,
                a=invoc.level,
                h=invoc.level)

class Pillard_pirate:
    def play(self, invoc, enchantment_id='62738'):
        if invoc.type & Type.PIRATE:
            self.buff(enchantment_id, self)

class Pillard_pirate_p:
    play= lambda self, invoc: Pillard_pirate.play(self, invoc, '62740')

def Kalecgos(self, invoc):
    if self != invoc and invoc.event & Event.BATTLECRY:
        Boost_all(self, "33_e", typ=Type.DRAGON)

def Lieutenant_garr(self, invoc):
    if self != invoc and invoc.is_type(Type.ELEMENTAL):
        bonus = 0
        for minion in self.owner:
            if minion.is_type(Type.ELEMENTAL):
                bonus += 1
        self.create_and_apply_enchantment("7_e", is_premium=self.is_premium, h=bonus)

def Favori_de_la_foule(self, invoc):
    if self != invoc and invoc.event & Event.BATTLECRY:
        self.create_and_apply_enchantment("8_e", is_premium=self.is_premium)

class Saurolisque_enrage:
    def play(self, source, enchantment_id='62164'):
        if source.event & Event.DEATHRATTLE and source is not self:
            self.buff(enchantment_id, self)

class Saurolisque_enrage_p:
    play = lambda self, source: Saurolisque_enrage.play(self, source, '62166')

class Roche_en_fusion:
    def play(self, source, enchantment_id='64298'):
        if source.type & Type.ELEMENTAL and source is not self:
            self.buff(enchantment_id, self)

class Roche_en_fusion_p:
    play = lambda self, source: Roche_en_fusion.play(self, source, '64301')

class Elementaire_de_fete:
    def play(self, source, enchantment_id='64057'):
        if source.type & Type.ELEMENTAL and source is not self:
            minions = self.owner.cards.filter(type=Type.ELEMENTAL).exclude(self)
            if minions:
                self.buff(enchantment_id, random.choice(minions))

class Elementaire_de_fete_p:
    def play(self, source):
        for _ in range(2):
            Elementaire_de_fete.play(self, source)

def Demon_demesure(self, target):
    if self != target and target.type & Type.DEMON:
        self.create_and_apply_enchantment("35_e", is_premium=self.is_premium)

def Maman_ourse(self, target):
    if self != target and target.type & Type.BEAST:
        target.create_and_apply_enchantment("36_e", is_premium=self.is_premium)

class Chef_de_Meute:
    def invoc(self, source, enchantment_id='59970'):
        if source.type & Type.BEAST and self is not source:
            self.buff(enchantment_id, source)

class Chef_de_Meute_p:
    invoc = lambda self, source: Chef_de_Meute.invoc(self, source, '59972')

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
        nb_dragon_in_board = len(self.my_zone.cards.filter_hex(type=Type.DRAGON))

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
        if self.controller.fight and repop.type & Type.MECH:
            self.buff(enchantment_id, self)

class Deflect_o_bot_p:
    invoc= lambda self, repop: Deflect_o_bot.invoc(self, repop, '61933')

class Jongleur_d_ame:
    def die(self, victim):
        if victim.type & Type.DEMON:
            self.append_action(
                damage_fight,
                self,
                self.my_zone.opponent,
                3,
                overkill=False)

class Jongleur_d_ame_p:
    def die(self, victim):
        for _ in range(2):
            Jongleur_d_ame(self, victim)

class Hyene_charognarde:
    def die(self, source, killer, enchantment_id='1633'):
        if source.owner is self.owner and source.type & Type.BEAST:
            self.buff(enchantment_id, self)

class Hyene_charognarde_p:
    die = lambda self, source, killer:\
        Hyene_charognarde.die(self, source, killer, '58396')

def Charognard2_2(self, victim):
    if self.are_same_type(victim):
        self.create_and_apply_enchantment("41_e", is_premium=self.is_premium)

class Poisson:
    def die(self, source, killer):
        if source.event & Event.DEATHRATTLE and\
            source.my_zone is self.my_zone:

            self.buff('-2_e', self, method=source.method, event=Event.DEATHRATTLE)

class Poisson_p:
    die = Poisson.die

class Trotte_bougie:
    def die(self, source, killer, enchantment_id='60560'):
        if source.type & Type.DRAGON:
            self.buff(enchantment_id, self)

class Trotte_bougie_p:
    die = lambda self, source, killer: Trotte_bougie.die(self, source, killer, '60648')

### BATTLECRY ###

class Anomalie_actualisante:
    def battlecry(self):
        if self.controller.bob.nb_free_roll < 1:
            self.controller.bob.nb_free_roll = 1

class Anomalie_actualisante_p:
    def battlecry(self):
        if self.controller.bob.nb_free_roll < 2:
            self.controller.bob.nb_free_roll = 2

def Amalgadon(self):
    type_cumul = 0
    nb_adapt = 0
    for servant in self.owner:
        if servant != self and servant.type and (not servant.type & type_cumul\
                or servant.type == Type.ALL):
            nb_adapt += 1
            if servant.type != Type.ALL:
                type_cumul |= servant.type

    nb_adapt *= self.double_if_premium(1)
    for _ in range(nb_adapt):
        adapt_spell(self)

def adapt_spell(self, nb=0):
    if not nb:
        nb = random.randint(1, 8)

    if 1 <= nb <= 8:
        self.create_and_apply_enchantment(str(42+nb) + '_e')
    else:
        print(f"Amalgadon adapt error n°{nb}")

def Guetteur_primaileron(self):
    for minion in self.owner:
        if minion != self and minion.is_type(Type.MURLOC):
            self.owner.owner.discover(self, nb=3, typ=Type.MURLOC)
            break

def Guetteur_primaileron_p(self):
    for minion in self.owner:
        if minion != self and minion.is_type(Type.MURLOC):
            self.owner.owner.discover(self, nb=3, typ=Type.MURLOC)
            self.owner.owner.discover(self, nb=3, typ=Type.MURLOC)
            break

def Tempete_de_la_taverne(self):
    self.owner.owner.discover(self, nb=1, typ=Type.ELEMENTAL)

def Tempete_de_la_taverne_p(self):
    self.owner.owner.discover(self, nb=1, typ=Type.ELEMENTAL)
    self.owner.owner.discover(self, nb=1, typ=Type.ELEMENTAL)

def Maitre_de_guerre_annihileen(self):
    health = self.owner.owner.dbfId.health - self.owner.owner.health
    self.create_and_apply_enchantment("12_e", is_premium=self.is_premium, h=health)

def Gaillarde_des_mers_du_sud(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=Type.PIRATE)
    if minion:
        bonus = 0
        for minion in self.owner.owner.minion_buy_this_turn:
            if minion.type & Type.PIRATE:
                bonus += 1
        minion.create_and_apply_enchantment("87_e", is_premium=self.is_premium, nb=bonus)

def Pillard_dure_ecaille(self):
    for minion in self.owner:
        if minion.state & State.TAUNT:
            minion.create_and_apply_enchantment("13_e", is_premium=self.is_premium)

def Roi_Bagargouille(self):
    Boost_other(self, "51_e", type=Type.MURLOC, is_premium=self.is_premium)

def Roi_Bagargouille_death(self):
    Boost_other(self, "52_e", type=Type.MURLOC, is_premium=False)

def Roi_Bagargouille_death_p(self):
    Boost_other(self, "52_e", type=Type.MURLOC, is_premium=True)

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

def Mecanoeuf(self):
    script_functions.invocation(self, "408a", 1, self.position)

def Mecanoeuf_p(self):
    script_functions.invocation(self, "408a_p", 1, self.position)

class Mousse_du_pont:
    def battlecry(self):
        self.controller.bob.level_up_cost -= 1

class Mousse_du_pont_p:
    def battlecry(self):
        for _ in range(2):
            Mousse_du_pont.battlecry(self)

def Defenseur_d_Argus(self):
    targets = [self.owner[self.position - 1], self.owner[self.position + 1]]

    for target in targets:
        if target:
            target.create_and_apply_enchantment("53_e", is_premium=self.is_premium)

class Aileron_toxique:
    def battlecry(self):
        minion = self.choice_one_of_them(
            self.my_zone.cards.filter_hex(type=Type.MURLOC).exclude(self)
            )
        self.buff("52297", minion)

class Homoncule_sans_gene:
    def battlecry(self):
        self.controller.health -= 2

def Sensei_virmen(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=Type.BEAST)
    if minion:
        minion.create_and_apply_enchantment("55_e", is_premium=self.is_premium)

class Chasseur_rochecave:
    def battlecry(self, enchant_id='41244'):
        minion = self.choose_one_of_them(
            self.my_zone.cards.filter_hex(type=Type.MURLOC).exclude(self))

        self.buff(enchant_id, minion)

class Chasseur_rochecave_p:
    battlecry = lambda x: Chasseur_rochecave.battlecry(x, '59486')

class Cliquetteur:
    def battlecry(self, enchant_id='2223'):
        minion = self.choose_one_of_them(
            self.my_zone.cards.filter_hex(type=Type.MECH).exclude(self))

        self.buff(enchant_id, minion)

class Cliquetteur_p:
    battlecry = lambda self: Cliquetteur.battlecry(self, '59502')

class Bondisseur_dent_de_metal:
    def battlecry(self, enchant_id='2205'):
        minions = self.my_zone.cards.filter_hex(type=Type.MECH).exclude(self)
        self.buff(enchant_id, *minions)

class Bondisseur_dent_de_metal_p:
    battlecry = lambda x: Bondisseur_dent_de_metal.battlecry(x, '59496')

class Navigateur_gangraileron:
    def battlecry(self, enchant_id='59713'):
        minions = self.my_zone.cards.filter_hex(type=Type.MURLOC).exclude(self)
        self.buff(enchant_id, *minions)

class Navigateur_gangraileron_p:
    battlecry= lambda self: Navigateur_gangraileron.battlecry(self, '61935')

class Tisse_cristal:
    def battlecry(self, enchant_id='40390'):
        minions = self.my_zone.cards.filter_hex(type=Type.DEMON).exclude(self)
        self.buff(enchant_id, *minions)

class Tisse_cristal_p:
    battlecry= lambda self: Tisse_cristal.battlecry(self, '59505')

class Assistant_arcanique:
    def battlecry(self, enchant_id='64302'):
        minions = self.my_zone.cards.filter_hex(type=Type.ELEMENTAL).exclude(self)
        self.buff(enchant_id, *minions)

class Assistant_arcanique_p:
    battlecry= lambda self: Assistant_arcanique.battlecry(self, '64304')

class Canonnier:
    def battlecry(self, enchant_id='62253'):
        minions = self.my_zone.cards.filter_hex(type=Type.PIRATE).exclude(self)
        self.buff(enchant_id, *minions)

class Canonnier_p:
    battlecry= lambda self: Canonnier.battlecry(self, '62255')

class Emissaire_du_crepuscule:
    def battlecry(self, enchant_id='60627'):
        minions = self.my_zone.cards.filter_hex(type=Type.DRAGON).exclude(self)
        self.buff(enchant_id, self.choose_one_of_them(minions))

class Emissaire_du_crepuscule_p:
    battlecry= lambda self: Emissaire_du_crepuscule.battlecry(self, '60666')

class Voyant_froide_lumiere:
    def battlecry(self, enchant_id='1718'):
        minions = self.my_zone.cards.filter_hex(type=Type.MURLOC).exclude(self)
        self.buff(enchant_id, *minions)

class Voyant_froide_lumiere_p:
    battlecry= lambda self: Voyant_froide_lumiere.battlecry(self, '59492')

class Maitre_chien:
    def battlecry(self, enchant_id='722'):
        minion = self.choose_one_of_them(
            self.my_zone.cards.filter_hex(type=Type.BEAST).exclude(self))

        self.buff(enchant_id, minion)

class Maitre_chien_p:
    battlecry= lambda self: Maitre_chien.battlecry(self, '59500')

class Surveillant_Nathrezim:
    def battlecry(self, enchantment_id='59187'):
        minion = self.choose_one_of_them(
            self.my_zone.cards.filter_hex(type=Type.DEMON).exclude(self))

        self.buff(enchantment_id, minion)

class Surveillant_Nathrezim_p:
    battlecry = lambda self: Surveillant_Nathrezim.battlecry(self, '59488')

class Menagerie_1:
    battlecry: lambda self: Bonus_ménagerie(self, "63488")

class Menagerie_1_p:
    battlecry: lambda self: Bonus_ménagerie(self, "63490")

def Menagerie_2(self):
    Bonus_ménagerie(self, "68_e")

class Elementaire_de_stase:
    def battlecry(self):
        elem_lst = self.controller.bob.local_hand.filter_hex(type=Type.ELEMENTAL).exlude(dbfId=self.dbfId)
        if elem_lst:
            elem = random.choice(elem_lst)
            if self.my_zone.opponent.create_card_in(elem):
                elem.state |= State.FREEZE

class Elementaire_de_stase_p:
    def battlecry(self):
        for _ in range(2):
            Elementaire_de_stase.battlecry(self)

def Bonus_ménagerie(self, key_effect):
    minion_list = self.owner.one_minion_by_type()
    if minion_list:
        random.shuffle(minion_list)
        self.buff(key_effect, *minion_list[:3])

def Lapin(self):
    self.create_and_apply_enchantment("69_e", is_premium=self.is_premium, nb=self.owner.owner.nb_lapin)

def Boost_other(self, effect_key, type=Type.ALL, nb_max=BATTLE_SIZE, is_premium=None):
    board = [minion
        for minion in self.owner
            if minion.is_type(type) and minion != self]

    if is_premium is None:
        is_premium = self.is_premium
    random_target = None
    while board and nb_max:
        random_target = random.choice(board)
        random_target.create_and_apply_enchantment(effect_key, is_premium=is_premium)
        board.remove(random_target)
        nb_max -= 1

    return random_target

def Boost_all(self, effect_key, typ=None, is_premium=None):
    if is_premium is None:
        is_premium = self.is_premium
    for minion in self.owner:
        if typ is None or minion.is_type(typ):
            minion.create_and_apply_enchantment(effect_key, is_premium=is_premium)

##### DEATHRATTLE #####


def Nadina(self):
    for minion in self.owner:
        if minion.type & Type.DRAGON:
            minion.state |= State.DIVINE_SHIELD

def Goldrinn(self):
    Boost_all(self, "70_e", Type.BEAST, is_premium=False)

def Goldrinn_p(self):
    Boost_all(self, "70_e", Type.BEAST, is_premium=True)

def Gentil_djinn(self):
    """ donne-t-il un elem au hasard de la taverne ou une carte elem choisie au
    hasard parmi toutes les possibilités ?
    maj 18.6 : summon que des serviteurs d'un niveau inférieur ou égal à celui de la taverne
    """
    cards = self.bob.hand.cards_type_of_tier_max(
            tier_max=self.owner.owner.level, typ=Type.ELEMENTAL)

    if cards:
        card = random.choice(cards)
        cards.remove(card)
        if card.dbfId != self.dbfId:
            script_functions.invocation(self, card.dbfId,
                nb_max=1, position=self.position)
            self.owner.owner.hand.append(card)
    else:
        print(f'{self.name} bob hand empty')

def Gentil_djinn_p(self):
    """ donne-t-il un elem au hasard de la taverne ou une carte elem choisie au
    hasard parmi toutes les possibilités ?
    maj 18.6 : summon que des serviteurs d'un niveau inférieur ou égal à celui de la taverne
    """
    cards = self.bob.hand.cards_type_of_tier_max(
            tier_max=self.owner.owner.level, typ=Type.ELEMENTAL)

    for _ in range(2):
        if cards:
            card = random.choice(cards)
            cards.remove(card)
            if card.dbfId != self.dbfId:
                script_functions.invocation(self, card.dbfId,
                    nb_max=1, position=self.position)
                self.owner.owner.hand.append(card)
        else:
            print(f'{self.name} bob hand empty')
            break

def Boagnarok(self):
    cards = self.bob.card_can_collect
    rale_cards = [key
        for key, value in cards.items()
            if Event.DEATHRATTLE in value["script"]]

    script_functions.invocation_random_list(self, rale_cards, 2)

def Boagnarok_p(self):
    cards = self.bob.card_can_collect
    rale_cards = [key
        for key, value in cards.items()
            if Event.DEATHRATTLE in value["script"]]

    script_functions.invocation_random_list(self, rale_cards, 4)

def Tranche_les_vagues(self):
    pirate_cards = [key
        for key, value in self.bob.card_can_collect.items()
            if value["type"] & Type.PIRATE]

    script_functions.invocation_random_list(self, pirate_cards, 3)

def Tranche_les_vagues_p(self):
    pirate_cards = [key
        for key, value in self.bob.card_can_collect.items()
            if value["type"] & Type.PIRATE]

    script_functions.invocation_random_list(self, pirate_cards, 6)

def Sneed(self):
    legendary_cards = [key
        for key, value in self.bob.card_can_collect.items()
            if value['rarity'] == Rarity.LEGENDARY]

    script_functions.invocation_random_list(self, legendary_cards, 1)

def Sneed_p(self):
    legendary_cards = [key
        for key, value in self.bob.card_can_collect.items()
            if value['rarity'] == Rarity.LEGENDARY]

    script_functions.invocation_random_list(self, legendary_cards, 2)

def Goliath_brisemer(self, target):
    Boost_other(self, "71_e", type=Type.PIRATE, is_premium=self.is_premium)

def Navrecorne_cuiracier(self, target):
    script_functions.invocation(self, "504a", 1, self.position)

def Navrecorne_cuiracier_p(self, target):
    script_functions.invocation(self, "504a_p", 1, self.position)

def Feu_de_brousse(self, target):
    new_target = target.adjacent_neighbors()
    if new_target:
        self.owner.owner.fight.take_damage(
                self,
                random.choice(new_target),
                -target.health,
                overkill=False)

def Feu_de_brousse_p(self, target):
    for new_target in target.adjacent_neighbors():
        self.owner.owner.fight.take_damage(
                self,
                new_target,
                -target.health,
                overkill=False)

def Heraut_de_la_flamme(self, target):
    if self.owner.opponent:
        damage = 3*self.double_if_premium(1)
        for minion in self.owner.opponent:
            if minion.is_alive:
                self.owner.owner.fight.take_damage(self, minion, damage)
                break

def Maman_des_diablotins(self):
    demon_cards = [key
        for key, value in self.bob.card_can_collect.items()
            if value["type"] & Type.DEMON]

    for _ in range(self.double_if_premium(1)):
        repop_id = script_functions.invocation_random_list(self, demon_cards, 1)
        if repop_id:
            repop_id.create_and_apply_enchantment('89_e')

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

def Rover_de_securite(self):
    script_functions.invocation(self, "410a", 1)

def Rover_de_securite_p(self):
    script_functions.invocation(self, "410a_p", 1)

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

def Criniere_des_savanes(self):
    script_functions.invocation(self, "405a", 2, self.position)

def Criniere_des_savanes_p(self):
    script_functions.invocation(self, "405a_p", 2, self.position)

def Matrone_de_la_piste(self):
    script_functions.invocation(self, "427a", 2, self.position)

def Matrone_de_la_piste_p(self):
    script_functions.invocation(self, "427a_p", 2, self.position)

def Amalgadon_repop(self):
    script_functions.invocation(self, "602a", 2, self.position)

def Seigneur_du_vide(self):
    script_functions.invocation(self, "506a", 3, self.position)

def Seigneur_du_vide_p(self):
    script_functions.invocation(self, "506a_p", 3, self.position)

class Menace_Repliquante:
    def deathrattle(self, position):
        self.invoc('48842', position)
        self.invoc('48842', position+1)
        self.invoc('48842', position+2)

class Menace_Repliquante_p:
    def deathrattle(self, position):
        self.invoc('58377', position)
        self.invoc('58377', position+1)
        self.invoc('58377', position+2)

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
    def play(self, enchantment, target):
        if target is self and enchantment.dbfId == CardName.BLOOD_GEM:
            enchantment.attack += 2
            enchantment.max_health += 2
            self.buff('92_e', self)

class Brute_dos_hirsute_p:
    def play(self, enchantment, target):
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
        for neighbour in self.adjacent_neighbors().filter_hex(type=Type.QUILBOAR):
            self.buff(CardName.BLOOD_GEM, neighbour)

class Porte_banniere_huran_p:
    def end_turn(self):
        for _ in range(2):
            Porte_banniere_huran.end_turn(self)

def Cogneur(self):
    self.owner.owner.hand.create_card_in("70136")

def Duo_dynamique(self, enchantment, target):
    if target != self and enchantment.dbfId == CardName.BLOOD_GEM and target.type & Type.QUILBOAR:
        self.create_and_apply_enchantment('81_e', is_premium=self.is_premium)

def Tremble_terre(self, enchantment, target):
    if self is target and enchantment.dbfId == CardName.BLOOD_GEM:
        for minion in self.owner:
            minion.create_and_apply_enchantment('82_e', is_premium=self.is_premium)

def Chevalier_dos_hirsute(self):
    if self.has_frenzy:
        self.remove_attr(state=State.FRENZY)
        self.state |= State.DIVINE_SHIELD

def Aggem_malepine(self, enchantment, target):
    if self is target and enchantment.dbfId == CardName.BLOOD_GEM:
        for minion in self.owner.one_minion_by_type():
            minion.create_and_apply_enchantment('83_e', is_premium=self.is_premium)

def Agamaggan(self):
    self.owner.add_aura(self, boost_blood_gem=self.double_if_premium(1))

def Charlga(self):
    nb_gem = self.double_if_premium(1)
    for minion in self.owner:
        if minion != self:
            for _ in range(nb_gem):
                minion.create_and_apply_enchantment(CardName.BLOOD_GEM, is_premium=False)

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
    def play(self, source):
        if source.type & Type.QUILBOAR and source is not self:
            self.owner.owner.hand.create_card_in("70136")
            self.buff('90_e', self)

class Prophete_du_sanglier_p:
    def play(self, source):
        if source.type & Type.QUILBOAR and source is not self:
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
