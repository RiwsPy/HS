# chargement des cartes selon les types bannis
# mouvement au tour par tour
# choix des cartes, soit précis (ElémentPlus) soit vague (Meilleure stat)
# calcul des probas de réalisation

import player
import combat
from operator import itemgetter
import random
import math
import board
import card
import bob
from collections import defaultdict

def compo_name(player):
    return '_'.join([minion.name for minion in player.board])

def arene_default():
    # pour T1 seulement
    # les deux joueurs ne levelup pas T2
    # les cartes ont un poids égal
    BOB = bob.Bob(type_ban=0)
    j1 = player.Player(BOB, 'J1', '')
    j1.power.hero_script = 'No_level_up'
    j2 = player.Player(BOB, 'J2', '')
    j2.power.hero_script = 'No_level_up'
    j1.is_bot = True
    j2.is_bot = True
    BOB.go_party(j1, j2)
    all_cards = BOB.card_of_tier_max(tier_max=1)
    result = {1: {}, 2: {}}

    for j1_card_key_number in all_cards:
        for j2_card_key_number in all_cards:
            j1.initialize()
            j2.initialize()
            j1_hp = j1.hp
            j2_hp = j2.hp
            BOB.nb_turn = 0
            BOB.begin_turn(no_bob=True)
            j1.hand.create_card(j1_card_key_number)
            for card in j1.hand[::-1]:
                card.play()
            j2.hand.create_card(j2_card_key_number)
            for card in j2.hand[::-1]:
                card.play()
            compo_name_j1 = compo_name(j1)
            compo_name_j2 = compo_name(j2)
            if compo_name_j1 not in result[BOB.nb_turn]:
                result[BOB.nb_turn][compo_name_j1] = defaultdict(int)
                result[BOB.nb_turn][compo_name_j1]['compo'] = [j1_card_key_number]
            if compo_name_j2 not in result[BOB.nb_turn]:
                result[BOB.nb_turn][compo_name_j2] = defaultdict(int)
                result[BOB.nb_turn][compo_name_j2]['compo'] = [j2_card_key_number]
            result[BOB.nb_turn][compo_name_j1]['nb_match'] += 1
            result[BOB.nb_turn][compo_name_j2]['nb_match'] += 1
            BOB.end_turn()
            result[BOB.nb_turn][compo_name_j1]['damage_recu_cumul'] += (j1_hp - j1.hp)
            result[BOB.nb_turn][compo_name_j2]['damage_recu_cumul'] += (j2_hp - j2.hp)

            champ = combat.Combat(j1, j2)
            gagnant, damage = champ.fight_initialisation()
            if gagnant:
                if gagnant == j1:
                    result[BOB.nb_turn][compo_name_j2]['damage_recu_cumul'] += damage
                    result[BOB.nb_turn][compo_name_j1]['damage_inflige_cumul'] += damage
                else:
                    result[BOB.nb_turn][compo_name_j1]['damage_recu_cumul'] += damage
                    result[BOB.nb_turn][compo_name_j2]['damage_inflige_cumul'] += damage

    # chaque combat est effectué deux fois, soit 578 combats par compo
    for j1_card_key_number in all_cards:
        for j2_card_key_number in all_cards:
            for j1_card_key_number_2 in all_cards:
                for j2_card_key_number_2 in all_cards:
                    j1.initialize()
                    j2.initialize()
                    BOB.nb_turn = 0
                    BOB.begin_turn(no_bob=True)
                    j1.hand.create_card(j1_card_key_number)
                    for card in j1.hand[::-1]:
                        card.play()
                    j2.hand.create_card(j2_card_key_number)
                    for card in j2.hand[::-1]:
                        card.play()
                    BOB.end_turn()
                    j1_hp = j1.hp
                    j2_hp = j2.hp
                    compo_name_j1_T1 = compo_name(j1)
                    compo_name_j2_T1 = compo_name(j2)
                    BOB.begin_turn(no_bob=True)

                    #j1.hand.create_card(j1_card_key_number)
                    j1.hand.create_card(j1_card_key_number_2)
                    for card in j1.hand[::-1]:
                        card.play()
                    #j2.hand.create_card(j2_card_key_number)
                    j2.hand.create_card(j2_card_key_number_2)
                    for card in j2.hand[::-1]:
                        card.play()
                    compo_name_j1 = compo_name(j1)
                    compo_name_j2 = compo_name(j2)
                    if compo_name_j1 not in result[BOB.nb_turn]:
                        result[BOB.nb_turn][compo_name_j1] = defaultdict(int)
                        result[BOB.nb_turn][compo_name_j1]['compo'] = [j1_card_key_number, j1_card_key_number_2]
                    if compo_name_j2 not in result[BOB.nb_turn]:
                        result[BOB.nb_turn][compo_name_j2] = defaultdict(int)
                        result[BOB.nb_turn][compo_name_j2]['compo'] = [j2_card_key_number, j2_card_key_number_2]
                    result[BOB.nb_turn][compo_name_j1]['nb_match'] += 1
                    result[BOB.nb_turn][compo_name_j2]['nb_match'] += 1
                    BOB.end_turn()
                    result[BOB.nb_turn][compo_name_j1]['damage_recu_cumul'] += result[1][compo_name_j1_T1]['damage_recu_cumul']/result[1][compo_name_j1_T1]['nb_match'] + (j1_hp - j1.hp)
                    result[BOB.nb_turn][compo_name_j2]['damage_recu_cumul'] += result[1][compo_name_j2_T1]['damage_recu_cumul']/result[1][compo_name_j2_T1]['nb_match'] + (j2_hp - j2.hp)
                    result[BOB.nb_turn][compo_name_j1]['damage_inflige_cumul'] += result[1][compo_name_j1_T1]['damage_inflige_cumul']/result[1][compo_name_j1_T1]['nb_match']
                    result[BOB.nb_turn][compo_name_j2]['damage_inflige_cumul'] += result[1][compo_name_j2_T1]['damage_inflige_cumul']/result[1][compo_name_j2_T1]['nb_match']

                    champ = combat.Combat(j1, j2)
                    gagnant, damage = champ.fight_initialisation()
                    if gagnant:
                        if gagnant == j1:
                            result[BOB.nb_turn][compo_name_j2]['damage_recu_cumul'] += damage
                            result[BOB.nb_turn][compo_name_j1]['damage_inflige_cumul'] += damage
                        else:
                            result[BOB.nb_turn][compo_name_j1]['damage_recu_cumul'] += damage
                            result[BOB.nb_turn][compo_name_j2]['damage_inflige_cumul'] += damage

    new_format_1 = [[compo_name, 
            info['damage_recu_cumul']/info['nb_match']*7-info['damage_inflige_cumul']/info['nb_match'],
            info['damage_recu_cumul']/info['nb_match'],
            -info['damage_inflige_cumul']/info['nb_match'],
            info['compo']]
        for compo_name, info in result[1].items()]

    new_format_2 = [[compo_name, 
            info['damage_recu_cumul']/info['nb_match']*7-info['damage_inflige_cumul']/info['nb_match'],
            info['damage_recu_cumul']/info['nb_match'],
            -info['damage_inflige_cumul']/info['nb_match'],
            info['compo']]
        for compo_name, info in result[2].items()]

    stats_1 = sorted(new_format_1, key=itemgetter(1, 2, 3))
    stats_2 = sorted(new_format_2, key=itemgetter(1, 2, 3))

    with open('test_T1.txt', 'w') as file:
        for info in stats_1:
            file.write(f'{info[0]}: DR moyen: {round(info[2], 2)} ; DI moyen: {round(info[3], 2)} ; Note: {round(info[1], 2)}\n')

    with open('test_T2.txt', 'w') as file:
        for info in stats_2:
            file.write(f'{info[0]}: DR moyen: {round(info[2], 2)} ; DI moyen: {round(info[3], 2)} ; Note: {round(info[1], 2)}\n')

    # calcul du meilleur choix T1, facultatif
    result_by_minion = defaultdict(list)
    for info in stats_2:
        for key_number in info[4]:
            card = BOB.card_can_collect.get(key_number)
            if card:
                result_by_minion[card['name']].append(info[1])
                break

    moyenne_by_minion = [[minion_name, round(sum(result)/len(result), 2)]
        for minion_name, result in result_by_minion.items()]

    stats_3 = sorted(moyenne_by_minion, key=itemgetter(1))
    with open('test_T1.txt', 'a') as file:
        file.write('\n\nRésultat des meilleurs choix T1 pour un no level_up T2 :\n\n')
        for info in stats_3:
            file.write(f'{info[0]}: note moyenne {info[1]}\n')


    # calcul du meilleur choix T2, facultatif
    result_by_minion = defaultdict(list)
    for info in stats_2:
        for key_number in info[4][::-1]:
            card = BOB.card_can_collect.get(key_number)
            if card:
                result_by_minion[card['name']].append(info[1])
                break

    moyenne_by_minion = [[minion_name, round(sum(result)/len(result), 2)]
        for minion_name, result in result_by_minion.items()]

    stats_4 = sorted(moyenne_by_minion, key=itemgetter(1))
    with open('test_T1.txt', 'a') as file:
        file.write('\n\nRésultat des meilleurs choix T2 pour un no level_up T2 :\n\n')
        for info in stats_4:
            file.write(f'{info[0]}: note moyenne {info[1]}\n')


