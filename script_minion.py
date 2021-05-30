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
    self.create_and_apply_enchantment("16", is_premium=self.is_premium, nb=nb)

def Captaine_Larrrrdeur(self, card):
    if card.type & constants.TYPE_PIRATE:
        self.owner.owner.gold += self.double_if_premium(1)

def Devoreur_dames(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_DEMON)
    if minion:
        self.owner.owner.gold += 3*self.double_if_premium(1)
        self.create_and_apply_enchantment("74", is_premium=self.is_premium, a=minion.attack, h=minion.health)
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
    self.owner.add_aura(self, insensible=1, method='Mal_Ganis')

def Mal_Ganis(self, target):
    if self != target and target.type & constants.TYPE_DEMON:
        target.create_and_apply_enchantment("78", is_premium=self.is_premium, origin=self, type='aura')

def Brise_siege_a(self):
    self.owner.add_aura(self, attack=self.double_if_premium(1), restr_type=constants.TYPE_DEMON)

def Chef_de_guerre_murloc_a(self):
    self.owner.add_aura(self, attack=self.double_if_premium(2), restr_type=constants.TYPE_MURLOC)

def Capitaine_des_mers_a(self): #add
    bonus = self.double_if_premium(1)
    self.owner.add_aura(self, attack=bonus, health=bonus, restr_type=constants.TYPE_PIRATE)

def Mythrax(self):
    self.create_and_apply_enchantment(
        "17",
        is_premium=self.is_premium,
        nb=len(self.owner.one_minion_by_type()))

def Heraut_qijari(self, victim):
    if victim.state & constants.STATE_TAUNT:
        for minion in victim.adjacent_neighbors():
            minion.create_and_apply_enchantment("18", is_premium=self.is_premium)

def Gardienne_dantan(self):
    self.owner.owner.hand.create_card('1001')

def Gardienne_dantan_p(self):
    self.owner.owner.hand.create_card('1001')
    self.owner.owner.hand.create_card('1001')

def Champion_dYshaarj(self, ally):
    if ally.state & constants.STATE_TAUNT:
        self.create_and_apply_enchantment("19", is_premium=self.is_premium)

def Bras_de_lempire(self, ally):
    if ally.state & constants.STATE_TAUNT:
        ally.create_and_apply_enchantment("20", is_premium=self.is_premium)

def Ritualiste_tourmente(self, defenser):
    if self == defenser:
        for minion in self.adjacent_neighbors():
            minion.create_and_apply_enchantment("21", is_premium=self.is_premium)

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
            minion.create_and_apply_enchantment("21", is_premium=self.is_premium)

def Capitaine_Grondeventre(self, attacker):
    if attacker.type & constants.TYPE_PIRATE and self != attacker:
        attacker.create_and_apply_enchantment("22", is_premium=self.is_premium)

def Brann(self):
    self.owner.add_aura(self, boost_battlecry=self.double_if_premium(1))

def Baron_Vaillefendre(self):
    self.owner.add_aura(self, boost_deathrattle=self.double_if_premium(1))

def Khadgar(self):
    self.owner.add_aura(self, boost_invoc=self.double_if_premium(1))

def Raflelor(self):
    self.create_and_apply_enchantment("1", is_premium=self.is_premium, nb=self.owner.nb_premium_card())

def Micromomie(self):
    Boost_other(self, "23", nb_max=1)

def Sensei_de_fer(self):
    Boost_other(self, "24", type=constants.TYPE_MECH, nb_max=1)

def Chambellan_Executus(self):
    nb = 0
    for minion in self.owner.owner.minion_play_this_turn:
        if minion.type & constants.TYPE_ELEMENTAL:
            nb += 1
    self.owner[0].create_and_apply_enchantment("25", is_premium=self.is_premium, nb=nb)

def Micro_machine(self):
    self.create_and_apply_enchantment("2", is_premium=self.is_premium)

def Dragon_infamelique(self):
    self.create_and_apply_enchantment("3", is_premium=self.is_premium)

def Plaiedecaille_cobalt(self):
    Boost_other(self, "26", nb_max=1)

def Massacreuse_croc_radieux(self):
    for minion in self.owner.one_minion_by_type():
        minion.create_and_apply_enchantment("27", is_premium=self.is_premium)

