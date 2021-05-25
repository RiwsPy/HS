
import matplotlib.pyplot as plt
import constants
import card
import player
import math
import re
import bob
import power
import random
from collections import defaultdict
fact = math.factorial

combin = lambda n,k: fact(n)//(fact(k)*fact(n-k))

def hypgeo(k,n,g,t):
    """hypgeo(k,n,g,t): prob d'avoir k réussites dans un échantillon de taille n,
    sachant qu'il y en a g dans la population de taille t"""
    return combin(g,k)*combin(t-g,n-k)/combin(t,n)

def binom(k,n,p):
    """binom(k,n,p): probabilité d'avoir k réussite(s) dans n évènements indépendants,
    chaque évènement ayant une probabilité p% de réussite"""
    x=combin(n,k)*p**k*(1-p)**(n-k)
    return x

def esperance(note_lst, proba_lst):
    cumul = 0
    for note, proba in zip(note_lst, proba_lst):
        cumul += note*proba

    return cumul


def amalgadon():
    nb_calc = 21
    nb_type = list(range(nb_calc))
    proba1 = adapt_calc1(nb_calc)
    proba2 = adapt_calc2(nb_calc)
    p1, = plt.plot(nb_type, proba1, '-g')
    p2, = plt.plot(nb_type, proba2, '-b')
    p4, = plt.plot(nb_type, [0, 0, 0, 0.0117, 0.0381, 0.0778, 0.1279, 0.1851, 0.2462, 0.3087, 0.3706, 0.4304, 0.4872, 0.5403, 0.5894, 0.6344, 0.6753, 0.7123, 0.7455, 0.7753, 0.8018], '-r')
    p1.set_label('1 bonus')
    p2.set_label('2 bonus')
    p4.set_label('3 bonus')
    plt.legend()
    plt.xlabel("Nombre d'adaptation")
    plt.ylabel('Probabilité de réussite (%)')
    plt.suptitle(f"Obtenir X bonus spécifiques sur Amalgadon")
    plt.grid(True)
    plt.show()

def adapt_calc1(nb_lancer = 20):
    lst = [0]
    for i in range(1, nb_lancer):
        lst.append(1-binom(0, i, 1/8))
    return lst

def adapt_calc2(nb_lancer = 20):
    # option n°2
    #proba_ini = 1/8*2/8
    #for i in range(20):
    #result = mult2(i)*proba_ini/8**i
    #lst.append(result+lst[-1])
    lst = [0, 0, 2/8*1/8]
    for n in range(1, nb_lancer-2):
        result = 0
        for j in range(n+1):
            result += 2/8*(6/8)**(n-j)*(7/8)**j
        lst.append(result*1/8+lst[-1])
    return lst

def adapt_calc3(nb_lancer = 20): # TODO : semble asymptomatique en 0.6, anormal, remplacée par un calcul manuel
    lst = [0, 0, 0]
    for n in range(nb_lancer-3): # n = 4 : range(1, 2)
        distri = [n, 0, 0]
        result = 0
        for j in range(len(distri)):
            if n == 0:
                result = (2/8)*(3/8)
            else:
                for k in range(n):
                    result += (7/8)**distri[0]*(6/8)**distri[1]*(5/8)**distri[2]*(2/8)*(3/8)
                    if distri[j]:
                        distri[j] -= 1
                        distri[(j+1)%3] += 1
            if not distri[(j+1)%3]:
                break

        lst.append(result*1/8+lst[-1])
    return lst


