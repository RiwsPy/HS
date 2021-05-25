# coding : utf-8

import combat
import card
import player
import random
import constants
from operator import itemgetter
import stats
import test
import bob
import time
from collections import defaultdict
import compo
import json
import arene


def arene_old(BOB, *players, TIER_MAX=6, TIER_MIN=1):
    stats = defaultdict(list)
    dmg = defaultdict(list)
    NB_TURN = 10 # faire un tour/random ?
    BOB.arene = True

    lst_card_can_collect = BOB.card_of_tier_max(tier_max=TIER_MAX)
    j1, j2 = players
    result = {}
    nb_match = NB_TURN*len(lst_card_can_collect)
    #len_bob_hand = len(BOB.hand)

    for card_test, info in lst_card_can_collect.items():
        card_name = info['name']
        result[card_name] = {}
        result[card_name]['nb_match'] = nb_match
        # pour être dans le même ordre pour tous
        result[card_name]['nb_win'] = 0
        result[card_name]['nb_draw'] = 0
        result[card_name]['nb_loss'] = 0
        result[card_name]['pv_loss'] = 0
        result[card_name]['pv_inflict'] = 0
        for enemy_card in lst_card_can_collect:
            for _ in range(NB_TURN):
                BOB.go_party(j1, j2)
                j1.level = TIER_MAX
                j2.level = TIER_MAX
                BOB.begin_turn(recursive=False, no_bob=True)

                j1.power.active_script_arene(card_test)
                j2.power.active_script_arene(enemy_card)
                BOB.end_turn()

                champ = combat.Combat(j1, j2)
                gagnant, damage = champ.fight_initialisation()

                result[card_name]['pv_loss'] += j1.init_hp - j1.hp
                if gagnant:
                    if gagnant == j1:
                        result[card_name]['pv_inflict'] += damage
                        result[card_name]['nb_win'] += 1
                        stats[card_name].append(1)
                        dmg[card_name].append(j1.hp - j1.init_hp)
                    else:
                        result[card_name]['pv_loss'] += damage
                        result[card_name]['nb_loss'] += 1
                        stats[card_name].append(-1)
                        dmg[card_name].append(j1.hp - j1.init_hp - damage)
                else:
                    result[card_name]['nb_draw'] += 1
                    stats[card_name].append(0)
                    dmg[card_name].append(j1.hp - j1.init_hp)

                #if len_bob_hand != len(BOB.hand):
                #    print(f'1 {card_test}, {enemy_card}, score {len_bob_hand}/{len(BOB.hand)}, {j2.board} {j2.hand}')

    #print(f"\nClassement des cartes pour {j1.pseudo} :")
    dict_to_list = [
        [key,
        round(sum(value)/nb_match, 2), # moyenne résultat
        round(sum(value_dmg)/nb_match, 2), # moyenne dégâts reçus
        round((1-value.count(-1)/nb_match)*100, 2)] # % de victoire + % de match nul
        for (key, value), value_dmg in zip(stats.items(), dmg.values())]

    stats = sorted(dict_to_list, key=itemgetter(1, 3, 2), reverse=True)
    for nb, id in enumerate(stats):
        if id[1] >= 0:
            id[1] = "+" + str(id[1])

        print(f"{(str(nb+1) + '. ' + str(id[0])).ljust(30)} {str(id[1]).ljust(5)} : NL {str(id[3]).ljust(5)} ; DM {id[2]}")

    #with open('stats_T1.json', 'w', encoding='utf-8') as file:
    #    json.dump(result, file, indent=4, ensure_ascii=False)
    return stats

