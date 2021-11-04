from os import stat
from db_card import Card_data
from enums import VERSION, CardName
import time
import json
import stats
from entity import Entity, Card
from datetime import datetime
from typing import Dict
from sequence import Sequence
from db_card import Meta_card_data

"""
compo_turn_3 = { # by synergy
    Race.ALL: (38797, 65661, 64040), # rejeton, ritualiste tourmenté, goutte d'eau
    Race.BEAST: (39481, 59940), # gentille grand mère, chef de meute
    Race.DEMON: (59937, 59186), # emprisonneur, surveillant Nathrezim
    Race.DRAGON: (61029, 60621), # gardien des glyphes, régisseur du temps
    Race.ELEMENTAL: (64056, 64296, 64040), # élémentaire en fête, roche en fusion, goutte
    Race.MECHANICAL: (49279, 778), # groboum, golem des moissons
    Race.MURLOC: (1063, 736), # chef de guerre, vieux troubloeil
    Race.PIRATE: (61060, 680), # yo-ho, capitaine des mers du sud
    Race.QUILBOAR: (70153, 70162), # prophète du sanglier, défense robuste
}
"""

class arene:
    def __init__(self, **kwargs) -> None:
        self.debut = time.time()
        self.type_ban = kwargs['type_ban']
        self.g = Card(
            CardName.DEFAULT_GAME,
            type_ban=self.type_ban,
            is_arene=True,
            no_bob=True)
        self.version = self.g.version
        self.method = kwargs['method']

        self.db_arene = db_arene(**kwargs)
        self.p1 = self.g.card_db[kwargs['p1']]
        self.p2 = self.g.card_db[kwargs['p2']]
        self.retro = kwargs['retro']

        self.dic_add = kwargs
        self.dic_add['p1'] = self.g.card_db[self.dic_add['p1']]['name']
        self.dic_add['p2'] = self.g.card_db[self.dic_add['p2']]['name']

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
                crd = self.g.card_db[int(card_dbfId.partition('_')[0])]
                crd.rating = card_rating
                cards_test.append(crd)
        else:
            print(f'Retro {dic_add["retro"]} de {method} introuvable.')

        return cards_test

    def base_T1(self, cards_test, p1, p2):
        cards_test = cards_test or self.g.card_can_collect.filter(level=1)
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
                    g.party_begin('rivvers', 'notoum', hero_p1=hero_p1, hero_p2=hero_p2)
                    j1, j2 = g.players
                    for _ in range(2):
                        with Sequence('TURN', g):
                            j1.power.active_script_arene(card_p1)
                            j2.power.active_script_arene(card_p2)

                        Sequence('FIGHT', g).start_and_close()

                    card_p1.value += \
                        calc_damage(j1, j2)*proba_apparition_p2
                    card_p1.counter += proba_apparition_p2

    """
    def base_T3(self, cards_test, p1, p2):
        cards_test = cards_test or self.g.card_can_collect.filter_maxmin_level(level_max=2)
        self.fight_base_T3(cards_test, p1, p2)

        return cards_test, 2

    def fight_base_T3(self, card_list, hero_p1, hero_p2):
        g = self.g
        NB_FIGHT = 3

        for synergy in compo_turn_3.copy():
            if not synergy & self.g.type_present:
                del compo_turn_3[synergy]

        for card_p1 in card_list:
            generator_p2_2 = stats.card_proba(
                            card_list,
                            player_level=2,
                            exclude_card=[card_p1])
            for card_p1_2, proba_c2 in generator_p2_2:
                for compo in compo_turn_3.values():
                    for _ in range(NB_FIGHT):
                        g.party_begin('rivvers', 'notoum', hero_p1=hero_p1, hero_p2=hero_p2)
                        j1, j2 = g.players
                        g.begin_turn()
                        g.end_turn()
                        g.begin_turn()
                        j1.power.active_script_arene()
                        j2.power.active_script_arene()
                        g.end_turn()
                        g.begin_turn()
                        j1.power.active_script_arene(card_p1, card_p1_2, force=True)
                        j2.power.active_script_arene(*compo, force=True)
                        g.end_turn()
                        g.fight_on()
                        g.fight_off()

                        card_p1.counter += proba_c2
                        card_p1.value += calc_damage(j1, j2)*proba_c2


    def base_T1_to_T3_no_refound(self, cards_test, p1, p2):
        cards_test = cards_test or self.g.card_can_collect.filter(level=1)
        self.fight_base_T1_to_T3_no_refound(cards_test, p1, p2)

        return cards_test, 1

    def fight_base_T1_to_T3_no_refound(self, card_list, hero_p1, hero_p2):
        g = self.g
        NB_FIGHT = 3

        for synergy in compo_turn_3.copy():
            if not synergy & self.g.type_present:
                del compo_turn_3[synergy]
        #cards_T2 = self.g.card_can_collect.filter_maxmin_level(level_max=2)
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
                        g.party_begin('rivvers', 'notoum', hero_p1=hero_p1, hero_p2=hero_p2)
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
        cards_test = cards_test or self.g.card_can_collect.filter(level=1)
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
            if not synergy & self.g.type_present:
                del compo_turn_3[synergy]
        #cards_T2 = self.g.card_can_collect.filter_maxmin_level(level_max=2)

        cards_T1_to_T3 = self.load_card_rating(
                        {"method": "base_T1_to_T3_no_refound",
                        "type_ban": self.type_ban,
                        "retro": 0,
                        "p1": CardName.DEFAULT_HERO,
                        "p2": CardName.DEFAULT_HERO},
                        method = 'base_T1_to_T3_no_refound')
        for card in cards_T1_to_T3:
            self.g.card_db[card].T1_to_T3_rating = card.rating

        cards_T2 = self.load_card_rating(
                        {"method": "base_T3",
                        "type_ban": self.type_ban,
                        "retro": 2,
                        "p1": CardName.DEFAULT_HERO,
                        "p2": CardName.DEFAULT_HERO},
                        method = 'base_T3')
        if not cards_T2:
            return

        for card_p1 in [self.g.card_db[64042]]: # card_list
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
                            g.party_begin('rivvers', 'notoum', hero_p1=hero_p1, hero_p2=hero_p2)
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
            ref_rating = self.g.card_db[59670]
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
    return {str(card_id) + '_' + card_id.name: round(card_id.value, 2)
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

    arene(method='base_T1', type_ban=0, retro=0,
        p1=CardName.DEFAULT_HERO,
        p2=CardName.DEFAULT_HERO)