def lapin(bob):
    # tri de la bdd par level / type ?
    # recherche d'un cri de guerre T2 dans une taverne 2
    lst_card = bob.card_can_collect
    nb_card = bob.nb_card_of_tier_max(2)

    # pour les joueurs sans avantages
    proba_roll  = 1-hypgeo(0, constants.NB_CARD_BY_LEVEL[2], constants.CARD_NB_COPY[2], nb_card)
    # pour Aranna après 5 rolls
    proba_aranna  = 1-hypgeo(0, constants.NB_CARD_BY_LEVEL_ARANNA[2], constants.CARD_NB_COPY[2], nb_card)

    
    nb_battlecry = 0
    for minion, info in lst_card.items():
        minion_level = int(info["level"])
        if minion_level <= 2 and info.get("script") and info["script"].get("0x1"):
            nb_battlecry += constants.CARD_NB_COPY[minion_level]

    proba_brann_power = 1-hypgeo(0, constants.NB_CARD_BY_LEVEL[2], constants.CARD_NB_COPY[2], nb_battlecry)

    po_max = 20
    po = list(range(po_max+1))

    # hero sans avantages
    proba_cumul = [proba_roll]
    po_this_turn = 6
    po_restant = 5
    for i in range(po_max):
        if po_this_turn == po_restant: # roll gratuit
            proba_cumul.append(proba_cumul[-1] + proba_roll*2)
            po_this_turn += 1
        else:
            proba_cumul.append(proba_cumul[-1] + proba_roll)
        po_restant -= 1
        if po_restant == 0:
            po_restant = po_this_turn

    # Nozdormu
    proba_cumul_noz = [proba_roll*2]
    po_this_turn = 6
    po_restant = 5
    for i in range(po_max):
        if po_this_turn == po_restant: # roll gratuit
            proba_cumul_noz.append(proba_cumul_noz[-1] + proba_roll*3)
            po_this_turn += 1
        else:
            proba_cumul_noz.append(proba_cumul_noz[-1] + proba_roll)
        po_restant -= 1
        if po_restant == 0:
            po_restant = po_this_turn


    # Aranna
    proba_cumul_aranna = [proba_roll]
    po_this_turn = 6
    po_restant = 5
    proba = proba_roll
    for i in range(po_max):
        if i >= 4:
            proba = proba_aranna

        if po_this_turn == po_restant: # roll gratuit
            proba_cumul_aranna.append(proba_cumul_aranna[-1] + proba*2)
            po_this_turn += 1
        else:
            proba_cumul_aranna.append(proba_cumul_aranna[-1] + proba)

        po_restant -= 1
        if po_restant == 0:
            po_restant = po_this_turn

    # Brann
    proba_cumul_brann = [proba_roll]
    po_this_turn = 6
    po_restant = 5
    for i in range(po_max):
        if po_this_turn == po_restant+1: # hero power
            proba_cumul_brann.append(proba_cumul_brann[-1] + proba_roll + proba_brann_power)
            po_this_turn += 1
        else:
            proba_cumul_brann.append(proba_cumul_brann[-1] + proba_roll)
        po_restant -= 1
        if po_restant == 0:
            po_restant = po_this_turn


    normal, = plt.plot(po, proba_cumul, '-b')
    normal.set_label('Héros standard')
    noz, = plt.plot(po, proba_cumul_noz, '-y')
    noz.set_label('Nozdormu')
    aranna, = plt.plot(po, proba_cumul_aranna, '-m')
    aranna.set_label('Aranna')
    brann, = plt.plot(po, proba_cumul_brann, '-g')
    brann.set_label('Brann')
    plt.legend()
    plt.xlabel("PO investies dans le roll")
    plt.ylabel('Probabilité cumulée de réussite')
    #plt.suptitle(f"Types bannis : {type_ban[0]} - {type_ban[1]}")
    plt.grid(True)
    plt.text(0, 0, "T3")
    plt.text(5, 0, "T4")
    plt.text(11, 0, "T5")
    plt.text(18, 0, "T6")
    plt.show()

def test():
    plt.plot([1, 2, 3, 4, 5, 6], constants.CARD_NB_COPY[1:], '-g')
    plt.xlabel('Niveau de taverne')
    plt.ylabel('Nombre de cartes')
    plt.show()