def test_compo(bob, type_ban=0):
    winners = []
    stats = defaultdict(list)
    dmg = defaultdict(list)

    compo = {
        "Gardien_Ritua_Goutte":[["211", 0, 0], ["222", 0, 0], ["117a", 0, 0]],
        "Gardien_Goutte_Tasse":[["211", 0, 0], ["117a", 0, 0], ["217", 0, 0]],
        "Sauro_Meute":[["209", 0, 0], ["215", 0, 0]],
        "Gardien_parieuse":[["211", 0, 0],["213", 0, 0]], # gardien des glyphes, parieuse convaincante
        "Gardien_tasse":[["211", 0, 0],["217", 0, 0]],
        "Boum_Moisson":[["206", 0, 0], ["204", 0, 0]],
        "Rejeton_empri_goutte":[["207", 0, 0],["210", 0, 0],["117a", 0, 0]],
        "Boum_Boum":[["206", 0, 0], ["206", 0, 0]],
        "Boum_Boum_Milli":[["206", 1, 1], ["206", 1, 1]],
        "Gardien_Lieutenant":[["211", 0, 0],["111", 0, 0]],
        "Chasse_marée_chef":[["100", 0, 0],["100a", 0, 0],["202", 0, 0]],
        "Trouble_Chasse_marée*2":[["208", 0, 0],["100", 0, 0],["100", 0, 0],["100a", 0, 0]],
        "Gardien_Régisseur":[["211", 0, 0],["214", 0, 0]],
        "Empri_buff":[["210", 0, 0],["216", 0, 0]],
        "Empri_Empri":[["210", 0, 0],["210", 0, 0]],
        "Moisson_Dent":[["204", 2, 0], ["204", 0, 0]],
        "Héroïne_Sauro":[["215", 0, 0], ["221", 0, 0]],
        "Boom_Sauro":[["215", 0, 0], ["206", 0, 0]],
        "Parieuse_Capitaine":[["213", 0, 0], ["201", 0, 0]],
        "Chat_Boost_Meute":[["209", 0, 0], ["103", 0, 0],["103a", 0, 0]],
        "Chat_Chat_Hyène":[["103", 0, 0],["103a", 0, 0], ["104", 0, 0]],
        "Loup_Hyène":[["203", 0, 0], ["104", 0, 0]],
        "Dent_Empri_Chasse":[["204", 0, 0],["210", 0, 0],["100", 0, 0]],
        "Empri_Dent_Chasse":[["210", 0, 0],["204", 0, 0],["100", 0, 0]],
        "Loup_Chef":[["209", 0, 0], ["203", 0, 0]],
        "Tisse_Empri":[["107", 0, 0], ["210", 0, 0]],
        "Compo_reference_T2":[["213", 0, 0], ["213", 0, 0]],
        "Ara_Clan_rat":[["312", 0, 0], ["305", 0, 0]],
        "Goutte_Elem_Capitaine":[["201", 0, 0], ["219", 0, 0], ["117a", 0, 0]],
        "Goutte_Elem_Empri":[["201", 0, 0], ["210", 0, 0], ["117a", 0, 0]],
        "Homoncule_buff_moisson":[["204", 0, 0], ["105", 2, 2]],
        "Homoncule_buff*2":[["105", 2, 2], ["216", 0, 0]],
        "Goule_goutte_golem":[["205", 0, 0], ["117a", 0, 0], ["204", 0, 0]]
    }
    compo_lst = list(compo)

    j1 = player.Player(bob, "Rivvers", "")
    j2 = player.Player(bob, "notoum", "")
    j1.is_bot = True
    j2.is_bot = True

    for _ in range(10000):
        random_compo_j1 = random.choice(compo_lst)
        random_compo_j2 = random.choice(compo_lst)
        if random_compo_j1 == random_compo_j2:
            continue

        bob.go_party(j1, j2)
        bob.begin_turn(no_bob=True)

        for minion in compo[random_compo_j1]:
            card = j1.hand.create_card(minion[0], atk_bonus=minion[1], def_bonus=minion[2])
            card.play()
        for minion in compo[random_compo_j2]:
            card = j2.hand.create_card(minion[0], atk_bonus=minion[1], def_bonus=minion[2])
            card.play()

        bob.end_turn()

        champ = combat.Combat(j1, j2)
        gagnant, damage = champ.fight_initialisation()

        if gagnant:
            winners.append(gagnant.hero)
            if gagnant == j1:
                stats[random_compo_j1].append(1)
                dmg[random_compo_j1].append(damage)
            else:
                stats[random_compo_j1].append(-1)
                dmg[random_compo_j1].append(-damage)
        else:
            winners.append(None)
            stats[random_compo_j1].append(0)
            dmg[random_compo_j1].append(damage)


    #print(f"\nClassement des cartes pour {j1.pseudo} :")
    dict_to_list = [[key, sum(value)/len(value), sum(dmg[key])/len(dmg[key])]
        for key, value in stats.items()]

    stats = sorted(dict_to_list,key=itemgetter(1, 2), reverse=True)
    for id in stats:
        print(f"{id[0]} : {round(id[1], 2)} (dégâts moyens : {round(id[2], 2)})")

    return stats