# note : l'influence de la PO du token doit être intégré dans les synergies
# jouer le mousse du pont n'a aucun avantage lors du T1 et ne devrait pas augmenter sa côte
def arene_pondere(players, key_lst, proba_lst, nb_turn, pr=True):
    """
        *param players: list of player.Player
        *param key_lst: list of card key_number
        *param proba_lst: list of percentage of occurence for each card
        *param pr: print the result if True
    """
    stats = []
    result = {}
    j1, j2, j3, j4 = players[:4]
    bob = j1.bob
    nb_minion = len(key_lst[0])

    for card_key in key_lst[0]:
        bob.go_party(*players)
        bob.begin_turn(no_bob=True, recursive=False)
        j1.force_buy_card(card_key)

        compo_name = []
        compo_key = []
        for minion in j1.board:
            compo_name.append(minion.name)
            compo_key.append(minion.key_number)
        compo_name = '_'.join(compo_name)

        result[compo_name] = {"nb_match":nb_minion, "damage_recu_cumul":(j1.init_hp - j1.hp)*100,
            "damage_inflige_cumul":0, "PO":calcul_PO(j1), "compo":compo_key}

        for key_j2, key_j3, proba_j2, proba_j3 in \
                zip(key_lst[1], key_lst[2], proba_lst[1], proba_lst[2]):

            #result[compo_name]["nb_match"] += 1
            bob.go_party(*players)

            bob.begin_turn(no_bob=True, recursive=False)
            j1.force_buy_card(card_key)
            j2.force_buy_card(key_j2)
            j3.force_buy_card(key_j3)
            bob.end_turn()

            for opponent, proba in zip((j2, j3), (proba_j2, proba_j3)):

                champ = combat.Combat(j1, opponent)
                gagnant, damage = champ.fight_initialisation()
                # résultats * proba d'obtention de la compo adverse
                damage *= proba*100

                if gagnant:
                    if gagnant == j1:
                        result[compo_name]["damage_inflige_cumul"] += damage
                    else:
                        result[compo_name]["damage_recu_cumul"] += damage

                j1.next_opponent = j3

                bob.begin_turn(no_bob=True, recursive=False)
                bob.end_turn()

    #print(f"\nClassement des cartes pour {players[0].pseudo} :")
    stats = []
    for key, value in result.items():
        nb_match = value["nb_match"]/len(key_lst[0])*100

        average_damage_recu = 0
        if value["damage_recu_cumul"]:
            average_damage_recu = round(value["damage_recu_cumul"]/nb_match, 2) # moyenne des dégâts reçus

        average_damage_inflige = 0
        if value["damage_inflige_cumul"]:
            average_damage_inflige = round(value["damage_inflige_cumul"]/nb_match, 2) # moyenne des dégâts reçus

        average_PO = value["PO"]
        note = round(-average_damage_recu*7+average_damage_inflige+average_PO*0, 2)
        stats.append([key, note, average_damage_recu, average_damage_inflige, average_PO, value["compo"]])

    stats = sorted(stats,key=itemgetter(1, 2, 3, 4), reverse=True)
    if pr:
        print(f"Choix pour {j1.hero.name} contre {j2.hero.name}, Tour {nb_turn} :", file=open("output.txt", "a"))
        for nb, id in enumerate(stats):
            if id[1] >= 0:
                note = "+" + str(id[1])
            else:
                note = str(id[1])
            print(f"{nb+1}. {id[0].ljust(40)} {note.ljust(6)}; DR {str(id[2]).ljust(4)} ; DI {str(id[3]).ljust(4)} ; PO {id[4]}", file=open("output.txt", "a"))
        print('\n', file=open("output.txt", "a"))

    return list(stats)

def calcul_PO(player):
    while player.hand or player.board:
        for minion in player.hand[::-1]:
            minion.play()
            minion.trade()
        for minion in player.board[::-1]:
            minion.trade()

    return player.gold+player.nb_free_roll-player.level_up_cost


if __name__ == "__main__":
    pass
