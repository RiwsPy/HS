from collections import defaultdict
from db_card import Meta_card_data
import math
from operator import itemgetter
from typing import Generator, Tuple, List
from enums import LEVEL_MAX, CARD_NB_COPY, NB_CARD_BY_LEVEL
fact = math.factorial

combin = lambda n,k: fact(n)//(fact(k)*fact(n-k))

def hypgeo(k, n, g, t) -> int:
    """
        hypgeo(k, n, g, t): probabilité d'avoir k réussite(s) dans un échantillon de taille n,
        sachant qu'il y en a g dans la population de taille t
        moyenne: n*g/t
        variance: n* ((t-n) / (t-1) * (g/t) * (t-g)/t)
    """
    if g == t:
        return int(bool(k))
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

def rating_esperance(result: Meta_card_data, player_level) -> int:
    esp = 0
    for card_id, proba in card_proba(result, player_level=player_level):
        esp += proba*card_id.value

    return esp

def card_proba(card_list, player_level=LEVEL_MAX, rating_type='', exclude_card=[]) -> Tuple[str, int]:
    # proba d'obtention de chaque carte pour le P2, sachant que P1 a acheté exclude_card
    # card_list contient le dbfId des cartes à prendre en compte
    # cas d'égalité entre 101 et 105 : [['100'], ['101', '105'], ['107']]
    nb_card_in_bob = nb_collectible_card_of_tier_max(card_list, tier_max=player_level) - len(exclude_card)
    cumul_proba = 1
    ret = 0
    proba = 0
    for card_id in ordered_card_rating(card_list, rating_type=rating_type):
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

        ret = cumul_proba_temp / len(card_id) or cumul_proba / len(card_id)
        for card in card_id:
            yield card, ret

    if abs(cumul_proba) > 0.001:
        print(f'proba cumul check : {cumul_proba}')
    if ret == 0:
        print(f'Warning : ret value == 0, {cumul_proba}, {nb_card_in_bob}, {proba}')

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

def ordered_card_rating(data: Meta_card_data, rating_type='') -> Generator:
    """
        [['116'], ['111', '41245'], ...]
    """
    result = defaultdict(list)
    if not rating_type:
        for card_data in data:
            result[card_data.rating].append(card_data)
    else:
        for card_data in data:
            result[card_data.all_rating[rating_type]].append(card_data)

    #print(sorted(result.items(), key=itemgetter(0), reverse=True))
    for _, card_list in sorted(result.items(), key=itemgetter(0), reverse=True):
        yield card_list

def esperance_1_card(card_list, card_by_roll=3, nb_roll=0, _esperance_min=None):
    # 1 carte parmi 3+ cartes
    # équivalent à espérance mais avec possibilité de roll
    card_list.sort('rating')

    combin_cumul = 0
    nb_cumul = 0
    nb_card_checked = 0
    for cote_max in card_list:
        nb_combin = combin(cote_max.nb_copy, card_by_roll)
        if nb_card_checked:
            for nb in range(1, card_by_roll):
                nb_combin += combin(cote_max.nb_copy, card_by_roll-nb)*combin(nb_card_checked, nb)

        combin_cumul += nb_combin
        if _esperance_min is not None:
            nb_cumul += max(cote_max.rating, _esperance_min)*nb_combin
        else:
            nb_cumul += cote_max.rating*nb_combin
        nb_card_checked += cote_max.nb_copy

    esperance = nb_cumul/combin(nb_card_checked, card_by_roll)

    if nb_roll > 0:
        esperance = esperance_1_card(card_list, card_by_roll=card_by_roll, nb_roll=nb_roll-1, _esperance_min=esperance)

    if combin_cumul != combin(nb_card_checked, card_by_roll):
        print('esperance_1_card ERROR combin_cumul')

    return esperance


def esperance_2_cards(card_list, card_by_roll=3, nb_roll=0, _esperance_min=None):
    # 2 cartes parmi 3+ cartes
    card_list.sort('rating')

    combin_cumul = 0
    nb_cumul = 0
    nb_card_checked = 0
    for nb, cote_min in enumerate(card_list):
        for cote_max in card_list[nb:]: # cote_max >= cote_min
            if cote_min.rating == cote_max.rating:
                nb_combin = combin(cote_max.nb_copy, card_by_roll)
                if nb_card_checked:
                    for nb in range(1, card_by_roll-1):
                        nb_combin += combin(cote_max.nb_copy, card_by_roll-nb)*combin(nb_card_checked, nb)
            else:
                nb_combin = cote_max.nb_copy*combin(cote_min.nb_copy, card_by_roll-1)
                if nb_card_checked:
                    for nb in range(1, card_by_roll-1):
                        nb_combin += cote_max.nb_copy*combin(cote_min.nb_copy, card_by_roll-1-nb)*combin(nb_card_checked, nb)
            combin_cumul += nb_combin
            add_rating = cote_min.rating+cote_max.rating
            if _esperance_min is not None:
                add_rating = max(_esperance_min, add_rating)
            nb_cumul += add_rating*nb_combin

        nb_card_checked += cote_min.nb_copy

    esperance = nb_cumul/combin(nb_card_checked, card_by_roll)

    if nb_roll > 0:
        esperance = esperance_2_cards(card_list, card_by_roll=card_by_roll, nb_roll=nb_roll-1, _esperance_min=esperance)

    if combin_cumul != combin(nb_card_checked, card_by_roll):
        print('esperance_2_cards ERROR combin_cumul')

    return esperance