def mult():
    lst = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    result = 0

    for index0 in range(8-lst[0]):
        for index1 in range(8-lst[0]):
            for index2 in range(8-lst[1]):
                for index3 in range(8-lst[2]):
                    for index4 in range(8-lst[3]):
                        for index5 in range(8-lst[4]):
                            for index6 in range(8-lst[5]):
                                for index7 in range(8-lst[6]):
                                    for index8 in range(8-lst[7]):
                                        for index9 in range(8-lst[8]):
                                            for index10 in range(8-lst[9]):
                                                for index11 in range(8-lst[10]):
                                                    for index12 in range(8-lst[11]):
                                                        for index13 in range(8-lst[12]):
                                                            for index14 in range(8-lst[13]):
                                                                for index15 in range(8-lst[14]):
                                                                    for index16 in range(8-lst[15]):
                                                                        mul = 1
                                                                        for value in lst:
                                                                            mul *= value
                                                                        result += mul
                                                                        print(lst)
                                                                        lst[16] += 1
                                                                    lst[15] += 1
                                                                    for index in range(16, len(lst)):
                                                                        lst[index] = lst[15]
                                                                lst[14] += 1
                                                                for index in range(15, len(lst)):
                                                                    lst[index] = lst[14]
                                                            lst[13] += 1
                                                            for index in range(14, len(lst)):
                                                                lst[index] = lst[13]
                                                        lst[12] += 1
                                                        for index in range(13, len(lst)):
                                                            lst[index] = lst[12]
                                                    lst[11] += 1
                                                    for index in range(12, len(lst)):
                                                        lst[index] = lst[11]
                                                lst[10] += 1
                                                for index in range(11, len(lst)):
                                                    lst[index] = lst[10]
                                            lst[9] += 1
                                            for index in range(10, len(lst)):
                                                lst[index] = lst[9]
                                        lst[8] += 1
                                        for index in range(9, len(lst)):
                                            lst[index] = lst[8]
                                    lst[7] += 1
                                    for index in range(8, len(lst)):
                                        lst[index] = lst[7]
                                lst[6] += 1
                                for index in range(7, len(lst)):
                                    lst[index] = lst[6]
                            lst[5] += 1
                            for index in range(6, len(lst)):
                                lst[index] = lst[5]
                        lst[4] += 1
                        for index in range(5, len(lst)):
                            lst[index] = lst[4]
                    lst[3] += 1
                    for index in range(4, len(lst)):
                        lst[index] = lst[3]
                lst[2] += 1
                for index in range(3, len(lst)):
                    lst[index] = lst[2]
            lst[1] += 1
            for index in range(2, len(lst)):
                lst[index] = lst[1]
        lst[0] += 1
        for index in range(1, len(lst)):
            lst[index] = lst[0]

    print(result)

def mult2(lenght=17):
    result = 0
    for i in range(lenght+1):
        result += 6**(lenght-i)*7**i

    return result

def proportion_type(bob, type_search=constants.TYPE_PIRATE):
    # calcule la proportion de pirate selon le niveau de taverne et les types bannis
    # nb_pirate / nb_carte
    different_type = {0: [], 1: [], 2:[], 4: [], 8: [], 16: [], 32: [], 64: []}

    for typ in different_type:
        for level in range(1, 7):
            cards = bob.card_synergy_by_level(typ, tier_max=level, tier_min=level)
            different_type[typ].append(len(cards)*constants.CARD_NB_COPY[level])

    result = {}
    for type_ban_1 in different_type:
        if not type_ban_1 or type_ban_1 == type_search:
            continue

        for type_ban_2 in different_type:
            if not type_ban_2 or type_ban_2 == type_search or type_ban_2 <= type_ban_1:
                continue

            type_ban_name = constants.TYPE_NAME[type_ban_1] + '/' + constants.TYPE_NAME[type_ban_2]
            result[type_ban_name] = []

            for level in range(1, 7):
                a = 0
                b = sum(different_type[type_search][0:level])
                for typ, value in different_type.items():
                    if not typ & (type_ban_1+type_ban_2):
                        a += sum(value[0:level])
                result[type_ban_name].append(constants.NB_CARD_BY_LEVEL[level]*b/a)

    color = ['#FF0000', '#00FF00', '#0000FF', '#191970', '#00FFFF', '#FF00FF', '#808080', '#FF8C00',
        '#B8860B', '#66CDAA', '#800080', '#FFFF00', '#000000', '#008080', '#808000']

    for nb, (name, info) in enumerate(result.items()):
        a, = plt.plot(list(range(1, 7)), info, color=color[nb])
        a.set_label(name)

    plt.title(f"Espérance d'obtention d'un serviteur de type {constants.TYPE_NAME[type_search]} selon le niveau de taverne et les types bannis")
    plt.legend()
    plt.grid(True)
    plt.show()


