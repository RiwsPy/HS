from db_card import Card_data
import game
from constants import Type
import time
import json
import stats
from entity import Entity, Meta_card_data
from datetime import datetime
from typing import Dict

class arene:
    def __init__(self) -> None:
        self.debut = time.time()
        self.g = game.Game(type_ban=0, is_arene=True, no_bob=True)
        self.version = self.g.version
        self.type_ban = str(Type.ALL - self.g.type_present)

    def fight_retro(self, retro=0, p1='aaa', p2='aaa'):
        g = self.g
        p1 = g.card_db[p1]
        p2 = g.card_db[p2]
        p_default = g.card_db['aaa']
        pr = 'Sortie_tour2_retro_'
        dic = g.db_arene
        self.init_dic()
        if search_in_dict(dic[self.version][self.type_ban], p1=p1.name, p2=p2.name, com=f'{pr}{retro}'):
            print(f'retro {retro} déjà existante.')
            return None
        print(f'retro {retro} en cours...')

        if retro < 1:
            cards_test = g.card_can_collect.filter(level=1)
        else:
            if p1 == 'aaa' and p2 == 'aaa':
                stat_data = search_in_dict(
                    dic[self.version][self.type_ban],
                    p1=p1.name,
                    p2=p2.name,
                    com=f'{pr}{retro-1}')
                if not stat_data:
                    self.fight_retro(retro=retro-1, p1=p1, p2=p2)
                    self.fight_retro(retro=retro, p1=p1, p2=p2)
                    return None
            else:
                stat_data = search_in_dict(
                    dic[self.version][self.type_ban],
                    p1=p_default.name,
                    p2=p_default.name,
                    com=f'Sortie_tour2_retro_2')
                if not stat_data:
                    print('retro introuvable')
                    return None
            cards_test = Meta_card_data()
            for card_dbfId, card_rating in stat_data['rating'].items():
                crd = g.card_db[card_dbfId]
                crd.rating = card_rating
                cards_test.append(crd)

        result = self.fight(cards_test, p1, p2)

        dic_add = {'data': 
            {'p1': p1.name, 'p2': p2.name, 'com': f'{pr}{retro}'}}

        dic[self.version][self.type_ban][str(datetime.now())] = dic_add
        dic_add['espérance'] = round(stats.rating_esperance(result), 4)
        dic_add['rating'] = ordered_rating(result)
        self.save_json()

        fin = time.time()
        print(fin-self.debut)

    def save_json(self):
        with open('db_arene.json', 'w', encoding='utf8') as file:
            json.dump(self.g.db_arene, file, indent=1, ensure_ascii=False)

    def init_dic(self):
        dic = self.g.db_arene
        version = self.version
        type_ban = self.type_ban
        if version not in dic:
            dic[version] = {}
            dic[version][type_ban] = {}
        elif type_ban not in dic[version]:
            dic[version][type_ban] = {}

    def fight(self, card_list, hero_p1, hero_p2):
        g = self.g
        NB_FIGHT = 10
        for card_p1 in card_list:
            generator_p2 = stats.card_proba(
                            card_list,
                            player_level=1,
                            exclude_card=[card_p1])
            card_p1.value = 0

            for card_p2, proba_apparition_p2 in generator_p2:
                proba_apparition_p2 /= NB_FIGHT
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

        return card_list

def ordered_rating(result: Meta_card_data) -> Dict[Card_data, int]:
    result.sort('value', reverse=True)
    return {card_id: round(card_id.value, 2)
        for card_id in result}

def calc_damage(p1: Entity, p2: Entity) -> int:
    return (p2.max_health - p2.health)*3/5 / (p2.max_health/40) - \
        (p1.max_health - p1.health)*5/3 / (p1.max_health/40)

def search_in_dict(data: dict, **kwargs) -> dict:
    for info_stat in data.values():
        if info_stat['data'] == kwargs:
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
        ret = search_value_in_list(value, lst[(middle+1):None], lon-middle-1)
        if ret is not None:
            return ret + middle + 1
        return None
    else:
        return middle


if __name__ == '__main__':
    arene().fight_retro(retro=2, p1="aaa", p2="aaa") #61910


