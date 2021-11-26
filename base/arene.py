from os import stat
from .enums import VERSION, CardName, Race
from .db_card import Card_data, Meta_card_data, CARD_DB
import time
import json
from . import stats
from .entity import Entity, Card
from datetime import datetime
from typing import DefaultDict, Dict
from .sequence import Sequence
from collections import defaultdict

compo_turn_3 = { # by synergy
    Race('NONE'): (CARD_DB[38797], CARD_DB[38797], CARD_DB[64040]), # rejeton, rejeton, goutte d'eau
    Race('BEAST'): (CARD_DB[70790], CARD_DB[62162]), # rat d'égoût, saurolisque
    Race('DEMON'): (CARD_DB[59937], CARD_DB[59186]), # emprisonneur, surveillant Nathrezim
    Race('DRAGON'): (CARD_DB[61029], CARD_DB[72072], CARD_DB[64040]), # gardien des glyphes, contrebandier dragonnet, goutte d'eau
    Race('ELEMENTAL'): (CARD_DB[64056], CARD_DB[64296], CARD_DB[64040]), # élémentaire de fête, roche en fusion, goutte
    Race('MECHANICAL'): (CARD_DB[49279], CARD_DB[49279]), # groboum, groboum
    Race('MURLOC'): (CARD_DB[1063], CARD_DB[736], CARD_DB[68469]), # chef de guerre, vieux troubloeil, éclaireur #
    Race('PIRATE'): (CARD_DB[61060], CARD_DB[680]), # yo-ho, capitaine des mers du sud
    Race('QUILBOAR'): (CARD_DB[70143], CARD_DB[70162]), # Géomancien, défense robuste
}

