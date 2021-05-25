# coding : utf-8

import random
import constants
import script_functions
import player

# habitué sans-visage (partiel)
def Murozond(self):
    pass
"""
    board_adv = self.owner.owner.last_opponent.real_board
    if board_adv and self.owner.owner.hand.can_add_card():
        card_key_number = random.choice(board_adv).key_number
        if card_key_number[-2:] == '_p':
            card_key_number = card_key_number[:-2]
        for card in self.bob.hand:
            if card.key_number == card_key_number:
                self.owner.owner.hand.append(card)
                return card
        return self.owner.owner.hand.create_card(card_key_number)
    return None

def Murozond_p(self):
    board_adv = [card
        for card in self.owner.owner.last_opponent.real_board
            if card.key_number != '513_p']

    if board_adv and self.owner.owner.hand.can_add_card():
        card_key_number = random.choice(board_adv).key_number
        if card_key_number[-2:] != '_p':
            if card_key_number + '_p' in self.bob.all_card:
                card_key_number = card_key_number + '_p'
        card = self.owner.owner.hand.create_card(card_key_number)
        if card_key_number[-2:] == '_p':
            card_key_number = card_key_number[:-2]

        card_from_bob = []
        for minion in self.bob.hand: # retrait des 3 cartes de la main de bob, sûr ?
            if minion.key_number == card_key_number:
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
    key_number = card.key_number
    if key_number[-2:] == '_p':
        key_number = key_number[:-2]
    self.set_card(key_number, copy=False)

def Habitue_sans_visage_p(self, card):
    #TODO
    key_number = card.key_number
    if key_number[-2:] != '_p':
        if key_number + '_p' in self.bob.all_card:
            key_number = key_number + '_p'

    self.set_card(key_number, copy=False)

def Nomi(self, card):
    if self != card and card.type & constants.TYPE_ELEMENTAL:
        self.owner.owner.bonus_nomi += self.double_if_premium(1)

def Tranchetripe(self):
    nb = 0
    for minion in self.owner:
        if minion.type & constants.TYPE_DRAGON:
            nb += 1
    if self.is_premium:
        self.apply_effect_on("16", nb)
    else:
        self.apply_effect_on("16_p", nb)

def Captaine_Larrrrdeur(self, card):
    if card.type & constants.TYPE_PIRATE:
        self.owner.owner.gold += self.double_if_premium(1)

def Devoreur_dames(self):
    #TODO !!!!!!
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_DEMON)
    if minion:
        self.attack += minion.attack*self.double_if_premium(1)
        self.health += minion.health*self.double_if_premium(1)
        self.owner.owner.gold += 3*self.double_if_premium(1)
        self.bob.hand.append(minion)

def Apprentie_reinit(self):
    self.mech_die = []

def Apprentie_kill(self, victim):
    if victim.type & constants.TYPE_MECH:
        try:
            self.mech_die.append(victim.key_number)
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
    bonus = self.double_if_premium(2)
    self.owner.add_enchantment(self, attack=bonus, health=bonus, insensible=1, restr_type=constants.TYPE_DEMON)

def Brise_siege_a(self):
    self.owner.add_enchantment(self, attack=self.double_if_premium(1), restr_type=constants.TYPE_DEMON)

def Chef_de_guerre_murloc_a(self):
    self.owner.add_enchantment(self, attack=self.double_if_premium(2), restr_type=constants.TYPE_MURLOC)

def Capitaine_des_mers_a(self): #add
    bonus = self.double_if_premium(1)
    self.owner.add_enchantment(self, attack=bonus, health=bonus, restr_type=constants.TYPE_PIRATE)

def Mythrax(self):
    type_indispo = 0
    nb = 0
    for minion in self.owner:
        if minion.type:
            if not minion.type & type_indispo or minion.type == constants.TYPE_ALL:
                nb += 1
                if minion.type != constants.TYPE_ALL:
                    type_indispo |= minion.type
    if not self.is_premium:
        self.apply_effect_on("17", nb)
    else:
        self.apply_effect_on("17_p", nb)

def Heraut_qijari(self, victim):
    if victim.state & constants.STATE_TAUNT:
        for minion in [self.owner[victim.position+1], self.owner[victim.position-1]]:
            if minion:
                if not self.is_premium:
                    minion.apply_effect_on("18")
                else:
                    minion.apply_effect_on("18_p")

def Gardienne_dantan(self):
    self.owner.owner.hand.create_card('1001')

def Gardienne_dantan_p(self):
    self.owner.owner.hand.create_card('1001')
    self.owner.owner.hand.create_card('1001')

def Champion_dYshaarj(self, ally):
    if ally.state & constants.STATE_TAUNT:
        self.apply_effect_on("19")

def Champion_dYshaarj_p(self, ally):
    if ally.state & constants.STATE_TAUNT:
        self.apply_effect_on("19_p")

def Bras_de_lempire(self, ally):
    if ally.state & constants.STATE_TAUNT:
        ally.apply_effect_on("20")

def Bras_de_lempire_p(self, ally):
    if ally.state & constants.STATE_TAUNT:
        ally.apply_effect_on("20_p")

def Ritualiste_tourmente(self, defenser):
    if self == defenser:
        for minion in [self.owner[self.position-1], self.owner[self.position+1]]:
            minion.apply_effect_on("21")

def Ritualiste_tourmente_p(self, defenser):
    if self == defenser:
        for minion in [self.owner[self.position-1], self.owner[self.position+1]]:
            minion.apply_effect_on("21_p")

def Nat_Pagle(self, attacker, victim):
    # n'est pas une découverte à 1 car peut se découvrir lui-même
    if self is attacker:
        for _ in range(self.double_if_premium(1)):
            lst = self.bob.hand.cards_of_tier_max(self.owner.owner.level)
            if lst:
                card = random.choice(lst)
                self.owner.owner.hand.append(card)

def Amiral_de_leffroi(self, attacker):
    if attacker.type & constants.TYPE_PIRATE:
        for minion in self.owner:
            minion.apply_effect_on("21")

def Amiral_de_leffroi_p(self, attacker):
    if attacker.type & constants.TYPE_PIRATE:
        for minion in self.owner:
            minion.apply_effect_on("21_p")

def Capitaine_Grondeventre(self, attacker):
    if attacker.type & constants.TYPE_PIRATE and self != attacker:
        attacker.apply_effect_on("22")

def Capitaine_Grondeventre_p(self, attacker):
    if attacker.type & constants.TYPE_PIRATE and self != attacker:
        attacker.apply_effect_on("22_p")

def Brann(self):
    self.owner.add_enchantment(self, boost_battlecry=self.double_if_premium(1))

def Baron_Vaillefendre(self):
    self.owner.add_enchantment(self, boost_deathrattle=self.double_if_premium(1))

def Khadgar(self):
    self.owner.add_enchantment(self, boost_invoc=self.double_if_premium(1))

def Raflelor(self):
    self.apply_effect_on("1", self.owner.nb_premium_card())

def Raflelor_p(self):
    self.apply_effect_on("1_p", self.owner.nb_premium_card())

def Micromomie(self):
    if not self.is_premium:
        Boost_other(self, "23", nb_max=1)
    else:
        Boost_other(self, "23_p", nb_max=1)

def Sensei_de_fer(self):
    Boost_other(self, "24", type=constants.TYPE_MECH, nb_max=1)

def Sensei_de_fer_p(self):
    Boost_other(self, "24_p", type=constants.TYPE_MECH, nb_max=1)

def Chambellan_Executus(self):
    nb = 1
    bonus = 1
    if self.is_premium:
        bonus = 2
    for minion in self.owner.owner.minion_play_this_turn:
        if minion.type & constants.TYPE_ELEMENTAL:
            nb += bonus
    self.owner[0].apply_effect_on("25", nb)

def Micro_machine(self):
    self.apply_effect_on("2")

def Micro_machine_p(self):
    self.apply_effect_on("2_p")

def Dragon_infamelique(self):
    self.apply_effect_on("3")

def Dragon_infamelique_p(self):
    self.apply_effect_on("3_p")

def Plaiedecaille_cobalt(self):
    Boost_other(self, "26", nb_max=1)

def Plaiedecaille_cobalt_p(self):
    Boost_other(self, "26_p", nb_max=1)

def Massacreuse_croc_radieux(self):
    position_check = list(range(len(self.owner)))
    type_indispo = 0

    while position_check:
        random_position = random.choice(position_check)
        minion = self.owner[random_position]
        if minion.type:
            if not minion.type & type_indispo or minion.type == constants.TYPE_ALL:
                minion.apply_effect_on("27")
                if minion.type != constants.TYPE_ALL:
                    type_indispo |= minion.type

        position_check.remove(random_position)

def Massacreuse_croc_radieux_p(self):
    position_check = list(range(len(self.owner)))
    type_indispo = 0

    while position_check:
        random_position = random.choice(position_check)
        minion = self.owner[random_position]
        if minion.type:
            if not minion.type & type_indispo or minion.type == constants.TYPE_ALL:
                minion.apply_effect_on("27_p")
                if minion.type != constants.TYPE_ALL:
                    type_indispo |= minion.type

        position_check.remove(random_position)

def Elémentplus(self, minion):
    if self is minion and type(self.owner.owner) is player.Player:
        self.owner.owner.hand.create_card("117a")

def Elémentplus_p(self, minion):
    if self is minion and type(self.owner.owner) is player.Player:
        self.owner.owner.hand.create_card("117a")
        self.owner.owner.hand.create_card("117a")

def Bronze_couenne(self, minion):
    if self is minion and type(self.owner.owner) is player.Player:
        self.owner.owner.hand.create_card("1022")
        self.owner.owner.hand.create_card("1022")
        if self.is_premium:
            self.owner.owner.hand.create_card("1022")
            self.owner.owner.hand.create_card("1022")

def Geomancien_de_Tranchebauge(self):
    self.owner.owner.hand.create_card("1022")
    if self.is_premium:
        self.owner.owner.hand.create_card("1022")

def Regisseur_du_temps(self, minion):
    if self is minion and type(self.owner.owner) is player.Player:
        for minion in self.bob.boards[self.owner.owner]:
            minion.apply_effect_on("28")

def Regisseur_du_temps_p(self, minion):
    if self is minion and type(self.owner.owner) is player.Player:
        for minion in self.owner.opponent:
            minion.apply_effect_on("28_p")

def Parieuse_convaincante(self, minion):
    if self is minion:
        self.owner.owner.gold += 2

def Parieuse_convaincante_p(self, minion):
    if self is minion:
        self.owner.owner.gold += 5

def Bolvar_sang_de_feu(self):
    self.apply_effect_on("29")

def Bolvar_sang_de_feu_p(self):
    self.apply_effect_on("29_p")

def Massacreur_drakonide(self):
    self.apply_effect_on("30")

def Massacreur_drakonide_p(self):
    self.apply_effect_on("30_p")

def Tisse_colere(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_DEMON):
        self.apply_effect_on("4")
        self.owner.owner.hp -= 1

def Tisse_colere_p(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_DEMON):
        self.apply_effect_on("4_p")
        self.owner.owner.hp -= 1

def Mande_flots_murloc(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_MURLOC):
        if type(self.owner.opponent.owner) is player.Player:
            self.apply_effect_on("31")
        else:
            self.apply_effect_on("5")

def Mande_flots_murloc_p(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_MURLOC):
        if type(self.owner.opponent.owner) is player.Player:
            self.apply_effect_on("31_p")
        else:
            self.apply_effect_on("5_p")

def Guetteur_Flottant(self):
    self.apply_effect_on("11")

def Guetteur_Flottant_p(self):
    self.apply_effect_on("11_p")

def Mini_Rag(self, invoc):
    if invoc.is_type(constants.TYPE_ELEMENTAL) and invoc != self:
        random.choice(self.owner).apply_effect_on("31", invoc.level)

def Mini_Rag_p(self, invoc):
    if invoc.is_type(constants.TYPE_ELEMENTAL) and invoc != self:
        for _ in range(2):
            random.choice(self.owner).apply_effect_on("31", invoc.level)

def Pillard_pirate(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_PIRATE):
        self.apply_effect_on("6")

def Pillard_pirate_p(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_PIRATE):
        self.apply_effect_on("6_p")

def Kalecgos(self, invoc):
    if self != invoc and invoc.have_script_type(constants.EVENT_BATTLECRY):
        Boost_all(self, "33", typ=constants.TYPE_DRAGON)

def Kalecgos_p(self, invoc):
    if self != invoc and invoc.have_script_type(constants.EVENT_BATTLECRY):
        Boost_all(self, "33_p", typ=constants.TYPE_DRAGON)

def Lieutenant_garr(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_ELEMENTAL):
        bonus = 0
        for minion in self.owner:
            if minion.is_type(constants.TYPE_ELEMENTAL):
                bonus += 1
        if self.is_premium:
            self.apply_effect_on("7_p", bonus)
        else:
            self.apply_effect_on("7", bonus)

def Favori_de_la_foule(self, invoc):
    if self != invoc and invoc.have_script_type(constants.EVENT_BATTLECRY):
        self.apply_effect_on("8")

def Favori_de_la_foule_p(self, invoc):
    if self != invoc and invoc.have_script_type(constants.EVENT_BATTLECRY):
        self.apply_effect_on("8_p")

def Saurolisque_enrage(self, invoc):
    if self != invoc and invoc.have_script_type(constants.EVENT_DEATHRATTLE):
        self.apply_effect_on("9")

def Saurolisque_enrage_p(self, invoc):
    if self != invoc and invoc.have_script_type(constants.EVENT_DEATHRATTLE):
        self.apply_effect_on("9_p")

def Roche_en_fusion(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_ELEMENTAL):
        self.apply_effect_on("10")

def Roche_en_fusion_p(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_ELEMENTAL):
        self.apply_effect_on("10_p")

def Elementaire_de_fete(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_ELEMENTAL):
        for _ in range(self.double_if_premium(1)):
            Boost_other(self, "34", type=constants.TYPE_ELEMENTAL, nb_max=1)

def Demon_demesure(self, target):
    if self != target and target.is_type(constants.TYPE_DEMON):
        self.apply_effect_on("35")

def Demon_demesure_p(self, target):
    if self != target and target.is_type(constants.TYPE_DEMON):
        self.apply_effect_on("35_p")

def Maman_ourse(self, target):
    if self != target and target.is_type(constants.TYPE_BEAST):
        self.apply_effect_on("36")

def Maman_ourse_p(self, target):
    if self != target and target.is_type(constants.TYPE_BEAST):
        self.apply_effect_on("36_p")

def Chef_de_Meute(self, target):
    if self != target and target.is_type(constants.TYPE_BEAST):
        self.apply_effect_on("37")

def Chef_de_Meute_p(self, target):
    if self != target and target.is_type(constants.TYPE_BEAST):
        self.apply_effect_on("37_p")

def Gardien_des_Glyphes(self, attacker):
    if self is attacker:
        self.apply_effect_on("38", self.attack)

def Gardien_des_Glyphes_p(self, attacker):
    if self is attacker:
        self.apply_effect_on("38_p", self.attack)

def Dragonnet_rouge(self):
    #for card in self.owner.owner.real_board.board:
    nb_dragon_in_board = 0
    for card in self.owner: # les dragons présents avant toute phase de combat sont comptabilisés
        if self.are_same_type(card):
            nb_dragon_in_board += 1

    if nb_dragon_in_board:
        for _ in range(self.double_if_premium(1)):
            if self.owner.opponent:
                target = random.choice(self.owner.opponent)
                #print(f"{self.name} souffle sur {target.name} !")
                self.owner.owner.fight.create_single_damage_event(self, target, nb_dragon_in_board)

def Ara_monstrueux(self):
    minion_with_deathrattle = [minion
        for minion in self.owner
            if minion.have_script_type(constants.EVENT_DEATHRATTLE) and minion.is_alive]

    if minion_with_deathrattle:
        target = random.choice(minion_with_deathrattle)
        target.active_script_type(constants.EVENT_DEATHRATTLE)

def Ara_monstrueux_p(self):
    minion_with_deathrattle = [minion
        for minion in self.owner
            if minion.have_script_type(constants.EVENT_DEATHRATTLE) and minion.is_alive]

    if minion_with_deathrattle:
        target = random.choice(minion_with_deathrattle)
        target.active_script_type(constants.EVENT_DEATHRATTLE)
        target.active_script_type(constants.EVENT_DEATHRATTLE)

def Deflect_o_bot(self, repop):
    if self != repop and repop.is_type(constants.TYPE_MECH):
        self.apply_effect_on("39")

def Deflect_o_bot_p(self, repop):
    if self != repop and repop.is_type(constants.TYPE_MECH):
        self.apply_effect_on("39_p")

def Jongleur_d_ame(self, victim):
    if victim.is_type(constants.TYPE_DEMON):
        if self.owner.opponent.board:
            random_target = random.choice(self.owner.opponent.board)
            self.owner.owner.fight.create_single_damage_event(self, random_target, 3)

def Jongleur_d_ame_p(self, victim):
    if victim.is_type(constants.TYPE_DEMON):
        for _ in range(2):
            if self.owner.opponent.board:
                random_target = random.choice(self.owner.opponent.board)
                self.owner.owner.fight.create_single_damage_event(self, random_target, 3)

def Charognard2_1(self, victim):
    if self.are_same_type(victim):
        self.apply_effect_on("40")

def Charognard4_2(self, victim):
    if self.are_same_type(victim):
        self.apply_effect_on("40_p")

def Charognard2_2(self, victim):
    if self.are_same_type(victim):
        self.apply_effect_on("41")

def Charognard4_4(self, victim):
    if self.are_same_type(victim):
        self.apply_effect_on("41_p")

def Poisson(self, victim):
    self.copy_deathrattle(victim)

def Init_poisson(self):
    try:
        del self.script[constants.EVENT_DEATHRATTLE]
    except KeyError:
        pass

def Dragon_killer2_2(self, killer, victim):
    if killer.is_type(constants.TYPE_DRAGON):
        self.apply_effect_on("41")

def Dragon_killer4_4(self, killer, victim):
    if killer.is_type(constants.TYPE_DRAGON):
        self.apply_effect_on("41_p")

### BATTLECRY ###

def Anomalie_actualisante(self):
    self.owner.owner.nb_free_roll = max(self.owner.owner.nb_free_roll, 1)

def Anomalie_actualisante_p(self):
    self.owner.owner.nb_free_roll = max(self.owner.owner.nb_free_roll, 2)

def Amalgadon(self):
    type_cumul = 0
    nb_adapt = 0
    for servant in self.owner:
        if servant != self and servant.type and (not servant.type & type_cumul\
                or servant.type == constants.TYPE_ALL):
            nb_adapt += 1
            if servant.type != constants.TYPE_ALL:
                type_cumul |= servant.type

    for _ in range(nb_adapt):
        adapt_spell(self)

def adapt_spell(self, nb=0):
    if not nb:
        nb = random.randint(1, 8)

    if nb == 8:
        self.add_deathrattle('Amalgadon_repop')
    elif nb > 0 and nb < 8:
        self.apply_effect_on(str(42+nb))
    else:
        print(f"Amalgadon adapt error n°{nb}")

def Amalgadon_p(self):
    type_cumul = 0
    nb_adapt = 0
    for servant in self.owner:
        if servant != self and servant.type and (not servant.type & type_cumul\
                or servant.type == constants.TYPE_ALL):
            nb_adapt += 2
            if servant.type != constants.TYPE_ALL:
                type_cumul |= servant.type

    for _ in range(nb_adapt):
        adapt_spell(self)

def Guetteur_primaileron(self):
    for minion in self.owner:
        if minion != self and minion.is_type(constants.TYPE_MURLOC):
            self.owner.owner.discover(self, nb=3, typ=constants.TYPE_MURLOC)
            break

def Guetteur_primaileron_p(self):
    for minion in self.owner:
        if minion != self and minion.is_type(constants.TYPE_MURLOC):
            self.owner.owner.discover(self, nb=3, typ=constants.TYPE_MURLOC)
            self.owner.owner.discover(self, nb=3, typ=constants.TYPE_MURLOC)
            break

def Tempete_de_la_taverne(self):
    self.owner.owner.discover(self, nb=1, typ=constants.TYPE_ELEMENTAL)

def Tempete_de_la_taverne_p(self):
    self.owner.owner.discover(self, nb=1, typ=constants.TYPE_ELEMENTAL)
    self.owner.owner.discover(self, nb=1, typ=constants.TYPE_ELEMENTAL)

def Maitre_de_guerre_annihileen(self):
    #TODO: 1 effet de valeur variable ??
    self.apply_effect_on("12", self.owner.owner.init_hp - self.owner.owner.hp)

def Maitre_de_guerre_annihileen_p(self):
    self.apply_effect_on("12_p", self.owner.owner.init_hp - self.owner.owner.hp)

def Gaillarde_des_mers_du_sud(self):
    bonus = 0
    for minion in self.owner.owner.minion_buy_this_turn:
        if minion.type & constants.TYPE_PIRATE:
            bonus += 1

    if bonus:
        minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_PIRATE)
        if minion:
            if self.is_premium:
                minion.apply_effect_on("50", bonus)
            else:
                minion.apply_effect_on("50_p", bonus)

def Pillard_dure_ecaille(self):
    for minion in self.owner:
        if minion.state & constants.STATE_TAUNT:
            minion.apply_effect_on("13")

def Pillard_dure_ecaille_p(self):
    for minion in self.owner:
        if minion.state & constants.STATE_TAUNT:
            minion.apply_effect_on("13_p")

def Roi_Bagargouille(self):
    Boost_other(self, "51", type=constants.TYPE_MURLOC)

def Roi_Bagargouille_p(self):
    Boost_other(self, "51_p", type=constants.TYPE_MURLOC)

def Roi_Bagargouille_death(self):
    Boost_other(self, "52", type=constants.TYPE_MURLOC)

def Roi_Bagargouille_death_p(self):
    Boost_other(self, "52_p", type=constants.TYPE_MURLOC)

def Invoc01(self): # chasse-marée, chat de gouttière
    script_functions.invocation(self, self.key_number + "a", 1, self.position)

def Invoc01_p(self): # chasse-marée, chat de gouttière
    script_functions.invocation(self, self.key_number[:-2] + "a_p", 1, self.position)

def Forban(self):
    script_functions.invocation(self, "113a", 1, self.position)

def Forban_p(self):
    script_functions.invocation(self, "113a_p", 1, self.position)

def Gentille_grand_mere(self):
    script_functions.invocation(self, "203a", 1, self.position)

def Gentille_grand_mere_p(self):
    script_functions.invocation(self, "203a_p", 1, self.position)

def Golem_des_moissons(self):
    script_functions.invocation(self, "204a", 1, self.position)

def Golem_des_moissons_p(self):
    script_functions.invocation(self, "204a_p", 1, self.position)

def Emprisonneur(self):
    script_functions.invocation(self, "210a", 1, self.position)

def Emprisonneur_p(self):
    script_functions.invocation(self, "210a_p", 1, self.position)

def Mecanoeuf(self):
    script_functions.invocation(self, "408a", 1, self.position)

def Mecanoeuf_p(self):
    script_functions.invocation(self, "408a_p", 1, self.position)

def Mousse_du_pont(self):
    self.owner.owner.level_up_cost -= 1
    #print(f"{self.name} réduit le coût de up de la taverne.")

def Mousse_du_pont_p(self):
    self.owner.owner.level_up_cost -= 2
    #print(f"{self.name} réduit le coût de up de la taverne.")

def Defenseur_d_Argus(self):
    targets = [self.owner[self.position - 1], self.owner[self.position + 1]]

    for target in targets:
        if target:
            if self.is_premium:
                target.apply_effect_on("53_p")
            else:
                target.apply_effect_on("53")

def Aileron_toxique(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_MURLOC)
    if minion:
        minion.apply_effect_on("54")

def Homoncule_sans_gene(self):
    self.owner.owner.hp -= 2

def Sensei_virmen(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_BEAST)
    if minion:
        minion.apply_effect_on("55")

def Sensei_virmen_p(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_BEAST)
    if minion:
        minion.apply_effect_on("55_p")

def Chasseur_rochecave(self): # bonus posé sur le premier murloc trouvé
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_MURLOC)
    if minion:
        minion.apply_effect_on("56")

def Chasseur_rochecave_p(self): # bonus posé sur le premier murloc trouvé
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_MURLOC)
    if minion:
        minion.apply_effect_on("56_p")

def Cliqueteur(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_MECH)
    if minion:
        minion.apply_effect_on("57")

def Cliqueteur_p(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_MECH)
    if minion:
        minion.apply_effect_on("57_p")

def Bondisseur_dent_de_metal(self):
    Boost_other(self, "58", type=constants.TYPE_MECH)

def Bondisseur_dent_de_metal_p(self):
    Boost_other(self, "58_p", type=constants.TYPE_MECH)

def Navigateur_gangraileron(self):
    Boost_other(self, "59", type=constants.TYPE_MURLOC)

def Navigateur_gangraileron_p(self):
    Boost_other(self, "59_p", type=constants.TYPE_MURLOC)

def Tisse_cristal(self):
    Boost_other(self, "60", type=constants.TYPE_DEMON)

def Tisse_cristal_p(self):
    Boost_other(self, "60_p", type=constants.TYPE_DEMON)

def Assistant_arcanique(self):
    Boost_other(self, "61", type=constants.TYPE_ELEMENTAL)

def Assistant_arcanique_p(self):
    Boost_other(self, "61_p", type=constants.TYPE_ELEMENTAL)

def Canonnier(self):
    Boost_other(self, "62", type=constants.TYPE_PIRATE)

def Canonnier_p(self):
    Boost_other(self, "62_p", type=constants.TYPE_PIRATE)

def Emissaire_du_crepuscule(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_DRAGON)
    if minion:
        self.apply_effect_on("63")

def Emissaire_du_crepuscule_p(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_DRAGON)
    if minion:
        self.apply_effect_on("63_p")

def Voyant_froide_lumiere(self):
    Boost_other(self, "64", type=constants.TYPE_MURLOC)

def Voyant_froide_lumiere_p(self):
    Boost_other(self, "64_p", type=constants.TYPE_MURLOC)

def Maitre_chien(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_BEAST)
    if minion:
        minion.apply_effect_on("65")

def Maitre_chien_p(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_BEAST)
    if minion:
        minion.apply_effect_on("65_p")

def Surveillant_Nathrezim(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_DEMON)
    if minion:
        minion.apply_effect_on("66")

def Surveillant_Nathrezim_p(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_DEMON)
    if minion:
        minion.apply_effect_on("66_p")

def Menagerie_1(self):
    Bonus_ménagerie(self, "67")

def Menagerie_2(self):
    Bonus_ménagerie(self, "67_p")

def Menagerie_3(self):
    Bonus_ménagerie(self, "68")

def Menagerie_4(self):
    Bonus_ménagerie(self, "68_p")

def Elementaire_de_stase(self):
    elem = None
    for minion in self.owner.opponent.owner.hand.cards_of_tier_max(self.owner.owner.level):
        if minion.is_type(constants.TYPE_ELEMENTAL):
            elem = minion
            break
    if elem:
        elem.play(board=self.owner.opponent)
        elem.state |= constants.STATE_FREEZE

def Elementaire_de_stase_p(self):
    for _ in range(2):
        elem = None
        for minion in self.owner.opponent.owner.hand.cards_of_tier_max(self.owner.owner.level):
            if minion.is_type(constants.TYPE_ELEMENTAL):
                elem = minion
                break
        if elem:
            elem.play(board=self.owner.opponent)
            elem.state |= constants.STATE_FREEZE

def Bonus_ménagerie(self, key_effect):
    position_check = list(range(len(self.owner)))
    type_indispo = 0
    nb_cible_restante = 3

    while nb_cible_restante and position_check:
        random_position = random.choice(position_check)
        serviteur = self.owner[random_position]
        if serviteur.is_type(constants.TYPE_ALL):
            if not serviteur.type & type_indispo or serviteur.type == constants.TYPE_ALL:
                nb_cible_restante -= 1
                serviteur.apply_effect_on(key_effect)
                if serviteur.type != constants.TYPE_ALL:
                    type_indispo |= serviteur.type

        position_check.remove(random_position)

def Lapin(self):
    self.apply_effect_on("69", self.owner.owner.nb_lapin)

def Lapin_p(self):
    self.apply_effect_on("69_p", self.owner.owner.nb_lapin)

def Boost_other(self, effect_key, type=constants.TYPE_ALL, nb_max=constants.BATTLE_SIZE):
    board = [minion
        for minion in self.owner
            if minion.is_type(type) and minion != self]

    random_target = None
    while board and nb_max:
        random_target = random.choice(board)
        random_target.apply_effect_on(effect_key)
        board.remove(random_target)
        nb_max -= 1

    return random_target

def Boost_all(self, effect_key, typ=None):
    for minion in self.owner:
        if typ is None or minion.is_type(typ):
            minion.apply_effect_on(effect_key)

##### DEATHRATTLE #####


def Nadina(self):
    for servant in self.owner:
        if servant.is_type(constants.TYPE_DRAGON):
            servant.state_fight |= constants.STATE_DIVINE_SHIELD

def Goldrinn(self):
    Boost_all(self, "70", constants.TYPE_BEAST)

def Goldrinn_p(self):
    Boost_all(self, "70_p", constants.TYPE_BEAST)

def Gentil_djinn(self):
    """ donne-t-il un elem au hasard de la taverne ou une carte elem choisie au
    hasard parmi toutes les possibilités ?
    maj 18.6 : summon que des serviteurs d'un niveau inférieur ou égal à celui de la taverne
    """
    cards = self.bob.hand.cards_type_of_tier_max(
            tier_max=self.owner.owner.level, typ=constants.TYPE_ELEMENTAL)

    if cards:
        card = random.choice(cards)
        cards.remove(card)
        if card.key_number != self.key_number:
            script_functions.invocation(self, card.key_number,
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
            tier_max=self.owner.owner.level, typ=constants.TYPE_ELEMENTAL)

    for _ in range(2):
        if cards:
            card = random.choice(cards)
            cards.remove(card)
            if card.key_number != self.key_number:
                script_functions.invocation(self, card.key_number,
                    nb_max=1, position=self.position)
                self.owner.owner.hand.append(card)
        else:
            print(f'{self.name} bob hand empty')
            break

def Boagnarok(self):
    cards = self.bob.card_can_collect
    rale_cards = [key
        for key, value in cards.items()
            if constants.EVENT_DEATHRATTLE in value["script"]]

    script_functions.invocation_random_list(self, rale_cards, 2)

def Boagnarok_p(self):
    cards = self.bob.card_can_collect
    rale_cards = [key
        for key, value in cards.items()
            if constants.EVENT_DEATHRATTLE in value["script"]]

    script_functions.invocation_random_list(self, rale_cards, 4)

def Tranche_les_vagues(self):
    pirate_cards = [key
        for key, value in self.bob.card_can_collect.items()
            if value["type"] & constants.TYPE_PIRATE]

    script_functions.invocation_random_list(self, pirate_cards, 3)

def Tranche_les_vagues_p(self):
    pirate_cards = [key
        for key, value in self.bob.card_can_collect.items()
            if value["type"] & constants.TYPE_PIRATE]

    script_functions.invocation_random_list(self, pirate_cards, 6)

def Sneed(self):
    cards = self.bob.card_can_collect
    legendary_cards = [key
        for key, value in cards.items()
            if value.get("legendary")]

    script_functions.invocation_random_list(self, legendary_cards, 1)

def Sneed_p(self):
    cards = self.bob.card_can_collect
    legendary_cards = [key
        for key, value in cards.items()
            if value.get("legendary")]

    script_functions.invocation_random_list(self, legendary_cards, 2)

def Goliath_brisemer(*arg):
    self = arg[0]
    Boost_other(self, "71", type=constants.TYPE_PIRATE)

def Goliath_brisemer_p(*arg):
    self = arg[0]
    Boost_other(self, "71_p", type=constants.TYPE_PIRATE)

def Navrecorne_cuiracier(self, target_position, attaquant_position, damage):
    script_functions.invocation(self, "504a", 1, attaquant_position)

def Navrecorne_cuiracier_p(self, target_position, attaquant_position, damage):
    script_functions.invocation(self, "504a_p", 1, attaquant_position)

def Feu_de_brousse(self, target_position, attaquant_position, damage):
    # la cible est déjà retirée du board adverse
    if damage > 0 and self.owner.opponent:
        if target_position == 0: # first card
            self.owner.owner.fight.take_damage(self, self.owner.opponent[0], damage, overkill=False)
        elif target_position == len(self.owner.opponent): # last card
            self.owner.owner.fight.take_damage(self, self.owner.opponent[-1], damage, overkill=False)
        else:
            if random.randint(0, 1):
                self.owner.owner.fight.take_damage(self, self.owner.opponent[target_position], damage, overkill=False)
            else:
                self.owner.owner.fight.take_damage(self, self.owner.opponent[target_position-1], damage, overkill=False)

def Feu_de_brousse_p(self, target_position, attaquant_position, damage):
    # la cible est déjà retirée du board adverse
    if damage > 0 and self.owner.opponent:
        if target_position == 0: # first card
            self.owner.owner.fight.take_damage(self, self.owner.opponent[0], damage, overkill=False)
        elif target_position == len(self.owner.opponent): # last card
            self.owner.owner.fight.take_damage(self, self.owner.opponent[-1], damage, overkill=False)
        else:
            self.owner.owner.fight.take_damage(self, self.owner.opponent[target_position], damage, overkill=False)
            self.owner.owner.fight.take_damage(self, self.owner.opponent[target_position-1], damage, overkill=False)

def Heraut_de_la_flamme(*arg):
    self = arg[0]
    if self.owner.opponent:
        for minion in self.owner.opponent:
            if minion.is_alive:
                self.owner.owner.fight.take_damage(self, minion, 3)
                break

def Heraut_de_la_flamme_p(*arg):
    self = arg[0]
    if self.owner.opponent:
        for minion in self.owner.opponent:
            if minion.is_alive:
                self.owner.owner.fight.take_damage(self, minion, 6)
                break

def Maman_des_diablotins(self):
    demon_cards = [key
        for key, value in self.bob.card_can_collect.items()
            if value["type"] & constants.TYPE_DEMON]

    repop_id = script_functions.invocation_random_list(self, demon_cards, 1)
    if repop_id:
        repop_id.state_fight |= constants.STATE_TAUNT

def Maman_des_diablotins_p(self):
    demon_cards = [key
        for key, value in self.bob.card_can_collect.items()
            if value["type"] & constants.TYPE_DEMON]

    for _ in range(2):
        repop_id = script_functions.invocation_random_list(self, demon_cards, 1)
        if repop_id:
            repop_id.state_fight |= constants.STATE_TAUNT

def Forgeronne_des_tarides(self):
    if self.has_frenzy:
        self.state_fight &= constants.STATE_ALL - constants.STATE_FRENZY
        for minion in self.owner:
            if minion != self:
                if not self.is_premium:
                    minion.apply_effect_on("72")
                else:
                    minion.apply_effect_on("72_p")

def Chef_du_gang_des_diablotins(self):
    script_functions.invocation(self, "300a", 1)

def Chef_du_gang_des_diablotins_p(self):
    script_functions.invocation(self, "300a_p", 1)

def Rover_de_securite(self):
    script_functions.invocation(self, "410a", 1)

def Rover_de_securite_p(self):
    script_functions.invocation(self, "410a_p", 1)

def GroBoum(self):
    if self.owner.opponent:
        target = random.choice(self.owner.opponent)
        self.owner.owner.fight.create_single_damage_event(self, target, 4)

def GroBoum_p(self):
    for _ in range(2):
        if self.owner.opponent:
            target = random.choice(self.owner.opponent)
            self.owner.owner.fight.create_single_damage_event(self, target, 4)

def Rejeton(self):
    Boost_all(self, "73")

def Rejeton_p(self):
    Boost_all(self, "73_p")

def Clan_des_rats(self):
    script_functions.invocation(self, "305a", self.attack, self.position)

def Clan_des_rats_p(self):
    script_functions.invocation(self, "305a_p", self.attack, self.position)

def Loup_contamine(self):
    script_functions.invocation(self, "306a", 2, self.position)

def Loup_contamine_p(self):
    script_functions.invocation(self, "306a_p", 2, self.position)

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

def Menace_Repliquante(self):
    script_functions.invocation(self, "308a", 3, self.position)

def Menace_Repliquante_p(self):
    script_functions.invocation(self, "308a_p", 3, self.position)

def Dechiqueteur_pilote(self):
    lst_key_number = ["100", "101", "104", "105", "109", "110", "111", "203", "205", "303"]

    all_card = self.bob.card_can_collect
    new_lst_key_number = [key_number
        for key_number in lst_key_number
            if key_number in all_card]

    key_number = random.choice(new_lst_key_number)
    script_functions.invocation(self, key_number, 1, self.position)

def Dechiqueteur_pilote_p(self):
    lst_key_number = ["100", "101", "104", "105", "109", "110", "111", "203", "205", "303"]

    all_card = self.bob.card_can_collect
    new_lst_key_number = [key_number
        for key_number in lst_key_number
            if key_number in all_card]

    for _ in range(2):
        key_number = random.choice(new_lst_key_number)
        script_functions.invocation(self, key_number, 1, self.position)

def Héroïne_altruiste(self):
    cibles_potentielles = [minion
        for minion in self.owner
            if not minion.state & constants.STATE_DIVINE_SHIELD and minion.is_alive]

    if cibles_potentielles:
        cible = random.choice(cibles_potentielles)
        cible.state_fight |= constants.STATE_DIVINE_SHIELD
        #print(f"{self.name} offre un bouclier divin à {cible.name} !")

def Héroïne_altruiste_p(self):
    cibles_potentielles = [minion
        for minion in self.owner
            if not minion.state & constants.STATE_DIVINE_SHIELD and minion.is_alive]

    for _ in range(2):
        if cibles_potentielles:
            cible = random.choice(cibles_potentielles)
            cible.state_fight |= constants.STATE_DIVINE_SHIELD
            cibles_potentielles.remove(cible)
            #print(f"{self.name} offre un bouclier divin à {cible.name} !")

def Serviteur_diabolique(self):
    if self.owner:
        random.choice(self.owner).attack += self.attack
        #print(f"{self.name} offre {self.attack} d'attaque à {target.name} !")

def Serviteur_diabolique_p(self):
    if self.owner:
        for _ in range(2):
            random.choice(self.owner).attack += self.attack
            #print(f"{self.name} offre {self.attack} d'attaque à {target.name} !")

def Goule_instable(self):
    if self.owner:
        board = self.owner[:]
        for servant in board:
            self.owner.owner.fight.create_single_damage_event(self, servant, 1)
    if self.owner.opponent:
        board = self.owner.opponent[:]
        for servant in board:
            self.owner.owner.fight.create_single_damage_event(self, servant, 1)

def Goule_instable_p(self):
    for _ in range(2):
        if self.owner:
            board = self.owner[:]
            for servant in board:
                self.owner.owner.fight.create_single_damage_event(self, servant, 1)
        if self.owner.opponent:
            board = self.owner.opponent[:]
            for servant in board:
                self.owner.owner.fight.create_single_damage_event(self, servant, 1)