def nb_script(bob, script=0, version=1, calcul="%", num_version="1.0", state=None):
    # % d'obtenir des cris de guerres dans la taverne selon les types bannis et le niveau de taverne
    # version 1 : résultat pour Bếte et Démon absents
    # version 2 : les autres
    # calcul : "%" ou "E", probabilité d'obtention ou Espérance

    different_type = {0x1:[[0, 0]], 0x2:[[0, 0]], 0x4:[[0, 0]],
                    0x8:[[0, 0]], 0x10:[[0, 0]], 0x20:[[0, 0]], 
                    0x40:[[0, 0]], 0x0:[[0, 0]]}
    for type in different_type:
        nb_card_of_type = 0
        nb_battlecry = 0
        for level in range(1, 7):
            cards = bob.card_synergy_by_level(type, tier_max=level, tier_min=level)
            nb_card_of_type += len(cards)*constants.CARD_NB_COPY[level]
            for crd in cards.values():
                if script and 'script' in crd and crd["script"].get(script) or\
                        state and crd.get('init_state', 0) & state:
                    nb_battlecry += constants.CARD_NB_COPY[level]

            different_type[type].append([nb_card_of_type, nb_battlecry])

    lst = {}
    types = [0x0, 0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40]
    for level in range(1, 7):
        for index, type_ban1 in enumerate(types[1:]):
            for type_ban2 in types[index+2:]:
                ban_name = constants.TYPE_NAME[type_ban1] + '/' + constants.TYPE_NAME[type_ban2]
                if level == 1:
                    lst[ban_name] = [[0, 0]]
                population = 0
                population_cri = 0
                for type in types:
                    if type != type_ban1 and type != type_ban2:
                        population += different_type[type][level][0]
                        population_cri += different_type[type][level][1]
                lst[ban_name].append([population, population_cri])

    tavern = [1, 2, 3, 4, 5, 6]
    result = []
    result_name = []
    for count, (key, info) in enumerate(lst.items()):
        result.append([])
        result_name.append(key)
        for level in tavern:
            if calcul == "%":
                result[count].append(1- hypgeo(0, constants.NB_CARD_BY_LEVEL[level], info[level][1], info[level][0]))
            elif calcul == "E":
                # nb_card_par_roll*nb_carte_recherchées/nb_card
                result[count].append(constants.NB_CARD_BY_LEVEL[level]*info[level][1]/info[level][0])

    if version == 1:
        add = 0
    else:
        add = 11

    a, = plt.plot(tavern, result[0+add], color = '#FF0000')
    a.set_label(result_name[0+add])
    b, = plt.plot(tavern, result[1+add], color = '#00FF00')
    b.set_label(result_name[1+add])
    c, = plt.plot(tavern, result[2+add], color =  '#0000FF')
    c.set_label(result_name[2+add])
    d, = plt.plot(tavern, result[3+add], color = '#191970')
    d.set_label(result_name[3+add])
    e, = plt.plot(tavern, result[4+add], color = '#00FFFF')
    e.set_label(result_name[4+add])
    f, = plt.plot(tavern, result[5+add], color = '#FF00FF')
    f.set_label(result_name[5+add])
    g, = plt.plot(tavern, result[6+add], color = '#808080')
    g.set_label(result_name[6+add])
    h, = plt.plot(tavern, result[7+add], color = '#FF8C00')
    h.set_label(result_name[7+add])
    i, = plt.plot(tavern, result[8+add], color = '#B8860B')
    i.set_label(result_name[8+add])
    j, = plt.plot(tavern, result[9+add], color = '#66CDAA')
    j.set_label(result_name[9+add])
    if version == 1:
        k, = plt.plot(tavern, result[10], color = '#800080')
        k.set_label(result_name[10])
    plt.legend()

    plt.xlabel("Niveau de taverne")
    if script == constants.EVENT_BATTLECRY:
        if calcul == "%":
            plt.ylabel("Probabilité d'obtention d'au moins un cri de guerre (%)")
            plt.title("Probabilité d'obtention d'un cri de guerre selon le niveau de taverne et les types bannis")
        elif calcul == "E":
            plt.ylabel("Espérance du nombre de cri de guerre")
            plt.title("Espérance d'obtention d'un cri de guerre selon le niveau de taverne et les types bannis")
    elif script == constants.EVENT_DEATHRATTLE:
        if calcul == "%":
            plt.ylabel("Probabilité d'obtention d'au moins un râle d'agonie (%)")
            plt.title("Probabilité d'obtention d'un râle d'agonie selon le niveau de taverne et les types bannis")
        elif calcul == "E":
            plt.ylabel("Espérance du nombre de râle d'agonie")
            plt.title("Espérance d'obtention d'un râle d'agonie selon le niveau de taverne et les types bannis")
    elif not script:
        # C'Thun: 3 états principaux au T6 (taverne 3) pour obtenir un bouclier divin en 3 rolls (+1)
        # 1 seul bouclier présent (ban méca/dragon, méca/élem, dragon/elem) : 28.5% (E: 0.08/roll)
        # 2 boucliers divins : 46% (E : 0.14/roll)
        # 3 boucliers divins : 63% (E : 0.23/roll)
        # 4 boucliers divins : 76% (E : 0.3/roll)
        if calcul == "%":
            plt.ylabel(f"Probabilité d'obtention d'au moins un {constants.STATE_NAME[state]} (%)")
            plt.title(f"Probabilité d'obtention d'un {constants.STATE_NAME[state]} selon le niveau de taverne et les types bannis")
        elif calcul == "E":
            plt.ylabel(f"Espérance du nombre de {constants.STATE_NAME[state]}")
            plt.title(f"Espérance d'obtention d'un {constants.STATE_NAME[state]} selon le niveau de taverne et les types bannis")

    plt.grid(True)
    plt.show()