class arene:
    def __init__(self, **kwargs) -> None:
        self.debut = time.time()
        self.g = Card(
            CardName.DEFAULT_GAME,
            types_ban=kwargs['types_ban'],
            is_arene=True,
            no_bob=True)
        self.type_ban = self.g.type_ban
        self.version = self.g.version
        self.method = kwargs['method']

        self.db_arene = db_arene(**kwargs)
        self.p1 = self.g.all_cards[kwargs['p1']]
        self.p2 = self.g.all_cards[kwargs['p2']]
        self.retro = kwargs['retro']

        self.dic_add = kwargs
        self.dic_add['p1'] = self.g.all_cards[self.dic_add['p1']]['name']
        self.dic_add['p2'] = self.g.all_cards[self.dic_add['p2']]['name']

        self.begin()

    def begin(self):
        if self.db_arene.search(version=self.version, **self.dic_add):
            print(f'retro {self.retro} déjà existante.')
            return None
        print(f'retro {self.retro} en cours...')

        if self.retro >= 1:
            self.dic_add['retro'] -= 1
            cards_test = self.load_card_rating(self.dic_add, self.method)
            self.dic_add['retro'] += 1
        else:
            cards_test = Meta_card_data()

        result, player_level = getattr(self, self.method)(cards_test, p1=self.p1, p2=self.p2)
        if result is None:
            return None

        for card in result:
            if card.counter:
                card.value /= card.counter
            else:
                print('ERROR', card.name, card.counter, card.value)

        self.db_arene[self.version][self.method][str(datetime.now())] = self.dic_add
        if self.p1 in (59805, 66196):
            value_lst = [card.value for card in result]
            esp = round(stats.esperance(value_lst, [1/len(result)]*len(result)), 4)
        else:
            esp = round(stats.rating_esperance(result, player_level=player_level), 4)
        self.dic_add['espérance'] = esp
        self.dic_add['rating'] = ordered_rating(result)

        self.db_arene.save()

        fin = time.time()
        print(fin-self.debut)

    def load_card_rating(self, dic_add: dict, method) -> Meta_card_data:
        cards_test = Meta_card_data()
        stat_data = self.db_arene.search(version=self.version, **dic_add)
        if stat_data:
            for card_dbfId, card_rating in stat_data['rating'].items():
                crd = self.g.all_cards[int(card_dbfId.partition('_')[0])]
                crd.rating = card_rating
                cards_test.append(crd)
        else:
            print(f'Retro {dic_add["retro"]} de {method} introuvable.')

        return cards_test

    def fight_compo_T3(self, _, p1, p2):
        g = self.g
        NB_FIGHT = 10
        ret = defaultdict(int)
        for race, compo1 in compo_turn_3.items():
            for compo2 in compo_turn_3.values():
                for _ in range(NB_FIGHT):
                    g.party_begin('p1_name', 'p2_name', hero_p1=p1, hero_p2=p2)
                    j1, j2 = g.players
                    j1.level = 2
                    j2.level = 2
                    with Sequence('TURN', g):
                        j1.power.active_script_arene(*compo1, force=True)
                        j2.power.active_script_arene(*compo2, force=True)
                    Sequence('FIGHT', g).start_and_close()

                    ret[compo1] += calc_damage(j1, j2)

        for compo, value in ret.items():
            print(compo, value)

        return None, None

    def base_T1(self, cards_test, p1, p2):
        cards_test = cards_test or self.g.minion_can_collect.filter(level=1)
        self.fight_base_T1(cards_test, p1, p2)

        return cards_test, 1

    def fight_base_T1(self, card_list, hero_p1, hero_p2):
        g = self.g
        NB_FIGHT = 10
        for card_p1 in card_list:
            generator_p2 = stats.card_proba(
                            card_list,
                            player_level=1,
                            exclude_card=[card_p1])
            card_p1.value = 0

            for card_p2, proba_apparition_p2 in generator_p2:
                print(card_p1.name, card_p2.name, proba_apparition_p2)
                for _ in range(NB_FIGHT):
                    g.party_begin('p1_name', 'p2_name', hero_p1=hero_p1, hero_p2=hero_p2)
                    j1, j2 = g.players
                    for _ in range(2):
                        with Sequence('TURN', g):
                            j1.power.active_script_arene(card_p1)
                            j2.power.active_script_arene(card_p2)

                        Sequence('FIGHT', g).start_and_close()

                    card_p1.value += \
                        calc_damage(j1, j2)*proba_apparition_p2
                    card_p1.counter += proba_apparition_p2

    def base_T3(self, cards_test, p1, p2):
        cards_test = cards_test or self.g.minion_can_collect.filter_maxmin_level(level_max=2)
        self.fight_base_T3(cards_test, p1, p2)

        return cards_test, 2

    def fight_base_T3(self, card_list, hero_p1, hero_p2):
        g = self.g
        NB_FIGHT = 3

        for synergy in compo_turn_3.copy():
            if synergy & self.g.type_ban:
                del compo_turn_3[synergy]

        for card_p1 in card_list:
            generator_p2_2 = stats.card_proba(
                            card_list,
                            player_level=2,
                            exclude_card=[card_p1])
            for card_p1_2, proba_c2 in generator_p2_2:
                for compo in compo_turn_3.values():
                    print(card_p1.name, card_p1_2.name)
                    for _ in range(NB_FIGHT):
                        g.party_begin('p1_name', 'p2_name', hero_p1=hero_p1, hero_p2=hero_p2)
                        j1, j2 = g.players
                        Sequence('TURN', g).start_and_close()
                        with Sequence('TURN', g):
                            j1.power.active_script_arene()
                            j2.power.active_script_arene()
                        with Sequence('TURN', g):
                            j1.power.active_script_arene(card_p1, card_p1_2, force=True)
                            j2.power.active_script_arene(*compo, force=True)
                        Sequence('FIGHT', g).start_and_close()

                        card_p1.counter += proba_c2
                        card_p1.value += calc_damage(j1, j2)*proba_c2


    """
    def base_T1_to_T3_no_refound(self, cards_test, p1, p2):
        cards_test = cards_test or self.g.minion_can_collect.filter(level=1)
        self.fight_base_T1_to_T3_no_refound(cards_test, p1, p2)

        return cards_test, 1

    def fight_base_T1_to_T3_no_refound(self, card_list, hero_p1, hero_p2):
        g = self.g
        NB_FIGHT = 3

        for synergy in compo_turn_3.copy():
            if synergy & self.g.type_ban:
                del compo_turn_3[synergy]
        #cards_T2 = self.g.minion_can_collect.filter_maxmin_level(level_max=2)
        cards_T2 = self.load_card_rating(
                        {"method": "base_T3",
                        "type_ban": self.type_ban,
                        "retro": 1,
                        "p1": CardName.DEFAULT_HERO,
                        "p2": CardName.DEFAULT_HERO},
                        method = 'base_T3')
        if not cards_T2:
            return

        for card_p1 in card_list:
            generator_p2 = stats.card_proba(
                            cards_T2,
                            player_level=2,
                            exclude_card=[card_p1])
            for card_p1_2, proba_c2 in generator_p2:
                for compo in compo_turn_3.values():
                    for _ in range(NB_FIGHT):
                        g.party_begin('p1_name', 'p2_name', hero_p1=hero_p1, hero_p2=hero_p2)
                        j1, j2 = g.players
                        g.begin_turn()
                        j1.power.active_script_arene(card_p1)
                        g.end_turn()
                        g.begin_turn()
                        j1.power.active_script_arene()
                        j2.power.active_script_arene()
                        g.end_turn()
                        # retrait de l'impact de l'homoncule
                        j1.health = j1.max_health
                        j2.health = j2.max_health
                        j1.hand.all_in_bob()
                        g.begin_turn()
                        j1.power.active_script_arene(card_p1_2, force=True)
                        j2.power.active_script_arene(*compo, force=True)
                        g.end_turn()
                        g.fight_on()
                        g.fight_off()

                        card_p1.counter += proba_c2
                        card_p1.value += calc_damage(j1, j2)*proba_c2

    def base_T2_to_T3(self, cards_test, p1, p2):
        cards_test = cards_test or self.g.minion_can_collect.filter(level=1)
        self.fight_base_T2_to_T3(cards_test, p1, p2)

        cards_list = self.load_card_rating(
                {"method": "base_T3",
                "type_ban": self.type_ban,
                "retro": 2,
                "p1": CardName.DEFAULT_HERO,
                "p2": CardName.DEFAULT_HERO},
                method = 'base_T3')

        # mousse du pont
        esp_without_roll = stats.esperance_2_cards(cards_list, 4, 0)
        esp_with_roll = stats.esperance_2_cards(cards_list, 4, 1)
        cards_list[61055].value += (esp_with_roll - esp_without_roll)*cards_list[61055].counter

        # anomalie actualisante
        esp_with_roll, conservation_rate, esp_moy = stats.esperance_2_cards_with_free_roll(cards_list, 4)
        cards_list[64042].value += (esp_with_roll - esp_without_roll)*cards_list[64042].counter
        cards_list[64042].esp_moy = esp_moy

        return cards_test, 1


    def fight_base_T2_to_T3(self, card_list, hero_p1, hero_p2):
        g = self.g
        NB_FIGHT = 1

        for synergy in compo_turn_3.copy():
            if synergy & self.g.type_ban:
                del compo_turn_3[synergy]
        #cards_T2 = self.g.minion_can_collect.filter_maxmin_level(level_max=2)

        cards_T1_to_T3 = self.load_card_rating(
                        {"method": "base_T1_to_T3_no_refound",
                        "type_ban": self.type_ban,
                        "retro": 0,
                        "p1": CardName.DEFAULT_HERO,
                        "p2": CardName.DEFAULT_HERO},
                        method = 'base_T1_to_T3_no_refound')
        for card in cards_T1_to_T3:
            self.g.all_cards[card].T1_to_T3_rating = card.rating

        cards_T2 = self.load_card_rating(
                        {"method": "base_T3",
                        "type_ban": self.type_ban,
                        "retro": 2,
                        "p1": CardName.DEFAULT_HERO,
                        "p2": CardName.DEFAULT_HERO},
                        method = 'base_T3')
        if not cards_T2:
            return

        for card_p1 in [self.g.all_cards[64042]]: # card_list
            print(f'{card_p1.name} en cours...')
            generator_p2 = stats.card_proba(
                            cards_T2,
                            player_level=2,
                            exclude_card=[card_p1])
            for card_p1_2, proba_c2 in generator_p2:
                generator_p2_2 = stats.card_proba(
                                cards_T2,
                                player_level=2,
                                exclude_card=[card_p1, card_p1_2])
                for card_p1_3, proba_c3 in generator_p2_2:
                    for compo in compo_turn_3.values():
                        for _ in range(NB_FIGHT):
                            g.party_begin('p1_name', 'p2_name', hero_p1=hero_p1, hero_p2=hero_p2)
                            j1, j2 = g.players
                            j1.power.hero_script = 'Special_arene_base_T2_to_T3'
                            g.begin_turn()
                            j1.power.active_script_arene(card_p1)
                            g.end_turn()
                            g.begin_turn()
                            j1.power.active_script_arene()
                            j2.power.active_script_arene()
                            g.end_turn()
                            # retrait de l'impact de l'homoncule
                            j1.health = j1.max_health
                            j2.health = j2.max_health
                            g.begin_turn()
                            j1.power.active_script_arene(card_p1_2, card_p1_3)
                            j2.power.active_script_arene(*compo, force=True)
                            g.end_turn()
                            g.fight_on()
                            g.fight_off()

                            card_p1.counter += proba_c2*proba_c3
                            card_p1.value += calc_damage(j1, j2)*proba_c2*proba_c3


    def base_T1_to_T3_extended(self, cards_test, p1, p2):
        if self.retro == 0:
            cards_test = self.load_card_rating(
                            {"method": "base_T2_to_T3",
                            "type_ban": self.type_ban,
                            "retro": 0,
                            "p1": CardName.DEFAULT_HERO,
                            "p2": CardName.DEFAULT_HERO},
                            method = 'base_T2_to_T3')
            # 9.5/5 = 2/2 + 2/4 + 2/5, impact prévisionnel jusqu'au Tour 5
            # TODO: valeur sous-évaluée pour l'anomalie actualisante > conservation_rate
            ref_rating = self.g.all_cards[59670]
            for card in cards_test:
                card.value = card.rating*9.5/5

            cards_test = self.load_card_rating(
                            {"method": "base_T1",
                            "type_ban": self.type_ban,
                            "retro": 2,
                            "p1": CardName.DEFAULT_HERO,
                            "p2": CardName.DEFAULT_HERO},
                            method = 'base_T1')

            for card in cards_test:
                card.value += card.rating
                card.counter = 1
        else:
            self.fight_base_T1(cards_test, p1, p2)
            for card in cards_test:
                card.value /= card.counter
                card.counter = 1

            cards_test = self.load_card_rating(
                            {"method": "base_T2_to_T3",
                            "type_ban": self.type_ban,
                            "retro": 0,
                            "p1": CardName.DEFAULT_HERO,
                            "p2": CardName.DEFAULT_HERO},
                            method = 'base_T2_to_T3')
            for card in cards_test:
                card.value += card.rating*9.5/5

        return cards_test, 1
        """

