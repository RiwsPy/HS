from db_card import CARD_DB
from utils import Card_list
from constants import Type, General, Event, NB_PRESENT_TYPE, VERSION
import random
import player
from entity import Entity
from hand import Bob_hand
from itertools import chain
import combat
from stats import *
import entity
import json

class Game(Entity):
    default_attr = {
        "event": Event.ALL,
        "test": False,
        "is_arene": False,
        'no_bob': False,
        'version': VERSION,
        'is_bot': True,
    }
    def __init__(self, type_ban=None, **attr):
        super().__init__("GAME", **attr)

        self.reinit()

        if type_ban is None:
            self.type_present = self.determine_present_type()
        else:
            self.type_present = Type.ALL - type_ban

        all_cards = entity.card_db()
        self.craftable_card = all_cards.\
            filter_hex(synergy=self.type_present).\
            filter(ban=None)

        self.craftable_hero = self.craftable_card.\
            filter(general=General.HERO)

        self.card_can_collect = self.craftable_card.\
            filter(general=General.MINION).\
            filter(cant_collect=None)
        
        self.hand = Bob_hand()
        self.hand.owner = self

        self.hand.create_card_in(*chain(*
            ([str(dbfId)]*dbfId.nb_copy
                for dbfId in self.card_can_collect)))

        #self.nb_card_by_syn = { nb: [0]*(LEVEL_MAX+1)
        #    for nb in TYPE_NAME }
        #self.nb_card_by_syn[card_synergy][card_level] += CARD_NB_COPY[card_level]
        #self.print_bdd_card()
        if self.is_arene:
            with open('db_arene.json', 'r') as file:
                dic = json.load(file)
            self.db_arene = dic
            """
            try:
                data_stat = dic[self.version][str(Type.ALL - self.type_present)]
            except KeyError:
                return None
            search = {'p1': 'Héros tout nul', 'p2': 'Héros tout nul', 'com': 'Sortie_tour2_retro_2'}
            data = None
            for info in data_stat.values():
                if info['data'] == search:
                    data = info['rating']
                    esp = info['espérance']
                    break
            if data:
                for card_id, rating in data.items():
                    card_data = self.card_db[card_id]
                    card_data.rating = rating
                    card_data.esp = esp
        """


    def reinit(self):
        self.entities = Card_list()
        self._nb_turn = 0
        #self.graveyard = Graveyard(self)
        self.trigger_stack = []
        self.action_stack = []
        self.fights = []

    @property
    def nb_turn(self):
        return self._nb_turn

    @nb_turn.setter
    def nb_turn(self, value):
        if value != self._nb_turn:
            self._nb_turn = value
        self.active_global_event(Event.BEGIN_TURN, *self.entities)

    def go_turn(self):
        self.begin_turn()
        self.end_turn()
        self.begin_fight()
        self.end_fight()

    def begin_turn(self):
        self.nb_turn += 1

    @property
    def players(self):
        return self.entities.filter(general=General.HERO)

    def end_turn(self):
        self.active_global_event(Event.END_TURN, *self.entities)
        self.fights = []
        players = self.players
        for nb, player in enumerate(players[::2]):
            self.fights.append(combat.Combat(self, player.board, players[nb*2+1].board))

    def begin_fight(self):
        if self.fights:
            for fight in self.fights:
                fight.fight_initialisation()
        else:
            print(f"game don't have fights attribute : see end_turn ?")

    def end_fight(self):
        self.active_global_event(Event.END_FIGHT, *self.entities)

    def party_begin(self, *players, hero_p1='', hero_p2='') -> None:
        if not players:
            return None

        self.all_in_bob()
        self.reinit()

        random.shuffle(self.craftable_hero)

        for nb, player_name in enumerate(players):
            bob = player.Bob(
                    card_can_collect=self.card_can_collect, 
                    type_present=self.type_present)
            self.append(bob)
            if self.no_bob:
                bob.remove_attr(event=Event.BEGIN_TURN)

            # de base, 4 héros sont disponibles lors de la sélection
            if self.is_arene:
                if nb == 0 and hero_p1:
                    hero_chosen = CARD_DB[hero_p1]
                elif nb == 1 and hero_p2:
                    hero_chosen = CARD_DB[hero_p2]
                else:
                    hero_chosen = CARD_DB['aaa']
            else:
                hero_chosen = self.choose_one_of_them(self.craftable_hero[nb*4:nb*4+4],
                    pr=f'Choix du héros pour {player_name} :')
            plyr = player.Player(player_name, hero_chosen, bob=bob)
            bob.board.opponent = plyr.board
            self.append(plyr)

    def determine_present_type(self) -> int:
        lst = Type.battleground_type()[:]
        random.shuffle(lst)

        return sum(lst[:NB_PRESENT_TYPE])



if __name__ == "__main__":
    g = Game()
    g.party_begin('rivvers', 'notoum')
    g.nb_turn += 1
    p1 = g.players[0]
    p2 = g.players[1]
    """
        # hyène, roche en fusion, rejeton, défense robuste, chef du gang, 
    p1.board.create_card_in('104')
    p1.board.create_card_in('220')
    p1.board.create_card_in('207')
    p1.board.create_card_in('225')
    p1.board.create_card_in('2288')
    print(p1.board.cards)
    p1.board.auto_placement_card()
    print(p1.board.cards)
    """

    """
    p1.board.create_card_in("116")
    p2.board.create_card_in("205")
    g.end_turn(p1, p2)
    g.begin_fight(p1)
    print(p1.board.cards)
    """


    """
    crd = plyr_1.hand.create_card_in('120')
    crd.play()
    crd = plyr_2.hand.create_card_in('112')
    crd.play()
    winner, damage = plyr_1.fight.fight_initialisation()
    print(winner, damage)
    """







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