def average_card(bob, typ=type):
    # moyenne de carte de type typ et de niveau maximal level_tavern
    nb_card_of_level = bob.nb_card_of_tier_max(1)
    different_type = ["0x1", "0x2", "0x4", "0x8", "0x10", "0x20", "0x40"]
    nb_card_of_type = []
    for tp in different_type:
        nb = len(bob.card_synergy_by_level(tp, tier_max=1))
        nb_card_of_type.append(nb)

    population = 0
    for index, type_ban1 in enumerate(different_type):
        if type_ban1 != typ:
            for index2, type_ban2 in enumerate(different_type[index+1:]):
                if type_ban2 != typ:
                    population += nb_card_of_level - nb_card_of_type[index] - nb_card_of_type[index2]
    nb_tirage = ((len(different_type)-1)*(len(different_type)-2))/2
    population_average = population/nb_tirage # population arrondie au supérieur = :/

    return 1-hypgeo(0, 3, nb_card_of_type[typ], math.ceil(population_average))

def card_type_card_t1():
    cards = bob.Bob(type_ban=0)
    # probabilité d'obtenir une carte d'un certain type au T1
    different_type = ["Bête", "Démon", "Dragon", "Elémentaire", "Méca", "Murloc", "Pirate"]
    lst = [average_card(cards, type)
        for type in different_type]

    plt.bar(different_type, lst)
    plt.xlabel("Type de serviteur")
    plt.ylabel("Probabilité d'obtention T1 (%)")
    plt.grid(True)
    plt.show()