def Elémentplus(self, minion):
    if self is minion and type(self.owner.owner) is player.Player:
        for _ in range(self.double_if_premium(1)):
            self.owner.owner.hand.create_card("117a")

def Bronze_couenne(self, minion):
    if self is minion and type(self.owner.owner) is player.Player:
        for _ in range(self.double_if_premium(2)):
            self.owner.owner.hand.create_card("1014")
            self.owner.owner.hand.create_card("1014")

def Geomancien_de_Tranchebauge(self):
    self.owner.owner.hand.create_card("1014")
    if self.is_premium:
        self.owner.owner.hand.create_card("1014")

def Regisseur_du_temps(self, minion):
    if self is minion and type(self.owner.owner) is player.Player:
        for minion in self.bob.boards[self.owner.owner]:
            minion.create_and_apply_enchantment("28", is_premium=self.is_premium)

def Parieuse_convaincante(self, minion):
    if self is minion:
        self.owner.owner.gold += 2

def Parieuse_convaincante_p(self, minion):
    if self is minion:
        self.owner.owner.gold += 5

def Bolvar_sang_de_feu(self):
    self.create_and_apply_enchantment("29", is_premium=self.is_premium)

def Massacreur_drakonide(self):
    self.create_and_apply_enchantment("30", is_premium=self.is_premium)

def Tisse_colere(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_DEMON):
        self.create_and_apply_enchantment("4", is_premium=self.is_premium)
        self.owner.owner.hp -= 1

def Mande_flots_murloc(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_MURLOC):
        if type(self.owner.opponent.owner) is player.Player:
            self.create_and_apply_enchantment("31", is_premium=self.is_premium)
        else:
            self.create_and_apply_enchantment("5", is_premium=self.is_premium)

def Guetteur_Flottant(self):
    self.create_and_apply_enchantment("11", is_premium=self.is_premium)

def Mini_Rag(self, invoc):
    if invoc.is_type(constants.TYPE_ELEMENTAL) and invoc != self:
        for _ in range(self.double_if_premium(1)):
            random.choice(self.owner).create_and_apply_enchantment(
                "31",
                is_premium=False,
                a=invoc.level,
                h=invoc.level)

def Pillard_pirate(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_PIRATE):
        self.create_and_apply_enchantment("6", is_premium=self.is_premium)

def Kalecgos(self, invoc):
    if self != invoc and invoc.have_script_type(constants.EVENT_BATTLECRY):
        Boost_all(self, "33", typ=constants.TYPE_DRAGON)

def Lieutenant_garr(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_ELEMENTAL):
        bonus = 0
        for minion in self.owner:
            if minion.is_type(constants.TYPE_ELEMENTAL):
                bonus += 1
        self.create_and_apply_enchantment("7", is_premium=self.is_premium, h=bonus)

def Favori_de_la_foule(self, invoc):
    if self != invoc and invoc.have_script_type(constants.EVENT_BATTLECRY):
        self.create_and_apply_enchantment("8", is_premium=self.is_premium)

def Saurolisque_enrage(self, invoc):
    if self != invoc and invoc.have_script_type(constants.EVENT_DEATHRATTLE):
        self.create_and_apply_enchantment("9", is_premium=self.is_premium)

def Roche_en_fusion(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_ELEMENTAL):
        self.create_and_apply_enchantment("10", is_premium=self.is_premium)

def Elementaire_de_fete(self, invoc):
    if self != invoc and invoc.is_type(constants.TYPE_ELEMENTAL):
        for _ in range(self.double_if_premium(1)):
            Boost_other(self, "34", type=constants.TYPE_ELEMENTAL, nb_max=1, is_premium=False)

def Demon_demesure(self, target):
    if self != target and target.is_type(constants.TYPE_DEMON):
        self.create_and_apply_enchantment("35", is_premium=self.is_premium)

def Maman_ourse(self, target):
    if self != target and target.is_type(constants.TYPE_BEAST):
        self.create_and_apply_enchantment("36", is_premium=self.is_premium)

def Chef_de_Meute(self, target):
    if self != target and target.is_type(constants.TYPE_BEAST):
        self.create_and_apply_enchantment("37", is_premium=self.is_premium)

