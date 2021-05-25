from collections import defaultdict
import combat
from operator import itemgetter
import json
import random
import player
import constants

def arene(BOB, *players, TIER_MAX=6, TIER_MIN=1, pr=True, nb_turn=1, proba_dict={}):
    NB_FIGHT = 5 # faire un tour/random ?
    BOB.arene = True

    lst_card_can_collect = BOB.card_of_tier_max(tier_max=TIER_MAX)

    j1, j2 = players[:2]
    j1 = player.Player(BOB, j1.pseudo, j1.hero.key)
    j2 = player.Player(BOB, j2.pseudo, j2.hero.key)
    j3 = player.Player(BOB, 'test1', '')
    j4 = player.Player(BOB, 'test2', '')
    j3.power.hero_script = 'Random_card_T2'
    j4.power.hero_script = 'Random_card_T2'
    result = {}

    # proba linéaire pour j1
    long = 1/len(lst_card_can_collect)
    default_dict_proba = {minion: long
        for minion in lst_card_can_collect}
    if not proba_dict:
        proba_dict[j2.pseudo] = default_dict_proba
    proba_dict[j1.pseudo] = default_dict_proba

    # proba pondérée pour j3, j4
    lst_default_choice = ['116', '101', '111', '100', '113', '105', '112', '118', '109',
        '107', '117', '114', '104', '103', '110', '108', '102']
    lst_default_choice = [key_number
            for key_number in lst_default_choice
                if key_number in lst_card_can_collect]
    lst_default_proba = j3.pick_best_card(lst_default_choice)
    default_dict_proba = {key_number: proba
        for key_number, proba in zip(lst_default_choice, lst_default_proba)}

    proba_dict[j3.pseudo] = default_dict_proba
    proba_dict[j4.pseudo] = default_dict_proba

    for plyr in (j1, j2, j3, j4):
        plyr.is_bot = True
        result[plyr.pseudo] = {}
        for card_test, info in lst_card_can_collect.items():
            result[plyr.pseudo][card_test] = defaultdict(int)
            result[plyr.pseudo][card_test]['name'] = info['name']

    for card_test in lst_card_can_collect:
        j1.card_sauv = card_test
        for enemy_card in lst_card_can_collect:
            j2.card_sauv = enemy_card
            for other_card in lst_card_can_collect:
                j3.card_sauv = other_card
                j4.card_sauv = other_card
                for _ in range(NB_FIGHT):
                    #a = len(BOB.hand)
                    BOB.go_party(j1, j2, j3, j4)

                    for _ in range(nb_turn):
                        BOB.begin_turn(recursive=False, no_bob=True)
                        for playr in (j1, j2, j3, j4):
                            playr.hp = playr.init_hp # pv réinit à chaque round pour éviter les cumuls
                            playr.power.active_script_arene(playr.card_sauv)
                        BOB.end_turn()

                        if BOB.nb_turn == 1:
                            champ = combat.Combat(j1, j2)
                            gagnant, damage = champ.fight_initialisation()
                            result = save_result(j1, j2, result, gagnant, damage, proba_dict)
                        elif BOB.nb_turn == 2:
                            champ = combat.Combat(j1, j3)
                            gagnant, damage = champ.fight_initialisation()
                            result = save_result(j1, j3, result, gagnant, damage, proba_dict)

                            champ = combat.Combat(j2, j4)
                            gagnant, damage = champ.fight_initialisation()
                            result = save_result(j2, j4, result, gagnant, damage, proba_dict)

                        #if a != len(BOB.hand):
                        #    print(f'1 {card_test}, {enemy_card}, score {a}/{len(BOB.hand)}, {j2.board} {j2.hand}')

    with open('stats_T1.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
    return result

def save_result(j1, j2, result, gagnant, damage, proba_dict):
    proba_real = proba_dict[j1.pseudo][j1.card_sauv] * proba_dict[j2.pseudo][j2.card_sauv]

    result[j1.pseudo][j1.card_sauv]['pv_loss'] += (j1.init_hp - j1.hp)*proba_real
    result[j2.pseudo][j2.card_sauv]['pv_loss'] += (j2.init_hp - j2.hp)*proba_real

    if gagnant:
        if gagnant == j1:
            result[j1.pseudo][j1.card_sauv]['pv_inflict'] += damage*proba_real
            result[j1.pseudo][j1.card_sauv]['nb_win'] += 1*proba_real
            result[j2.pseudo][j2.card_sauv]['pv_loss'] += damage*proba_real
            result[j2.pseudo][j2.card_sauv]['nb_loss'] += 1*proba_real
        else:
            result[j1.pseudo][j1.card_sauv]['pv_loss'] += damage*proba_real
            result[j1.pseudo][j1.card_sauv]['nb_loss'] += 1*proba_real
            result[j2.pseudo][j2.card_sauv]['pv_inflict'] += damage*proba_real
            result[j2.pseudo][j2.card_sauv]['nb_win'] += 1*proba_real
    else:
        result[j1.pseudo][j1.card_sauv]['nb_draw'] += 1*proba_real
        result[j2.pseudo][j2.card_sauv]['nb_draw'] += 1*proba_real

    return result


def arene_T2(BOB, *players, TIER_MAX=6, TIER_MIN=1, pr=True, nb_turn=1, proba_dict={}):
    BOB.arene = True

    lst_card_can_collect = BOB.card_of_tier_max(tier_max=2, tier_min=2)
    cthun = BOB.all_card['116']
    lst_card_can_collect.update({'116': cthun})

    j1, j2 = players[:2]
    j1 = player.Player(BOB, j1.pseudo, j1.hero.key)
    j2 = player.Player(BOB, j2.pseudo, j2.hero.key)
    result = {}

    # proba linéaire pour j1
    long = len(lst_card_can_collect)
    default_dict_proba = {minion: 1/long
        for minion in lst_card_can_collect}
    if not proba_dict:
        proba_dict[j2.pseudo] = default_dict_proba
    proba_dict[j1.pseudo] = default_dict_proba
    j2.is_bot = True

    for plyr in (j1,):
        plyr.is_bot = True
        result[plyr.pseudo] = {}
        for card_test, info in lst_card_can_collect.items():
            result[plyr.pseudo][card_test] = defaultdict(int)
            result[plyr.pseudo][card_test]['name'] = info['name']

    option_j2 = [['213', '223', '117a'], # parieuse, Yo-oh et goutte d'eau
                ['211', '210'], # gardien des glyphes, emprisonneur
                ['223', '201'], # yo-oh, capitaine des mers du sud
                ['101', '202'], # chef de guerre murloc, chasseur rochecave
                ['204', '215'], # saurolisque, golem des moissons
                ['103a', '203', '209']] # chat, gentille grand mère, chef de meute
    for card_test in lst_card_can_collect:
        for card_test2 in lst_card_can_collect:
            j1.card_sauv = [card_test, card_test2]
            for compo_j2 in option_j2:
                j2.card_sauv = compo_j2
                BOB.go_party(j1, j2)
                BOB.begin_turn(recursive=False, no_bob=True)
                #card = j1.hand.create_card(random.choice(lst_card_can_collect))
                #card.play()
                BOB.end_turn()
                BOB.begin_turn(recursive=False, no_bob=True)
                j1.level_up()
                j2.level_up()
                BOB.end_turn()
                BOB.begin_turn(recursive=False, no_bob=True)
                j1.hand.create_card(card_test, card_test2)
                j2.hand.create_card(*compo_j2)
                for card in j1.hand[::-1]:
                    if card.script and constants.EVENT_INVOC in card.script:
                        card.play()
                for card in j1.hand[::-1]:
                    if card.script and constants.EVENT_PLAY in card.script:
                        card.play()
                for card in j1.hand[::-1]:
                    if card.script and constants.EVENT_BATTLECRY not in card.script:
                        card.play()
                for card in j1.hand[::-1]:
                    card.play()
                for card in j2.hand[::-1]:
                    card.play()
                BOB.end_turn()
                champ = combat.Combat(j1, j2)
                gagnant, damage = champ.fight_initialisation()
                result = save_result2(j1, j2, result, gagnant, damage)

    #with open('stats_T1.json', 'w', encoding='utf-8') as file:
    #    json.dump(result, file, indent=4, ensure_ascii=False)
    truc = [[info['name'], info['pv_loss']*7-info['pv_inflict']]
        for info in result[j1.pseudo].values()]
    truc = sorted(truc, key=itemgetter(1))
    print(truc)

    return result

def save_result2(j1, j2, result, gagnant, damage):
    for card_key_number in j1.card_sauv:
        result[j1.pseudo][card_key_number]['pv_loss'] += (j1.init_hp - j1.hp)

        if gagnant:
            if gagnant == j1:
                result[j1.pseudo][card_key_number]['pv_inflict'] += damage
                result[j1.pseudo][card_key_number]['nb_win'] += 1
            else:
                result[j1.pseudo][card_key_number]['pv_loss'] += damage
                result[j1.pseudo][card_key_number]['nb_loss'] += 1
        else:
            result[j1.pseudo][card_key_number]['nb_draw'] += 1

    return result