def esperance_2_cards_with_free_roll(card_list, card_by_roll=3):
    card_list.sort('rating')

    esp_moy = esperance_2_cards(card_list, card_by_roll)
    esp_max = esperance_1_card(card_list, card_by_roll)

    combin_cumul = 0
    nb_cumul = 0
    nb_cumul_with_convervation = 0
    nb_cumul_without_conservation = 0
    nb_combin_conservation = 0
    nb_card_checked = 0
    for nb, cote_min in enumerate(card_list):
        for cote_max in card_list[nb:]: # cote_max >= cote_min
            if cote_min.rating == cote_max.rating:
                nb_combin = combin(cote_max.nb_copy, card_by_roll)
                if nb_card_checked:
                    for nb in range(1, card_by_roll-1):
                        nb_combin += combin(cote_max.nb_copy, card_by_roll-nb)*combin(nb_card_checked, nb)
            else:
                nb_combin = cote_max.nb_copy*combin(cote_min.nb_copy, card_by_roll-1)
                if nb_card_checked:
                    for nb in range(1, card_by_roll-1):
                        nb_combin += cote_max.nb_copy*combin(cote_min.nb_copy, card_by_roll-1-nb)*combin(nb_card_checked, nb)

            combin_cumul += nb_combin

            if cote_min.rating >= esp_moy/2: # deux cartes > 1
                nb_combin_conservation += nb_combin
                nb_cumul += (cote_min.rating+cote_max.rating)*nb_combin
                nb_cumul_with_convervation += (cote_min.rating+cote_max.rating)*nb_combin
            elif cote_max.rating < esp_moy - esp_max: # deux cartes < 0.8
                nb_cumul += esp_moy*nb_combin
                nb_cumul_without_conservation += esp_moy*nb_combin
            elif cote_max.rating >= esp_moy/2: # cote_max >= 1
                if cote_min.rating < esp_moy - esp_max:
                    nb_cumul += (cote_max.rating+esp_max)*nb_combin
                    nb_cumul_without_conservation += (cote_max.rating+esp_max)*nb_combin
                else:
                    nb_combin_conservation += nb_combin
                    nb_cumul += (cote_min.rating+cote_max.rating)*nb_combin
                    nb_cumul_with_convervation += (cote_min.rating+cote_max.rating)*nb_combin
            else: # 0.8 < cote_max < 1
                nb_cumul += (cote_max.rating+esp_max)*nb_combin
                nb_cumul_without_conservation += (cote_max.rating+esp_max)*nb_combin

        nb_card_checked += cote_min.nb_copy

    esperance = nb_cumul/combin(nb_card_checked, card_by_roll)
    taux_de_conservation_du_roll = nb_combin_conservation/combin(nb_card_checked, card_by_roll)

    if combin_cumul != combin(nb_card_checked, card_by_roll):
        print(f'esperance_2_cards ERROR combin_cumul {combin_cumul} / {combin(nb_card_checked, card_by_roll)}')

    return esperance, taux_de_conservation_du_roll, esp_moy


def esperance_2_cards_with_free_roll_force(card_list, card_by_roll=3):
    card_list.sort('rating')

    esp_moy = esperance_2_cards(card_list, card_by_roll)
    esp_max = esperance_1_card(card_list, card_by_roll)

    combin_cumul = 0
    nb_cumul = 0
    nb_combin_conservation = 0
    nb_card_checked = 0
    for nb, cote_min in enumerate(card_list):
        for cote_max in card_list[nb:]: # cote_max >= cote_min
            if cote_min.rating == cote_max.rating:
                nb_combin = combin(cote_max.nb_copy, card_by_roll)
                if nb_card_checked:
                    for nb in range(1, card_by_roll-1):
                        nb_combin += combin(cote_max.nb_copy, card_by_roll-nb)*combin(nb_card_checked, nb)
            else:
                nb_combin = cote_max.nb_copy*combin(cote_min.nb_copy, card_by_roll-1)
                if nb_card_checked:
                    for nb in range(1, card_by_roll-1):
                        nb_combin += cote_max.nb_copy*combin(cote_min.nb_copy, card_by_roll-1-nb)*combin(nb_card_checked, nb)

            combin_cumul += nb_combin

            if cote_min.rating >= esp_moy/2: # deux cartes > 1
                nb_combin_conservation += nb_combin
                nb_cumul += (cote_min.rating+cote_max.rating)*nb_combin
            elif cote_max.rating < esp_moy - esp_max: # deux cartes < 0.8
                nb_cumul += esp_moy*nb_combin
            elif cote_max.rating >= esp_moy/2: # cote_max >= 1
                nb_cumul += (cote_max.rating+esp_max)*nb_combin
            else: # 0.8 < cote_max < 1
                nb_cumul += (cote_max.rating+esp_max)*nb_combin

        nb_card_checked += cote_min.nb_copy

    esperance = nb_cumul/combin(nb_card_checked, card_by_roll)
    taux_de_conservation_du_roll = nb_combin_conservation/combin(nb_card_checked, card_by_roll)

    if combin_cumul != combin(nb_card_checked, card_by_roll):
        print('esperance_2_cards ERROR combin_cumul')

    return esperance, taux_de_conservation_du_roll


if __name__ == '__main__':
    print(hypgeo(0, 3, 16, 16))
