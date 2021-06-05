from bob import Bob
from constants import Type, General, Event, LEVEL_MAX, TYPE_NAME, CARD_NB_COPY, NB_PRESENT_TYPE
import random
import player
from entity import CARD_DB
from typing import Dict

class Game:
    def __init__(self, type_ban=None):
        self._nb_turn = 0
        self.players = []
        self.arene = False
        self.trigger_stack = []
        self.entities = []

        if type_ban is None:
            self.type_present = self.determine_present_type()
        else:
            self.type_present = Type.ALL - type_ban

        self.craftable_card = {key: value
            for key, value in CARD_DB.items()
                if not value.get('ban') and \
                    value['synergy'] & self.type_present}

        self.craftable_hero = {key: value
            for key, value in self.craftable_card.items()
                if value['general'] == General.HERO}

        bob_card_dict = {key: value
            for key, value in self.craftable_card.items()
                if not value.get('cant_collect') and \
                    value['general'] == General.MINION}

        self.bob = Bob(bob_card_dict, type_present=self.type_present)
        self.bob.owner = self

        #self.nb_card_by_syn = { nb: [0]*(LEVEL_MAX+1)
        #    for nb in TYPE_NAME }
        #self.nb_card_by_syn[card_synergy][card_level] += CARD_NB_COPY[card_level]
        #self.print_bdd_card()

    @property
    def nb_turn(self):
        return self._nb_turn

    @nb_turn.setter
    def nb_turn(self, value):
        self._nb_turn = value
        self.active_event(Event.BEGIN_TURN)

    def active_event(self, event):
        for entity in self.entities:
            entity.active_event(event)

    def add_players(self, *players):
        heroes_can_collect = self.heroes_can_collect() # va être utile pour Sire Finley

        shuffle_list_name = list(heroes_can_collect)
        random.shuffle(shuffle_list_name)
        for nb, player_name in enumerate(players):
            print(f'Choix du héros pour {player_name} :')
            # de base, 4 héros sont disponibles lors de la sélection
            hero_chosen = self.choice_sample_hero(shuffle_list_name[nb*4:nb*4+4])
            if hero_chosen:
                plyr = player.Player('', player_name, heroes_can_collect[hero_chosen])
                self.players.append(plyr)
                plyr.owner = self

        self.bob.create_boards(*self.players)

    def choice_sample_hero(self, choice_list):
        """
            player chooses one card omong ``choice_list`` iterable
            *return: chosen card
            *rtype: iterable content
        """
        for nb, minion in enumerate(choice_list):
            print(f'{nb}- {minion}')
        while True:
            try:
                return choice_list[int(input())]
            except IndexError:
                print('Valeur incorrecte.')
            except ValueError:
                print('Saississez une valeur.')

    def determine_present_type(self) -> int:
        lst = Type.battleground_type()[:]
        random.shuffle(lst)

        return sum(lst[:NB_PRESENT_TYPE])

    def heroes_can_collect(self) -> Dict[str, str]:
        return {hero_info['name']: hero_id
            for hero_id, hero_info in self.craftable_hero.items()}

if __name__ == "__main__":
    g = Game()
    g.add_players('rivvers', 'notoum')
    print(g.players[0].hero.health)
    print(g.entities)










    """
    def print_bdd_card(self):
        len_max = 0
        for synergy_name in TYPE_NAME.values():
            len_max = max(len_max, len(synergy_name))
        separator = ' :'

        with open('bdd_card', 'w', encoding='utf-8') as file:
            title = 'Présence des différentes synergies :\n'
            line_1 = ' '*(len_max+len(separator))
            for i in range(1, LEVEL_MAX+1):
                line_1 += f'T{i}'.center(4)
            line_1 += 'Total\n'

            file.write(title)
            file.write(line_1)

            line_x = ''
            check_all_cards = self.nb_card_by_syn
            for key, value in check_all_cards.items():
                line_x += TYPE_NAME[key].ljust(len_max) + separator

                value = value[1:] # exclusion des cartes de niveau 0
                line_x += ''.join(map(lambda x: str(x).rjust(4), value))
                line_x += str(sum(value)).rjust(5) + '\n'
            file.write(line_x)

            last_line = 'Total'.ljust(len_max) + separator
            som = 0
            for i in range(1, LEVEL_MAX+1):
                total = 0
                for j in check_all_cards.values():
                    total += j[i]
                last_line += str(total).rjust(4)
                som += total
            last_line += str(som).rjust(5)
            file.write(last_line)        
    """