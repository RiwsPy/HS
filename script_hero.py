import player
import arene
from operator import itemgetter

def Default_script(self, recursive=True): # self = player ?,next_opponent dans un attribut ?
    if self.nb_turn == 1 and self.gold >= self.minion_cost:
        if recursive:
            pass
            #lst = self.best_card_T1(self.next_opponent)
            #self.buy_card()
    if self.nb_turn >= 2 and self.gold >= self.level_up_cost and self.level == 1:
        self.level_up()
    elif self.gold >= self.level_up_cost + 3:
        self.level_up()

def No_level_up(self, recursive=True):
    if self.gold//self.minion_cost <= (self.gold-self.power.next_roll_cost)//self.minion_cost:
        # et carte pas intéressante
        pass
        # roll
    elif self.gold >= self.minion_cost:
        pass
        # achat meilleure carte

def Millhouse(self, recursive=True):
    if self.nb_turn == 1:
        pass

def Nozdormu(self, recursive=True):
    if self.nb_turn == 1 and self.gold >= self.minion_cost:
        if recursive:
            # les personnages sont modifiés, bob également
            cote, esperance = self.best_card_T1(*self.bob.boards.keys())
            for _ in range(self.nb_free_roll+1):
                note = 0
                best_note = -1000
                best_minion = None
                for minion in self.board.opponent:
                    if cote[minion.key_number] > best_note:
                        best_note = cote[minion.key_number]
                        best_minion = minion
                    note += cote[minion.key_number]

                note /= len(self.board.opponent)
                print(f'espérance : {esperance}, espérance obtenue {note}')
                print(f'meilleur minion {best_minion}, note : {best_note}')
                if self.nb_free_roll > 0:
                    if best_note <= esperance:
                        print('roll conseillé')
                        self.roll()
                    else:
                        print('achat conseillé')
                        break
                else:
                    print('aucun roll disponible : achat conseillé')
                    break

def Millificent(self, recursive=True):
    if self.nb_turn == 1 and self.gold >= self.minion_cost:
        result = arene.arene(self.bob, self, self.next_opponent, TIER_MAX=self.level, pr=False, nb_turn=2)

        # TODO il nous faut appliquer la méthode de l'opposant
        new_format = [[key_number, info['name'], (info['pv_loss']*7-info['pv_inflict'])/(info['nb_win']+info['nb_loss']+info['nb_draw'])]
            for key_number, info in result[self.next_opponent.pseudo].items()]
        sorted_result = sorted(new_format, key=itemgetter(2))
        print('j2 contre j1')
        best_minion = [info[0]
            for info in sorted_result]
        best_minion_proba = self.pick_best_card(best_minion)
        proba_dict = {}
        result_j2 = {key_number: proba
            for key_number, proba in zip(best_minion, best_minion_proba)}
        proba_dict[self.next_opponent.pseudo] = result_j2

        print(sorted_result)

        new_format = [[key_number, info['name'], (info['pv_loss']*7-info['pv_inflict'])/(info['nb_win']+info['nb_loss']+info['nb_draw'])]
            for key_number, info in result[self.pseudo].items()]
        sorted_result = sorted(new_format, key=itemgetter(2))
        print('j1 contre j2')
        print(sorted_result)
        print(result[self.pseudo])

        """
        result = arene.arene(self.bob, self, self.next_opponent, TIER_MAX=self.level, pr=False, nb_turn=2, proba_dict=proba_dict)

        new_format = [[key_number, info['name'], (info['pv_loss']*7-info['pv_inflict'])/info['nb_match']]
            for key_number, info in result[self.pseudo].items()]
        sorted_result = sorted(new_format, key=itemgetter(2))
        print('j1 contre j2, V2')
        print(sorted_result)
        """

def AFK(self, recursive=True):
    if self.gold >= self.minion_cost:
        pass