def Gardien_des_Glyphes(self, attacker):
    if self is attacker:
        self.create_and_apply_enchantment("38", is_premium=self.is_premium, a=self.attack)

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
        self.create_and_apply_enchantment("39", is_premium=self.is_premium)

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
        self.create_and_apply_enchantment("40", is_premium=self.is_premium)

def Charognard2_2(self, victim):
    if self.are_same_type(victim):
        self.create_and_apply_enchantment("41", is_premium=self.is_premium)

def Poisson(self, victim):
    self.copy_deathrattle(victim)

def Init_poisson(self):
    try:
        del self.script[constants.EVENT_DEATHRATTLE]
    except KeyError:
        pass

def Dragon_killer2_2(self, killer, victim):
    if killer.is_type(constants.TYPE_DRAGON):
        self.create_and_apply_enchantment("41", is_premium=self.is_premium)

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

    nb_adapt *= self.double_if_premium(1)
    for _ in range(nb_adapt):
        adapt_spell(self)

def adapt_spell(self, nb=0):
    if not nb:
        nb = random.randint(1, 8)

    if 1 <= nb <= 8:
        self.create_and_apply_enchantment(str(42+nb))
    else:
        print(f"Amalgadon adapt error n°{nb}")

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
    health = self.owner.owner.init_hp - self.owner.owner.hp
    self.create_and_apply_enchantment("12", is_premium=self.is_premium, h=health)

def Gaillarde_des_mers_du_sud(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_PIRATE)
    if minion:
        bonus = 0
        for minion in self.owner.owner.minion_buy_this_turn:
            if minion.type & constants.TYPE_PIRATE:
                bonus += 1
        minion.create_and_apply_enchantment("87", is_premium=self.is_premium, nb=bonus)

def Pillard_dure_ecaille(self):
    for minion in self.owner:
        if minion.state & constants.STATE_TAUNT:
            minion.create_and_apply_enchantment("13", is_premium=self.is_premium)

def Roi_Bagargouille(self):
    Boost_other(self, "51", type=constants.TYPE_MURLOC, is_premium=self.is_premium)

def Roi_Bagargouille_death(self):
    Boost_other(self, "52", type=constants.TYPE_MURLOC, is_premium=False)

def Roi_Bagargouille_death_p(self):
    Boost_other(self, "52", type=constants.TYPE_MURLOC, is_premium=True)

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
            target.create_and_apply_enchantment("53", is_premium=self.is_premium)

def Aileron_toxique(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_MURLOC)
    if minion:
        minion.create_and_apply_enchantment("54", is_premium=self.is_premium)

def Homoncule_sans_gene(self):
    self.owner.owner.hp -= 2

def Sensei_virmen(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_BEAST)
    if minion:
        minion.create_and_apply_enchantment("55", is_premium=self.is_premium)

def Chasseur_rochecave(self): # bonus posé sur le premier murloc trouvé
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_MURLOC)
    if minion:
        minion.create_and_apply_enchantment("56", is_premium=self.is_premium)

def Cliqueteur(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_MECH)
    if minion:
        minion.create_and_apply_enchantment("57", is_premium=self.is_premium)

def Bondisseur_dent_de_metal(self):
    Boost_other(self, "58", type=constants.TYPE_MECH, is_premium=self.is_premium)

def Navigateur_gangraileron(self):
    Boost_other(self, "59", type=constants.TYPE_MURLOC, is_premium=self.is_premium)

def Tisse_cristal(self):
    Boost_other(self, "60", type=constants.TYPE_DEMON, is_premium=self.is_premium)

def Assistant_arcanique(self):
    Boost_other(self, "61", type=constants.TYPE_ELEMENTAL, is_premium=self.is_premium)

def Canonnier(self):
    Boost_other(self, "62", type=constants.TYPE_PIRATE, is_premium=self.is_premium)

def Emissaire_du_crepuscule(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_DRAGON)
    if minion:
        self.create_and_apply_enchantment("63", is_premium=self.is_premium)

def Voyant_froide_lumiere(self):
    Boost_other(self, "64", type=constants.TYPE_MURLOC, is_premium=self.is_premium)

def Maitre_chien(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_BEAST)
    if minion:
        minion.create_and_apply_enchantment("65", is_premium=self.is_premium)