if __name__ == "__main__":
    BOB = bob.Bob(type_ban=0)
    #nb = BOB.nb_card_of_tier_max(4)
    # 11 exemplaires T4 dont 2 déjà achetées
    # 50 cartes réparties chez les adversaires dont 2 fois la carte recherchée (+5 et 2 chez moi)
    #nb_cartes_restantes = nb - 50 - 7
    #nb_exemplaires_restants = 11 - 2 - 2
    #ratio_par_roll = nb_cartes_restantes / nb_exemplaires_restants / 5
    #print('moy', ratio_par_roll) # carte en 7 exemplaires # 24.3
    #print('max', nb_cartes_restantes / 9 / 5) # carte en 9 exemplaires # 18.9
    #print('min', nb_cartes_restantes / 5 / 5) # carte en 5 exemplaires # 34

    debut = time.time()

    #test_compo(BOB)

    #compo.arene_default()


    j1 = player.Player(BOB, "Rivvers", "Eudora")
    j2 = player.Player(BOB, "notoum", "George")
    #print(arene.arene(BOB, j1, j2, TIER_MAX=1))
    arene_old(BOB, j1, j2, TIER_MAX=1)
    #result1 = arene.arene_T2(BOB, j1, j2, TIER_MAX=1, nb_turn=2)

    #truc = test.test()
    #truc.test_all(BOB)
    """
    j1 = player.Player(BOB, "Rivvers", "Millificent")
    j2 = player.Player(BOB, "notoum", "Eudora")
    j3 = player.Player(BOB, "mechelou", "Eudora")
    j4 = player.Player(BOB, "loulou", "Rafaam")
    j5 = player.Player(BOB, "Pierre", "Eudora")
    j6 = player.Player(BOB, "Molu", "Neunoeil")
    j1.is_bot = True
    j2.is_bot = True
    j3.is_bot = True
    j4.is_bot = True
    j5.is_bot = True
    j6.is_bot = True
    #j1.best_card_T1(j1, j2, j3, j4, j5, j6, nb_turn=2)

    BOB.go_party(j1, j2, j3, j4, j5, j6)
    BOB.begin_turn()
    """

    #j1.power.active_script(recursive=True)

    """
    player_1 = player.Player(BOB, "Rivvers", "Conservateur")
    player_2 = player.Player(BOB, "Rivvers2", "")
    player_3 = player.Player(BOB, "Rivvers3", "AFK")
    player_4 = player.Player(BOB, "Rivvers4", "AFK")
    player_5 = player.Player(BOB, "Rivvers5", "AFK")
    player_6 = player.Player(BOB, "Rivvers6", "AFK")
    player_7 = player.Player(BOB, "Rivvers7", "AFK")
    player_8 = player.Player(BOB, "Rivvers8", "AFK")
    player_1.is_bot = True
    player_2.is_bot = True

    #BOB.go_party(player_1, player_2, player_3, player_4, player_5, player_6, player_7, player_8)
    BOB.go_party(player_1, player_2)
    bob_board = BOB.boards.copy()
    for player in bob_board:
        player.begin_turn()
    """

    fin = time.time()
    print(fin-debut)
