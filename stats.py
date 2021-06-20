from collections import defaultdict
from db_card import Meta_card_data
import math
from operator import itemgetter
from typing import Generator, Tuple, List
from constants import LEVEL_MAX, CARD_NB_COPY, NB_CARD_BY_LEVEL
fact = math.factorial

combin = lambda n,k: fact(n)//(fact(k)*fact(n-k))

def hypgeo(k, n, g, t) -> int:
    """
        hypgeo(k, n, g, t): probabilité d'avoir k réussite(s) dans un échantillon de taille n,
        sachant qu'il y en a g dans la population de taille t
        moyenne: n*g/t
        variance: n* ((t-n) / (t-1) * (g/t) * (t-g)/t)
    """
    k = min(max(k, 0, n - t + g), n, g)
    return combin(g, k)*combin(t-g, n-k)/combin(t, n)

def binom(k, n, p) -> int:
    """
        binom(k,n,p): probabilité d'avoir k réussite(s) dans n évènements indépendants,
        chaque évènement ayant une probabilité p% de réussite
    """

    return combin(n, k) * p**k * (1-p)**(n-k)

def esperance(note_lst, proba_lst) -> int:
    esp = 0
    for note, proba in zip(note_lst, proba_lst):
        esp += note*proba

    return esp

def rating_esperance(result: Meta_card_data) -> int:
    esp = 0
    for card_id, proba in card_proba(result, player_level=1):
        esp += proba*card_id.value

    return esp

def card_proba(card_list, player_level=LEVEL_MAX, exclude_card=[]) -> Tuple[str, int]:
    # proba d'obtention de chaque carte pour le P2, sachant que P1 a acheté exclude_card
    # card_list contient le dbfId des cartes à prendre en compte
    # cas d'égalité entre 101 et 105 : [['100'], ['101', '105'], ['107']]
    nb_card_in_bob = nb_collectible_card_of_tier_max(card_list, tier_max=player_level) - len(exclude_card)
    cumul_proba = 1

    for card_id in ordered_card_rating(card_list):
        cumul_proba_temp = 0
        for card in card_id:
            nb_temp = card.nb_copy - exclude_card.count(card)
            proba = \
                cumul_proba *(1 - \
                hypgeo(0,
                    NB_CARD_BY_LEVEL[player_level],\
                    nb_temp,
                    nb_card_in_bob))
            cumul_proba_temp += proba
            nb_card_in_bob -= nb_temp
            cumul_proba -= proba

        ret = cumul_proba_temp / len(card_id)
        for card in card_id:
            yield card, ret

    if abs(cumul_proba) > 0.001:
        print(f'proba cumul check : {cumul_proba}') 

def card_proba_equi(card_list, player_level=LEVEL_MAX, exclude_card=[]) -> Tuple[str, int]:
    nb_card_in_bob = nb_collectible_card_of_tier_max(card_list, tier_max=player_level) - len(exclude_card)

    for card_id in card_list:
        for card in card_id:
            yield card, \
                (card.nb_copy - exclude_card.count(card)) \
                / nb_card_in_bob

def card_proba_nozdormu(card_list, player_level=LEVEL_MAX, exclude_card=[]):
    nb_card_in_bob = nb_collectible_card_of_tier_max(card_list, tier_max=player_level) - len(exclude_card)
    cumul_proba = 1

    card_id_to_spwawn_proba = defaultdict(int)
    for card_ids in card_list:
        cumul_proba_temp = 0
        cumul_nb_temp = 0
        if card_ids[0].value < card_ids[0].esp:
            break
        for card in card_ids:
            nb_temp = card.nb_copy - exclude_card.count(card)
            cumul_nb_temp += nb_temp
            cumul_proba_temp += \
                cumul_proba *(1 - \
                hypgeo(0,
                    NB_CARD_BY_LEVEL[player_level],\
                    nb_temp,
                    nb_card_in_bob))

        ret = cumul_proba_temp / len(card_ids)
        for card in card_ids:
            card_id_to_spwawn_proba[card] += ret
        cumul_proba -= cumul_proba_temp
        nb_card_in_bob -= cumul_nb_temp

    for card_id, rating in card_proba(card_list, player_level):
        yield card_id, card_id_to_spwawn_proba[card_id]+rating*cumul_proba


def nb_collectible_card_of_tier_max(card_list, tier_max=LEVEL_MAX, tier_min=1) -> int:
    result = 0
    for card_dbfId in card_list:
        if tier_min <= card_dbfId.level <= tier_max:
            result += card_dbfId.nb_copy
    return result

def ordered_card_rating(data: Meta_card_data) -> Generator:
    """
        [['116'], ['111', '41245'], ...]
    """
    result = defaultdict(list)
    for card_data in data:
        result[card_data.value].append(card_data)

    #print(sorted(result.items(), key=itemgetter(0), reverse=True))
    for _, card_list in sorted(result.items(), key=itemgetter(0), reverse=True):
        yield card_list


if __name__ == '__main__':
    print(hypgeo(0, 3, 16, 16))
