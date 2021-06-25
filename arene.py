from db_card import Card_data
import game
from constants import Type
import time
import json
import stats
from entity import Entity, Meta_card_data
from datetime import datetime
from typing import Dict

compo_turn_3 = { # by synergy
    Type.ALL: ('38797', '65661', '64040'), # rejeton, ritualiste tourmenté, goutte d'eau
    Type.BEAST: ('39481', '59940'), # gentille grand mère, chef de meute
    Type.DEMON: ('59937', '59186'), # emprisonneur, surveillant Nathrezim
    Type.DRAGON: ('61029', '60621'), # gardien des glyphes, régisseur du temps
    Type.ELEMENTAL: ('64056', '64296', '64040'), # élémentaire en fête, roche en fusion, goutte
    Type.MECH: ('49279', '778'), # groboum, golem des moissons
    Type.MURLOC: ('1063', '736'), # chef de guerre, vieux troubloeil
    Type.PIRATE: ('61060', '680'), # yo-ho, capitaine des mers du sud
    Type.QUILBOAR: ('70153', '70162'), # prophète du sanglier, défense robuste
}

class arene:
    def __init__(self, **kwargs) -> None:
        self.debut = time.time()
        self.type_ban = kwargs['type_ban']
        self.g = game.Game(type_ban=self.type_ban, is_arene=True, no_bob=True)
        self.version = self.g.version
        self.method = kwargs['method']

        with open('db_arene.json', 'r') as file:
            dic = json.load(file)
        self.db_arene = dic
        self.init_dic()
        self.p1 = self.g.card_db[kwargs['p1']]
        self.p2 = self.g.card_db[kwargs['p2']]
        self.retro = kwargs['retro']

        self.dic_add = {'kwargs': kwargs}

        self.begin()


    def begin(self):
        if search_in_dict(self.db_arene[self.version][self.method], **self.dic_add):
            print(f'retro {self.retro} déjà existante.')
            return None
        print(f'retro {self.retro} en cours...')

        if self.retro >= 1:
            self.dic_add['kwargs']['retro'] -= 1
            cards_test = self.load_card_rating(self.dic_add, self.method)
            self.dic_add['kwargs']['retro'] += 1
        else:
            cards_test = Meta_card_data()

        result, player_level = getattr(self, self.method)(cards_test, p1=self.p1, p2=self.p2)

        for card in result:
            if card.counter:
                card.value /= card.counter
            else:
                print('ERROR', card.name, card.counter, card.value)

        self.db_arene[self.version][self.method][str(datetime.now())] = self.dic_add
        if self.p1 in ('59805', '66196'):
            value_lst = [card.value for card in result]
            esp = round(stats.esperance(value_lst, [1/len(result)]*len(result)), 4)
        else:
            esp = round(stats.rating_esperance(result, player_level=player_level), 4)
        self.dic_add['espérance'] = esp
        self.dic_add['rating'] = ordered_rating(result)

        self.save_json()

        fin = time.time()
        print(fin-self.debut)

    def load_card_rating(self, dic_add: dict, method) -> Meta_card_data:
        cards_test = Meta_card_data()
        stat_data = search_in_dict(self.db_arene[self.version][method], **dic_add)
        if stat_data:
            for card_dbfId, card_rating in stat_data['rating'].items():
                crd = self.g.card_db[card_dbfId.split('_')[0]]
                crd.rating = card_rating
                cards_test.append(crd)
        else:
            print(f'Retro {self.retro} de {method} introuvable.')

        return cards_test

    def save_json(self):
        with open('db_arene.json', 'w', encoding='utf8') as file:
            json.dump(self.db_arene, file, indent=1, ensure_ascii=False)

    def init_dic(self):
        dic = self.db_arene
        version = self.version
        method = self.method
        if version not in dic:
            dic[version] = {}
            dic[version][method] = {}
        elif method not in dic[version]:
            dic[version][method] = {}

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
                for _ in range(NB_FIGHT):
                    g.party_begin('rivvers', 'notoum', hero_p1=hero_p1, hero_p2=hero_p2)
                    j1, j2 = g.players
                    for nb in range(2):
                        g.begin_turn()
                        j1.power.active_script_arene(card_p1)
                        j2.power.active_script_arene(card_p2)
                        g.end_turn()
                        g.begin_fight()
                        g.end_fight()

                    card_p1.value += \
                        calc_damage(j1, j2)*proba_apparition_p2
                    card_p1.counter += proba_apparition_p2

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
                        g.begin_fight()
                        g.end_fight()

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
        cards_T2 = self.load_card_rating({'kwargs':
                        {"method": "base_T3",
                        "type_ban": self.type_ban,
                        "retro": 1,
                        "p1": "aaa",
                        "p2": "aaa"}},
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
                        g.begin_fight()
                        g.end_fight()

                        card_p1.counter += proba_c2
                        card_p1.value += calc_damage(j1, j2)*proba_c2

    def base_T2_to_T3(self, cards_test, p1, p2):
        cards_test = cards_test or self.g.card_can_collect.filter(level=1)
        self.fight_base_T2_to_T3(cards_test, p1, p2)

        cards_list = self.load_card_rating({'kwargs':
                {"method": "base_T3",
                "type_ban": self.type_ban,
                "retro": 2,
                "p1": "aaa",
                "p2": "aaa"}},
                method = 'base_T3')

        # mousse du pont
        esp_without_roll = stats.esperance_2_cards(cards_list, 4, 0)
        esp_with_roll = stats.esperance_2_cards(cards_list, 4, 1)
        cards_list['61055'].value += (esp_with_roll - esp_without_roll)*cards_list['61055'].counter

        # anomalie actualisante
        esp_with_roll = stats.esperance_2_cards_with_free_roll(cards_list, 4)[0]
        cards_list['64042'].value += (esp_with_roll - esp_without_roll)*cards_list['64042'].counter

        return cards_test, 1


    def fight_base_T2_to_T3(self, card_list, hero_p1, hero_p2):
        g = self.g
        NB_FIGHT = 1

        for synergy in compo_turn_3.copy():
            if not synergy & self.g.type_present:
                del compo_turn_3[synergy]
        #cards_T2 = self.g.card_can_collect.filter_maxmin_level(level_max=2)

        cards_T1_to_T3 = self.load_card_rating({'kwargs':
                        {"method": "base_T1_to_T3_no_refound",
                        "type_ban": self.type_ban,
                        "retro": 0,
                        "p1": "aaa",
                        "p2": "aaa"}},
                        method = 'base_T1_to_T3_no_refound')
        for card in cards_T1_to_T3:
            self.g.card_db[card].T1_to_T3_rating = card.rating

        cards_T2 = self.load_card_rating({'kwargs':
                        {"method": "base_T3",
                        "type_ban": self.type_ban,
                        "retro": 2,
                        "p1": "aaa",
                        "p2": "aaa"}},
                        method = 'base_T3')
        if not cards_T2:
            return

        for card_p1 in [self.g.card_db["64042"]]: # card_list
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
                            g.begin_fight()
                            g.end_fight()

                            card_p1.counter += proba_c2*proba_c3
                            card_p1.value += calc_damage(j1, j2)*proba_c2*proba_c3


    def base_T1_to_T3_extended(self, cards_test, p1, p2):
        if self.retro == 0:
            cards_test = self.load_card_rating({'kwargs':
                            {"method": "base_T2_to_T3",
                            "type_ban": self.type_ban,
                            "retro": 0,
                            "p1": "aaa",
                            "p2": "aaa"}},
                            method = 'base_T2_to_T3')
            # 9.5/5 = 2/2 + 2/4 + 2/5, impact prévisionnel jusqu'au Tour 5
            for card in cards_test:
                card.value = card.rating*9.5/5

            cards_test = self.load_card_rating({'kwargs':
                            {"method": "base_T1",
                            "type_ban": self.type_ban,
                            "retro": 2,
                            "p1": "aaa",
                            "p2": "aaa"}},
                            method = 'base_T1')

            for card in cards_test:
                card.value += card.rating
                card.counter = 1
        else:
            self.fight_base_T1(cards_test, p1, p2)
            for card in cards_test:
                card.value /= card.counter
                card.counter = 1

            cards_test = self.load_card_rating({'kwargs':
                            {"method": "base_T2_to_T3",
                            "type_ban": self.type_ban,
                            "retro": 0,
                            "p1": "aaa",
                            "p2": "aaa"}},
                            method = 'base_T2_to_T3')
            for card in cards_test:
                card.value += card.rating*9.5/5

        return cards_test, 1

    def test_esperance(self, cards_test, p1, p2):
        return cards_test



    def fight_base_T1_to_T3_x(self, card_list, hero_p1, hero_p2):
        g = self.g
        NB_FIGHT = 1

        for synergy in compo_turn_3.copy():
            if not synergy & self.g.type_present:
                del compo_turn_3[synergy]

        #cards_T1 = g.card_can_collect.filter(level=1)
        cards_T1 = [g.card_db['976'],
                    g.card_db['40426'],
                    g.card_db['64038'],
                    g.card_db['70147'],
                    g.card_db['70143'],
                    g.card_db['68469']]
        cards_T1_other = [card
                for card in g.card_can_collect.filter(level=1)
                    if card not in cards_T1]

        for card_p1 in cards_T1:
            generator_p2 = stats.card_proba(
                            card_list,
                            player_level=2)
            for card_p1_2, proba_p1_2 in generator_p2:
                generator_p2_2 = stats.card_proba(
                                card_list,
                                player_level=2,
                                exclude_card=[card_p1_2])
                for card_p1_3, proba_p1_3 in generator_p2_2:
                    for compo in compo_turn_3.values():
                        for _ in range(NB_FIGHT):
                            g.party_begin('rivvers', 'notoum', hero_p1=hero_p1, hero_p2=hero_p2)
                            j1, j2 = g.players
                            g.begin_turn()
                            j1.power.active_script_arene(card_p1)
                            j2.power.active_script_arene('68469')
                            g.end_turn()
                            g.begin_turn()
                            j1.power.active_script_arene()
                            j2.power.active_script_arene()
                            g.end_turn()
                            g.begin_turn()
                            j1.power.active_script_arene(card_p1_2, card_p1_3)
                            j2.power.active_script_arene(*compo)
                            g.end_turn()
                            g.begin_fight()
                            g.end_fight()

                            damage_value = calc_damage(j1, j2)
                            proba_mult = proba_p1_2*proba_p1_3/NB_FIGHT
                            if card_p1 == '68469':
                                for card in cards_T1_other:
                                    card.counter_2 += proba_mult
                                    card.value_2 += damage_value*proba_mult
                                    card_p1_2.counter += proba_mult
                                    card_p1_3.counter += proba_mult
                                    card_p1_2.value += damage_value*proba_mult
                                    card_p1_3.value += damage_value*proba_mult
                            else:
                                card_p1.counter_2 += proba_mult
                                card_p1.value_2 += damage_value*proba_mult
                                card_p1_2.counter += proba_mult
                                card_p1_3.counter += proba_mult
                                card_p1_2.value += damage_value*proba_mult
                                card_p1_3.value += damage_value*proba_mult

        return card_list

def ordered_rating(result: Meta_card_data) -> Dict[Card_data, int]:
    result.sort('value', reverse=True)
    return {card_id + '_' + card_id.name: round(card_id.value, 2)
        for card_id in result}

def calc_damage(p1: Entity, p2: Entity) -> int:
    return (p2.max_health - p2.health)*3/5 / (p2.max_health/40) - \
        (p1.max_health - p1.health)*5/3 / (p1.max_health/40)

def search_in_dict(data: dict, **kwargs) -> dict:
    for info_stat in data.values():
        if info_stat.get('kwargs') == kwargs['kwargs']:
            return info_stat
    return {}

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


if __name__ == '__main__':
    arene(method='base_T1_to_T3_extended', type_ban=0, retro=2, p1="aaa", p2="aaa") #61910