def Surveillant_Nathrezim(self):
    minion = self.owner.owner.minion_choice(self.owner, self, restr=constants.TYPE_DEMON)
    if minion:
        minion.create_and_apply_enchantment("66", is_premium=self.is_premium)

def Menagerie_1(self):
    Bonus_ménagerie(self, "67")

def Menagerie_2(self):
    Bonus_ménagerie(self, "68")

def Elementaire_de_stase(self):
    player = self.owner.owner
    elem_lst = [minion
        for minion in player.bob.hand.cards_of_tier_max(player.level)
            if minion.type & constants.TYPE_ELEMENTAL]
    for _ in range(self.double_if_premium(1)):
        if self.owner.opponent.can_add_card() and elem_lst:
            elem = random.choice(elem_lst)
            elem_lst.remove(elem)
            elem.play(board=self.owner.opponent)
            elem.state |= constants.STATE_FREEZE

def Bonus_ménagerie(self, key_effect):
    minion_list = list(self.owner.one_minion_by_type())
    random.shuffle(minion_list)
    for minion in minion_list[:3]:
        minion.create_and_apply_enchantment(key_effect, is_premium=self.is_premium)

def Lapin(self):
    self.create_and_apply_enchantment("69", is_premium=self.is_premium, nb=self.owner.owner.nb_lapin)

def Boost_other(self, effect_key, type=constants.TYPE_ALL, nb_max=constants.BATTLE_SIZE, is_premium=None):
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
    for servant in self.owner:
        if servant.is_type(constants.TYPE_DRAGON):
            servant.state_fight |= constants.STATE_DIVINE_SHIELD

def Goldrinn(self):
    Boost_all(self, "70", constants.TYPE_BEAST, is_premium=False)

def Goldrinn_p(self):
    Boost_all(self, "70", constants.TYPE_BEAST, is_premium=True)

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
    legendary_cards = [key
        for key, value in self.bob.card_can_collect.items()
            if value['rarity'] == constants.RARITY_LEGENDARY]

    script_functions.invocation_random_list(self, legendary_cards, 1)

def Sneed_p(self):
    legendary_cards = [key
        for key, value in self.bob.card_can_collect.items()
            if value['rarity'] == constants.RARITY_LEGENDARY]

    script_functions.invocation_random_list(self, legendary_cards, 2)

def Goliath_brisemer(self, target):
    Boost_other(self, "71", type=constants.TYPE_PIRATE, is_premium=self.is_premium)

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
            if value["type"] & constants.TYPE_DEMON]

    for _ in range(self.double_if_premium(1)):
        repop_id = script_functions.invocation_random_list(self, demon_cards, 1)
        if repop_id:
            repop_id.state_fight |= constants.STATE_TAUNT

def Forgeronne_des_tarides(self):
    if self.has_frenzy:
        self.remove_state(constants.STATE_FRENZY)
        for minion in self.owner:
            if minion != self:
                minion.create_and_apply_enchantment("72", is_premium=self.is_premium)

def Chef_du_gang_des_diablotins(self):
    script_functions.invocation(self, "300a", 1)

def Chef_du_gang_des_diablotins_p(self):
    script_functions.invocation(self, "300a_p", 1)

def Rover_de_securite(self):
    script_functions.invocation(self, "410a", 1)

def Rover_de_securite_p(self):
    script_functions.invocation(self, "410a_p", 1)

def GroBoum(self):
    potential_targets = [minion
        for minion in self.owner.opponent
            if minion.is_alive]

    if potential_targets:
        target = random.choice(potential_targets)
        self.owner.owner.fight.create_single_damage_event(self, target, 4)

def GroBoum_p(self):
    for _ in range(2):
        GroBoum(self)

def Rejeton(self):
    Boost_all(self, "73", is_premium=False)

def Rejeton_p(self):
    Boost_all(self, "73", is_premium=True)

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
        random.choice(cibles_potentielles).state_fight |= constants.STATE_DIVINE_SHIELD

def Héroïne_altruiste_p(self):
    for _ in range(2):
        Héroïne_altruiste(self)

def Serviteur_diabolique(self):
    if self.owner:
        random.choice(self.owner).create_and_apply_enchantment("79", a=self.attack, is_premium=False)

def Serviteur_diabolique_p(self):
    for _ in range(2):
        Serviteur_diabolique(self)