def buy_all_elem():
    # type_ban: 0x3, héros 'classique'
    # {1: 4.082, 2: 2.992, 3: 3.118, 4: 3.124, 5: 3.29, 6: 3.736}

    # type_ban: 0x3, Millhouse
    # {1: 4.022, 2: 2.934, 3: 3.258, 4: 3.24, 5: 3.188, 6: 3.952}

    # type_ban: 0x3, Aranna
    # {1: 6.188, 2: 4.038, 3: 4.068, 4: 3.71, 5: 4.034, 6: 3.826}

    # type_ban: 0x3, Nozdormu
    # {1: 4.348, 2: 3.506, 3: 3.436, 4: 3.426, 5: 3.682, 6: 3.898}

    # type_ban: 0x3, Brann avec utilisation du pouvoir/tour
    # {1: 3.742, 2: 3.026, 3: 3.338, 4: 3.444, 5: 3.64, 6: 4.096}

    # type_ban: 0x3, Toki avec utilisation du pouvoir/tour
    # {1: 3.94, 2: 3.178, 3: 3.234, 4: 3.304, 5: 3.272, 6: 3.512}

    BOB = bob.Bob(type_ban=0x3)
    j1 = player.Player(BOB, 'rivvers', 'Toki')
    j2 = player.Player(BOB, 'notoum', '')
    BOB.go_party(j1, j2)
    #j1.power = power.Power(6, j1)

    lvl_result = {}
    for lvl in range(1, 7):
        j1.level = lvl
        lvl_result[lvl] = 0
        result = []
        for _ in range(500):
            cont = True
            BOB.begin_turn()
            j1.gold = 10
            nb_elem = 0
            while cont:
                for minion in j1.hand[::-1]:
                    minion.play()
                    if minion.type & constants.TYPE_ELEMENTAL:
                        nb_elem += 1
                    minion.trade()

                for key in ('517', '117', '324', '118'):
                    # partiellement faux, un elem 517 rajouté via un élem de stase ne sera pas prioritaire
                    for minion in j1.board.opponent[::-1]:
                        if j1.can_buy_minion(): # par ordre de priorité
                            if minion.key_number == key:
                                minion.trade()
                                minion.play()
                                minion.trade()
                                nb_elem += 1
                                break
                for minion in j1.board.opponent[::-1]:
                    if j1.can_buy_minion():
                        if minion.type & constants.TYPE_ELEMENTAL:
                            minion.trade()
                            minion.play()
                            minion.trade()
                            nb_elem += 1
                            break
                if not j1.can_buy_minion():
                    cont = False
                    result.append(nb_elem)
                    BOB.end_turn()
                else:
                    if j1.power.id in (14, 50) and not j1.power.is_disabled: # Brann, Toki
                        j1.power.active_manual()
                    else:
                        j1.roll()
        lvl_result[lvl] = sum(result)/len(result)
    print(lvl_result)

if __name__ == "__main__":
    cards = bob.Bob(0x3)
    #nb_script(cards, script=constants.EVENT_DEATHRATTLE, version=2, calcul="%", num_version="19.6")
    #nb_script(cards, script=None, version=1, calcul="E", num_version="19.6", state=constants.STATE_DIVINE_SHIELD)
    #proportion_type(cards, type_search=constants.TYPE_ELEMENTAL)
    #buy_all_elem()