def ordered_rating(result: Meta_card_data) -> Dict[Card_data, int]:
    return {f'{int(card_id.dbfId)}' + '_' + card_id.name: round(card_id.value, 2)
        for card_id in sorted(result, key=lambda x: x.value, reverse=True)}

def calc_damage(p1: Entity, p2: Entity) -> int:
    return (p2.max_health - p2.health)*3/5 / (p2.max_health/40) - \
        (p1.max_health - p1.health)*5/3 / (p1.max_health/40)

def search_value_in_list(value, lst, lon=None):
    if not lst:
        return None
    lon = lon or len(lst)
    if lon <= 1:
        if lst[0] == value:
            return 0
        return None
    middle = lon//2
    if lst[middle] > value:
        return search_value_in_list(value, lst[0:middle], middle)
    elif lst[middle] < value:
        try:
            return search_value_in_list(value, lst[(middle+1):None], lon-middle-1) + 1 + middle
        except TypeError:
            return None
    return middle


class db_arene(dict):
    filename = 'db/arene.json'

    def __init__(self, version=VERSION, method='no_method', **kwargs):
        with open(self.__class__.filename, 'r') as file:
            super().__init__(**json.load(file))

        if version not in self:
            self[version] = {}
            self[version][method] = {}
        elif method not in self[version]:
            self[version][method] = {}

    def search(self, version=VERSION, **kwargs) -> dict:
        for data in self[version][kwargs['method']].values():
            find = True
            for info_name, info_value in kwargs.items():
                if data.get(info_name) != info_value:
                    find = False
                    break
            if find:
                return data
        return {}
        """
        for info_stat in self[version][kwargs['method']].values():
            if info_stat.get('kwargs') == kwargs:
                return info_stat
        return {}
        """

    def search_minion_rate(self, minion, **kwargs) -> int:
        for card, rate in self.search(**kwargs)['rating'].items():
            if minion == card.split('_')[0]:
                return rate
        return 0

    def save(self):
        with open(self.__class__.filename, 'w', encoding='utf8') as file:
            json.dump(self, file, indent=1, ensure_ascii=False)

if __name__ == '__main__':
    """
    db = db_arene()
    print(db.search_minion_rate(63614, **{
     "method": "base_T1",
     "type_ban": 0,
     "retro": 0,
     "p1": CardName.DEFAULT_HERO,
     "p2": CardName.DEFAULT_HERO}))
    """

    arene(method='base_T3', type_ban=0, retro=3,
        p1=CardName.DEFAULT_HERO,
        p2=CardName.DEFAULT_HERO)