def Goule_instable(self):
    for minion in self.owner+self.owner.opponent:
        self.owner.owner.fight.create_single_damage_event(self, minion, 1)

def Goule_instable_p(self):
    for _ in range(2):
        Goule_instable(self)

def Aile_de_mort(self, minion):
    minion.create_and_apply_enchantment("313", is_premium=False, origin=self, type='aura')

def Chauffard_huran(self):
    if self.has_frenzy:
        self.remove_state(constants.STATE_FRENZY)
        for _ in range(self.double_if_premium(1)):
            self.owner.owner.hand.create_card("1014")

def Defense_robuste(self, enchantment, target):
    if target is self and enchantment.key_number == "500":
        if self.is_premium:
            self.create_and_apply_enchantment('85', is_premium=False)
        else:
            self.create_and_apply_enchantment('84', is_premium=False)

def Brute_dos_hirsute_a(self):
    self.quest_value = 0

def Brute_dos_hirsute(self, enchantment, target):
    if target is self and enchantment.key_number == "500" and self.quest_value == 0:
        self.quest_value = 1
        self.enchantment[-1].a += 2*self.double_if_premium(1)
        self.enchantment[-1].h += 2*self.double_if_premium(1)

def Mande_epines(self):
    for _ in range(self.double_if_premium(1)):
        self.owner.owner.hand.create_card("1014")

def Mande_epines_d(self):
    self.owner.owner.hand.create_card("1014")

def Mande_epines_d_p(self):
    for _ in range(2):
        Mande_epines_d(self)

def Necrolyte(self):
    minion = self.owner.owner.minion_choice(self.owner, self)
    if minion:
        for neighbour in minion.adjacent_neighbors():
            change = False
            for enchantment in neighbour.enchantment[::-1]:
                if enchantment.key_number == '500':
                    minion.apply_enchantment_on(enchantment)
                    change = True
            if change:
                neighbour.calc_stat_from_scratch()
        minion.calc_stat_from_scratch()

def Porte_banniere_huran(self):
    for neighbour in self.adjacent_neighbors():
        if neighbour.type & constants.TYPE_QUILBOAR:
            for _ in range(self.double_if_premium(1)):
                neighbour.create_and_apply_enchantment('500', is_premium=False)

def Cogneur(self):
    self.owner.owner.hand.create_card("1014")

def Duo_dynamique(self, enchantment, target):
    if target != self and enchantment.key_number == "500" and target.type & constants.TYPE_QUILBOAR:
        self.create_and_apply_enchantment('81', is_premium=self.is_premium)

def Tremble_terre(self, enchantment, target):
    if self is target and enchantment.key_number == "500":
        for minion in self.owner:
            minion.create_and_apply_enchantment('82', is_premium=self.is_premium)

def Chevalier_dos_hirsute(self):
    if self.has_frenzy:
        self.remove_state(constants.STATE_FRENZY)
        self.state_fight |= constants.STATE_DIVINE_SHIELD

def Aggem_malepine(self, enchantment, target):
    if self is target and enchantment.key_number == "500":
        for minion in self.owner.one_minion_by_type():
            minion.create_and_apply_enchantment('83', is_premium=self.is_premium)

def Agamaggan(self):
    self.owner.add_aura(self, boost_blood_gem=self.double_if_premium(1))

def Charlga(self):
    nb_gem = self.double_if_premium(1)
    for minion in self.owner:
        if minion != self:
            for _ in range(nb_gem):
                minion.create_and_apply_enchantment('500', is_premium=False)

def Capitaine_Plate_Defense(self):
    self.owner.add_aura(self, spend_gold=1, check='Capitaine_Plate_Defense_check')

def Capitaine_Plate_Defense_check(self):
    while self.quest_value >= 3:
        self.quest_value -= 3
        for _ in range(self.double_if_premium(1)):
            self.owner.owner.hand.create_card("1014")

def wake_up(self):
    # Maeiv effect
    self.create_and_apply_enchantment('315')
    self.owner.opponent.owner.hand.append(self)

def Prophete_du_sanglier(self):
    if self.quest_value == 0:
        self.quest_value = 1
        self.owner.owner.hand.create_card("1014")

def Prophete_du_sanglier_a(self):
    self.quest_value = 0
