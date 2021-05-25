import math
import random
import player
import bob
import constants
from collections import defaultdict

fact = math.factorial

combin = lambda n,k: fact(n)//(fact(k)*fact(n-k))

def hypgeo(k, n, g, t):
    """hypgeo(k,n,g,t): prob d'avoir k réussites dans un échantillon de taille n,
    sachant qu'il y en a g dans la population de taille t"""
    if g >= t:
        return int(bool(k))
    return combin(g, k)*combin(t-g, n-k)/combin(t, n)

def binom(k, n, p):
    """binom(k,n,p): probabilité d'avoir k réussite(s) dans n évènements indépendants,
    chaque évènement ayant une probabilité p% de réussite"""
    return combin(n, k)*p**k *(1 - p)**(n - k)

def esperance(note_lst, proba_lst):
    cumul = 0
    for note, proba in zip(note_lst, proba_lst):
        cumul += note*proba

    return cumul

def mult_div(value, turn):
    result = value
    for nb in range(1, turn):
        result *= value-nb
    return result


class Stats:
    def __init__(self):
        BOB = bob.Bob(0)
        self.bob = BOB
        self.board_esp = {}
        j1 = player.Player(BOB, 'j1')
        self.player = j1

        BOB.go_party(j1, 
            player.Player(BOB, 'bot1'),
            player.Player(BOB, 'bot2'), 
            player.Player(BOB, 'bot3'), 
            player.Player(BOB, 'bot4'), 
            player.Player(BOB, 'bot5'), 
            player.Player(BOB, 'bot6'),
            player.Player(BOB, 'bot7'))

        self.init_key_cote()

    def init_key_cote(self):
        self.key_cote = {key: info.get('cote', 0)
            for key, info in self.bob.card_can_collect.items()}

    def dict_nb_card_cote_of_tier_max(self, tier_max=1):
        result = defaultdict(int)
        for cards in self.bob.hand[1:tier_max+1]:
            for card in cards:
                result[self.key_cote[card.key_number]] += 1
        return result

    def card_cote(self, key_number):
        if key_number in self.key_cote:
            return self.key_cote[key_number]
        if key_number in self.bob.all_card:
            return self.bob.all_card[key_number]['cote']
        print(f'Unkown card key_number {key_number}')
        return 0

    def esperance_1_card(self, tier_max=1, card_by_roll=3, nb_roll=0, _esperance_min=0):
        # 1 carte parmi 3+ cartes
        # ok
        bob = self.bob
        nb_card = bob.hand.nb_cards_of_tier_max(tier_max=tier_max)
        dict_value = self.dict_nb_card_cote_of_tier_max(tier_max)

        combin_cumul = 0
        nb_cumul = 0
        nb_card_of_cote_less_than_max = 0
        for cote_max in sorted(dict_value):
            nb_card_of_cote_max = dict_value[cote_max]

            nb_combin = combin(nb_card_of_cote_max, card_by_roll)
            if nb_card_of_cote_less_than_max:
                for nb in range(1, card_by_roll):
                    nb_combin += combin(nb_card_of_cote_max, card_by_roll-nb)*combin(nb_card_of_cote_less_than_max, nb)

            combin_cumul += nb_combin
            nb_cumul += max(cote_max, _esperance_min)*nb_combin

            nb_card_of_cote_less_than_max += nb_card_of_cote_max

        esperance = nb_cumul/combin(nb_card, card_by_roll)

        if nb_roll > 0:
            esperance = self.esperance_1_card(tier_max=tier_max, card_by_roll=card_by_roll, nb_roll=nb_roll-1, _esperance_min=esperance)

        if combin_cumul != combin(nb_card, card_by_roll):
            print('esperance_1_card ERROR combin_cumul')

        return esperance

    def esperance_2_cards_with_free_roll(self, tier_max=1, card_by_roll=3):
        nb_card = self.bob.hand.nb_cards_of_tier_max(tier_max=tier_max)
        dict_value = self.dict_nb_card_cote_of_tier_max(tier_max)
        esp_moy = self.esperance_2_cards(tier_max, card_by_roll) # ~ 2
        esp_max = self.esperance_1_card(tier_max, card_by_roll) # ~ 1.18

        combin_cumul = 0
        nb_cumul = 0
        nb_combin_conservation = 0
        nb_card_of_cote_less_than_min = 0
        dict_sorted = sorted(dict_value)
        for nb, cote_min in enumerate(dict_sorted):
            nb_card_of_cote_min = dict_value[cote_min]
            for cote_max in dict_sorted[nb:]: # cote_max >= cote_min
                nb_card_of_cote_max = dict_value[cote_max]

                if cote_min == cote_max:
                    nb_combin = combin(nb_card_of_cote_max, card_by_roll)
                    if nb_card_of_cote_less_than_min:
                        for nb in range(1, card_by_roll-1):
                            nb_combin += combin(nb_card_of_cote_max, card_by_roll-nb)*combin(nb_card_of_cote_less_than_min, nb)
                else:
                    nb_combin = nb_card_of_cote_max*combin(nb_card_of_cote_min, card_by_roll-1)
                    if nb_card_of_cote_less_than_min:
                        for nb in range(1, card_by_roll-1):
                            nb_combin += nb_card_of_cote_max*combin(nb_card_of_cote_min, card_by_roll-1-nb)*combin(nb_card_of_cote_less_than_min, nb)

                combin_cumul += nb_combin

                if cote_min >= esp_moy/2: # deux cartes > 1
                    nb_combin_conservation += nb_combin
                    nb_cumul += round(cote_min+cote_max, 2)*nb_combin
                elif cote_max < esp_moy - esp_max: # deux cartes < 0.8
                    nb_cumul += esp_moy*nb_combin
                elif cote_max >= esp_moy/2: # cote_max >= 1
                    if cote_min < esp_moy - esp_max:
                        nb_cumul += round(cote_max+esp_max, 2)*nb_combin
                    else:
                        nb_combin_conservation += nb_combin
                        nb_cumul += round(cote_min+cote_max, 2)*nb_combin
                else: # 0.8 < cote_max < 1
                    nb_cumul += round(cote_max+esp_max, 2)*nb_combin

            nb_card_of_cote_less_than_min += nb_card_of_cote_min

        esperance = nb_cumul/combin(nb_card, card_by_roll)
        taux_de_conservation_du_roll = nb_combin_conservation/combin(nb_card, card_by_roll)

        if combin_cumul != combin(nb_card, card_by_roll):
            print('esperance_2_cards ERROR combin_cumul')

        return esperance, taux_de_conservation_du_roll

    def esperance_2_cards(self, tier_max=1, card_by_roll=3, nb_roll=0, _esperance_min=0):
        # 2 cartes parmi 3+ cartes
        # ok
        nb_card = self.bob.hand.nb_cards_of_tier_max(tier_max=tier_max)
        dict_value = self.dict_nb_card_cote_of_tier_max(tier_max)

        combin_cumul = 0
        nb_cumul = 0
        nb_card_of_cote_less_than_min = 0
        dict_sorted = sorted(dict_value)
        for nb, cote_min in enumerate(dict_sorted):
            nb_card_of_cote_min = dict_value[cote_min]
            for cote_max in dict_sorted[nb:]: # cote_max >= cote_min
                nb_card_of_cote_max = dict_value[cote_max]

                if cote_min == cote_max:
                    nb_combin = combin(nb_card_of_cote_max, card_by_roll)
                    if nb_card_of_cote_less_than_min:
                        for nb in range(1, card_by_roll-1):
                            nb_combin += combin(nb_card_of_cote_max, card_by_roll-nb)*combin(nb_card_of_cote_less_than_min, nb)
                else:
                    nb_combin = nb_card_of_cote_max*combin(nb_card_of_cote_min, card_by_roll-1)
                    if nb_card_of_cote_less_than_min:
                        for nb in range(1, card_by_roll-1):
                            nb_combin += nb_card_of_cote_max*combin(nb_card_of_cote_min, card_by_roll-1-nb)*combin(nb_card_of_cote_less_than_min, nb)

                combin_cumul += nb_combin
                nb_cumul += max(_esperance_min, round(cote_min+cote_max, 2))*nb_combin

            nb_card_of_cote_less_than_min += nb_card_of_cote_min

        esperance = nb_cumul/combin(nb_card, card_by_roll)

        if nb_roll > 0:
            esperance = self.esperance_2_cards(tier_max=tier_max, card_by_roll=card_by_roll, nb_roll=nb_roll-1, _esperance_min=esperance)

        if combin_cumul != combin(nb_card, card_by_roll):
            print('esperance_2_cards ERROR combin_cumul')

        return esperance

    def esperance_2_cards_with_cote_min(self, tier_max=1, card_by_roll=3, nb_roll=0, _esperance_min=0, card_cote_min=0):
        # utilisé tour 3 la carte cote_min n'est achetée que si sa côté est > à la carte achetée tour 1
        # 2 cartes parmi 3+ cartes
        # ok
        nb_card = self.bob.hand.nb_cards_of_tier_max(tier_max=tier_max)
        dict_value = self.dict_nb_card_cote_of_tier_max(tier_max)

        combin_cumul = 0
        combin_cumul_under_than_min = 0
        nb_cumul = 0
        nb_card_of_cote_less_than_min = 0
        dict_sorted = sorted(dict_value)
        for nb, cote_min in enumerate(dict_sorted):
            nb_card_of_cote_min = dict_value[cote_min]
            for cote_max in dict_sorted[nb:]: # cote_max >= cote_min
                nb_card_of_cote_max = dict_value[cote_max]

                if cote_min == cote_max:
                    nb_combin = combin(nb_card_of_cote_max, card_by_roll)
                    if nb_card_of_cote_less_than_min:
                        for nb in range(1, card_by_roll-1):
                            nb_combin += combin(nb_card_of_cote_max, card_by_roll-nb)*combin(nb_card_of_cote_less_than_min, nb)
                else:
                    nb_combin = nb_card_of_cote_max*combin(nb_card_of_cote_min, card_by_roll-1)
                    if nb_card_of_cote_less_than_min:
                        for nb in range(1, card_by_roll-1):
                            nb_combin += nb_card_of_cote_max*combin(nb_card_of_cote_min, card_by_roll-1-nb)*combin(nb_card_of_cote_less_than_min, nb)

                combin_cumul += nb_combin
                if cote_min <= card_cote_min:
                    combin_cumul_under_than_min += nb_combin
                nb_cumul += max(_esperance_min, round(max(cote_min, card_cote_min)+cote_max, 2))*nb_combin

            nb_card_of_cote_less_than_min += nb_card_of_cote_min

        esperance = nb_cumul/combin(nb_card, card_by_roll)

        if nb_roll > 0:
            esperance = self.esperance_2_cards_with_cote_min(tier_max=tier_max, card_by_roll=card_by_roll, nb_roll=nb_roll-1, _esperance_min=esperance, card_cote_min=card_cote_min)

        if combin_cumul != combin(nb_card, card_by_roll):
            print('esperance_2_cards_with_cote_min ERROR combin_cumul')

        return esperance, combin_cumul_under_than_min/combin_cumul


    def esperance_2_cards_with_token(self, tier_max=1, card_by_roll=3, token_key_number='100'):
        # 2 cartes parmi 3+ cartes avec un token sur le board
        # vente du token en cas de tirage catastrophe, garde du garde sinon
        # TODO: la meilleure des deux cartes peut potentiellement être achetée avant de roll
        esperance = self.esperance_2_cards(tier_max=tier_max, card_by_roll=card_by_roll)

        bob = self.bob
        nb_card = bob.hand.nb_cards_of_tier_max(tier_max=tier_max)
        dict_value = self.dict_nb_card_cote_of_tier_max(tier_max)
        token_cote = self.card_cote(token_key_number)

        combin_cumul = 0
        nb_cumul = 0
        nb_card_of_cote_less_than_min = 0
        dict_sorted = sorted(dict_value)
        for nb, cote_min in enumerate(dict_sorted):
            nb_card_of_cote_min = dict_value[cote_min]
            for cote_max in dict_sorted[nb:]: # cote_max >= cote_min
                nb_card_of_cote_max = dict_value[cote_max]

                if cote_min == cote_max:
                    nb_combin = combin(nb_card_of_cote_max, card_by_roll)
                    if nb_card_of_cote_less_than_min:
                        for nb in range(1, card_by_roll-1):
                            nb_combin += combin(nb_card_of_cote_max, card_by_roll-nb)*combin(nb_card_of_cote_less_than_min, nb)
                else:
                    nb_combin = nb_card_of_cote_max*combin(nb_card_of_cote_min, card_by_roll-1)
                    if nb_card_of_cote_less_than_min:
                        for nb in range(1, card_by_roll-1):
                            nb_combin += nb_card_of_cote_max*combin(nb_card_of_cote_min, card_by_roll-1-nb)*combin(nb_card_of_cote_less_than_min, nb)

                combin_cumul += nb_combin
                nb_cumul += max(esperance, round(cote_min+cote_max+token_cote, 2))*nb_combin

            nb_card_of_cote_less_than_min += nb_card_of_cote_min

        if combin_cumul != combin(nb_card, card_by_roll):
            print('esperance_2_cards ERROR combin_cumul')

        esperance = nb_cumul/combin(nb_card, card_by_roll)

        return esperance

    def change_dict_nb_card_cote_on(self, add={}):
        for card in add:
            if card in self.key_cote:
                self.key_cote[card] += add[card]

    def change_dict_nb_card_cote_off(self):
        self.init_key_cote()

    def omu_double_roll(self):
        name = 'Omu double roll sans token'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.esperance_1_card(tier_max=1, card_by_roll=3)
        self.board_esp[name][2] = self.board_esp[name][1]
        self.board_esp[name][3] = self.esperance_2_cards(2, 4, nb_roll=2)
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(3, 4, nb_roll=1)

    def omu_level_up_T3(self):
        name = 'Omu levelup Tour3 sans token'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.esperance_1_card(tier_max=1, card_by_roll=3)
        self.board_esp[name][2] = self.board_esp[name][1] + self.esperance_1_card(tier_max=1, card_by_roll=3, nb_roll=1)

        add = {
                '207': 0.2, # rejeton
                '222': 0.2, # ritualiste
                '217': 0.4, # tasse
                '205': 0.2, # goule
        }
        self.change_dict_nb_card_cote_on(add=add)
        self.board_esp[name][3] = self.esperance_1_card(2, 4) + self.board_esp[name][2]
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(3, 4)
        self.change_dict_nb_card_cote_off()

    def omu_T2_T2(self):
        name = 'Omu achat T2 tour 2'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('118')
        card = self.bob.hand.discard('118')
        self.board_esp[name][2] = self.esperance_1_card(2, 4)
        self.bob.hand.append(card)
        self.board_esp[name][3] = self.esperance_1_card(2, 4, nb_roll=1) + self.board_esp[name][2]
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4, nb_roll=1)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(3, 4, nb_roll=1)

    def omu_token(self):
        name = 'Omu mousse du pont'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('117')
        card = self.bob.hand.discard('117')
        self.board_esp[name][2] = self.board_esp[name][1] + self.esperance_1_card(tier_max=1, card_by_roll=3, nb_roll=1)
        if '111' in self.key_cote:
            card2 = self.bob.hand.discard('111')
        elif '101' in self.key_cote:
            card2 = self.bob.hand.discard('101')

        add = { 
                '207': 0.2, # rejeton
                '222': 0.2, # ritualiste
                '217': 0.4, # tasse
                '205': 0.2, # goule
        }
        self.change_dict_nb_card_cote_on(add=add)

        self.board_esp[name][3] = self.esperance_2_cards_with_token(2, 4, '111')
        self.bob.hand.append(card)
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)
        self.bob.hand.append(card2)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(3, 4, nb_roll=1)
        self.change_dict_nb_card_cote_off()

    def anomalie_actualisante(self):
        if not '118' in self.bob.card_can_collect:
            return None

        name = 'Anomalie actualisante'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('118')
        card = self.bob.hand.discard('118')
        self.board_esp[name][2] = self.board_esp[name][1]
        esp_T3, taux_conservation = self.esperance_2_cards_with_free_roll(2, 4)
        self.board_esp[name][3] = esp_T3
        self.bob.hand.append(card)
        espt_T4_moy = self.esperance_2_cards(2, 4)
        self.board_esp[name][4] = self.board_esp[name][3] + taux_conservation*esp_T3 + (1-taux_conservation)*espt_T4_moy
        self.board_esp[name][5] = self.board_esp[name][4] + (1-taux_conservation*taux_conservation)*self.esperance_1_card(2, 4) + \
            taux_conservation*taux_conservation*self.esperance_1_card(3, 4)


    def element_plus(self):
        # impact du roll T2 généré par l'élément plus
        if not '117' in self.bob.card_can_collect:
            return None

        name = 'Elément Plus'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('117')

        card = self.bob.hand.discard('117')
        self.board_esp[name][2] = self.board_esp[name][1]

        add = { '219': 0.5, # élémentaire en fête
                '220': 0.3, # roche en fusion
                '207': 0.2, # rejeton
                '222': 0.2, # ritualiste
                '217': 0.4, # tasse
                '205': 0.2, # goule
                '117': 0.1, # élément Plus
        }
        self.change_dict_nb_card_cote_on(add=add)

        self.board_esp[name][3] = self.esperance_2_cards_with_token(2, 4, '117a')
        self.bob.hand.append(card)
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(2, 4)

        self.change_dict_nb_card_cote_off()

    def acolyte_de_cthun(self):
        if not '116' in self.bob.card_can_collect:
            return None

        name = 'Acolyte de Cthun'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('116')
        card = self.bob.hand.discard('116')
        self.board_esp[name][2] = self.board_esp[name][1]

        add = {
                '205': 0.1, # goule
                '211': 0.25, # gardien des glyphes
                '116': 0.1,
        }
        self.change_dict_nb_card_cote_on(add=add)

        result_T3 = self.esperance_2_cards_with_cote_min(2, 4, card_cote_min=self.card_cote('116'))
        proba_double_roll = result_T3[1]
        self.board_esp[name][3] = result_T3[0]
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)*(1-proba_double_roll) + self.esperance_2_cards(2, 4, nb_roll=2)*proba_double_roll
        self.bob.hand.append(card)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(2, 4)

        self.change_dict_nb_card_cote_off()


    def homoncule(self):
        if not '105' in self.bob.card_can_collect:
            return None

        name = 'Homoncule sans gêne'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('105')
        card = self.bob.hand.discard('105')
        self.board_esp[name][2] = self.board_esp[name][1]

        add = {
                '217': 0.4, # tasse
                '216': 0.75, # surveillant
                '205': 0.2, # goule
                '211': 0.2, # gardien des glyphes
                '105': 0.1,
        }
        self.change_dict_nb_card_cote_on(add=add)

        result_T3 = self.esperance_2_cards_with_cote_min(2, 4, card_cote_min=self.card_cote('105'))
        proba_double_roll = result_T3[1]
        self.board_esp[name][3] = result_T3[0]
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)*(1-proba_double_roll) + self.esperance_2_cards(2, 4, nb_roll=2)*proba_double_roll
        self.bob.hand.append(card)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(2, 4)

        self.change_dict_nb_card_cote_off()


    def tisse_colere(self):
        if not '107' in self.bob.card_can_collect:
            return None

        name = 'Tisse-colère'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('107')
        card = self.bob.hand.discard('107')
        self.board_esp[name][2] = self.board_esp[name][1]

        add = {
                '216': 0.5, # surveillant
                '105': 0.5, # homoncule
                '108': 0.5, # serviteur diabolique
                '210': 0.5, # emprisonneur
                '107': 0.1,
        }
        self.change_dict_nb_card_cote_on(add=add)

        result_T3 = self.esperance_2_cards_with_cote_min(2, 4, card_cote_min=self.card_cote('107'))
        proba_double_roll = result_T3[1]
        self.board_esp[name][3] = result_T3[0]
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)*(1-proba_double_roll) + self.esperance_2_cards(2, 4, nb_roll=2)*proba_double_roll
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(2, 4)
        self.bob.hand.append(card)

        self.change_dict_nb_card_cote_off()

    def chasseur_rochecave(self):
        if not '101' in self.bob.card_can_collect:
            return None

        name = 'Chasseur rochecave'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('101')
        card = self.bob.hand.discard('101')
        self.board_esp[name][2] = self.board_esp[name][1]

        add = {
                '101': 0.3, # chasseur-rochecave
                '208': 0.3, # vieux troubleoeil
                '202': 0.2, # chef de guerre murloc
                '207': 0.2, # rejeton
                '222': 0.2, # ritualiste
                '217': 0.4, # tasse
                '205': 0.2, # goule
        }
        self.change_dict_nb_card_cote_on(add=add)

        result_T3 = self.esperance_2_cards_with_cote_min(2, 4, card_cote_min=self.card_cote('101'))
        proba_double_roll = result_T3[1]
        self.board_esp[name][3] = result_T3[0]
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)*(1-proba_double_roll) + self.esperance_2_cards(2, 4, nb_roll=2)*proba_double_roll
        self.bob.hand.append(card)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(2, 4)

        self.change_dict_nb_card_cote_off()

    def lieutenant_draconide(self):
        if not '111' in self.bob.card_can_collect:
            return None

        name = 'Lieutenant draconide'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('111')
        card = self.bob.hand.discard('111')
        self.board_esp[name][2] = self.board_esp[name][1]

        add = {
                '217': 0.4, # tasse
                '205': 0.2, # goule
                '112': 0.1, # dragonnet rouge
                '211': 0.2, # gardien des glyphes
                '218': 0.2, # trotte-bougie
                '111': 0.1,
        }
        self.change_dict_nb_card_cote_on(add=add)

        result_T3 = self.esperance_2_cards_with_cote_min(2, 4, card_cote_min=self.card_cote('111'))
        proba_double_roll = result_T3[1]
        self.board_esp[name][3] = result_T3[0]
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)*(1-proba_double_roll) + self.esperance_2_cards(2, 4, nb_roll=2)*proba_double_roll
        self.bob.hand.append(card)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(2, 4)

        self.change_dict_nb_card_cote_off()

    def chasse_marée(self):
        # impact du roll T2 généré par le chasse-marée
        if not '100' in self.bob.card_can_collect:
            return None

        name = 'Chasse marée'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('100')
        card = self.bob.hand.discard('100')
        self.board_esp[name][2] = self.board_esp[name][1]

        add = {
                '101': 0.2, # chasseur-rochecave
                '208': 0.3, # vieux troubleoeil
                '202': 0.2, # chef de guerre murloc
                '207': 0.2, # rejeton
                '222': 0.2, # ritualiste
                '217': 0.4, # tasse
                '205': -0.2, # goule
                '100': 0.1,
        }
        self.change_dict_nb_card_cote_on(add=add)

        self.board_esp[name][3] = self.esperance_2_cards_with_token(2, 4, '100a')
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(2, 4)
        self.bob.hand.append(card)

        self.change_dict_nb_card_cote_off()


    def micro_machine(self):
        # impact du roll T2 généré par le chasse-marée
        if not '110' in self.bob.card_can_collect:
            return None

        name = 'Micro-machine'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('110')
        card = self.bob.hand.discard('110')
        self.board_esp[name][2] = self.board_esp[name][1]+0.2

        add = {
                '217': 0.1, # tasse
                '110': 0.1,
        }
        self.change_dict_nb_card_cote_on(add=add)

        result_T3 = self.esperance_2_cards_with_cote_min(2, 4, card_cote_min=0.8)
        proba_double_roll = result_T3[1]
        self.board_esp[name][3] = result_T3[0]
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)*(1-proba_double_roll) + self.esperance_2_cards(2, 4, nb_roll=2)*proba_double_roll
        self.bob.hand.append(card)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(2, 4)

        self.change_dict_nb_card_cote_off()

    def mande_flots(self):
        if not '102' in self.bob.card_can_collect:
            return None

        name = 'Mande-flots murloc'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('102')
        card = self.bob.hand.discard('102')
        self.board_esp[name][2] = self.board_esp[name][1]

        add = {
                '101': 0.3, # chasseur-rochecave
                '208': 0.5, # vieux troubleoeil
                '202': 0.4, # chef de guerre murloc
                '217': 0.2, # tasse
                '205': 0.1, # goule
                '100': 0.5, # chasse-marée
                '102': 0.2,
        }
        self.change_dict_nb_card_cote_on(add=add)

        result_T3 = self.esperance_2_cards_with_cote_min(2, 4, card_cote_min=self.card_cote('102'))
        proba_double_roll = result_T3[1]
        self.board_esp[name][3] = result_T3[0]
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)*(1-proba_double_roll) + self.esperance_2_cards(2, 4, nb_roll=2)*proba_double_roll
        self.bob.hand.append(card)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(2, 4)

        self.change_dict_nb_card_cote_off()


    def chat_de_gouttière(self):
        # impact du roll T2 généré par le chat de gouttière
        if not '103' in self.bob.card_can_collect:
            return None

        name = 'Chat de gouttière'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('103')
        card = self.bob.hand.discard('103')
        self.board_esp[name][2] = self.board_esp[name][1]

        add = {
                '104': 0.2, # hyène
                '207': 0.1, # rejeton
                '222': 0.2, # ritualiste
                '217': 0.3, # tasse
                '205': -0.1, # goule
                '103': 0.1,
        }
        self.change_dict_nb_card_cote_on(add=add)

        self.board_esp[name][3] = self.esperance_2_cards_with_token(2, 4, '103a')
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(3, 4) - self.card_cote('103a')
        self.bob.hand.append(card)

        self.change_dict_nb_card_cote_off()

    def mousse_du_pont(self):
        if not '114' in self.bob.card_can_collect:
            return None

        add = {
                '217': 0.2, # tasse
                '205': 0.2, # goule
                '201': 0.2, # capitaine des mers du sud
                '114': 0.1,
        }
        self.change_dict_nb_card_cote_on(add=add)

        name = 'Mousse du pont'
        self.board_esp[name] = {}
        self.board_esp[name][1] = self.card_cote('114')
        card = self.bob.hand.discard('114')
        self.board_esp[name][2] = self.board_esp[name][1]
        self.board_esp[name][3] = self.esperance_2_cards(2, 4, nb_roll=1)
        self.bob.hand.append(card)
        self.board_esp[name][4] = self.board_esp[name][3] + self.esperance_2_cards(2, 4)
        self.board_esp[name][5] = self.board_esp[name][4] + self.esperance_1_card(2, 4)

        self.change_dict_nb_card_cote_off()

    def bot_reference(self):
        self.board_esp['ref'] = {}
        self.board_esp['ref'][1] = self.esperance_1_card(tier_max=1, card_by_roll=3)
        self.board_esp['ref'][2] = self.board_esp['ref'][1]
        self.board_esp['ref'][3] = self.esperance_2_cards(tier_max=2, card_by_roll=4)
        self.board_esp['ref'][4] = self.board_esp['ref'][3] + self.esperance_2_cards(tier_max=2, card_by_roll=4)
        self.board_esp['ref'][5] = self.board_esp['ref'][4] + self.esperance_1_card(2, 4)

if __name__ == "__main__":
    cl = Stats()
    cl.bot_reference()

    cl.mousse_du_pont()
    cl.element_plus()
    cl.chasse_marée()
    cl.tisse_colere()
    cl.lieutenant_draconide()
    cl.chasseur_rochecave()
    cl.homoncule()
    cl.mande_flots()
    cl.micro_machine()
    cl.acolyte_de_cthun()
    cl.anomalie_actualisante()
    cl.chat_de_gouttière()

    cl.omu_double_roll()
    cl.omu_level_up_T3()
    cl.omu_token()
    cl.omu_T2_T2()

    for name, info in cl.board_esp.items():
        print(name, ':', info)

