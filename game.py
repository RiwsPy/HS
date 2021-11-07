from db_card import CARD_DB
from utils import Card_list, db_arene
from enums import Race, Type, NB_PRESENT_TYPE, VERSION, CardName, ADAPT_ENCHANTMENT
import random
import player
from entity import Entity, Card
from hand import Bob_hand
from itertools import chain
from stats import *
import entity
from collections import deque
from combat import Combat
import db_card


class Game(Entity):
    default_attr = {
        "test": False,
        "is_arene": False,
        'no_bob': False,
        'version': VERSION,
        'current_sequence': '',
        'is_bot': True,
    }

    def __init__(self, *args, **attr):
        super().__init__(CardName.DEFAULT_GAME, **attr)

        self.reinit()

        type_ban = attr.get('type_ban', self.determine_present_type())
        self.type_present = Race('ALL').hex - type_ban

        all_cards = entity.card_db().filter(ban=None)
        if self.type_present != 0:
            self.craftable_card = all_cards.\
                filter_hex(synergy=self.type_present)
        else: # tous types ban
            self.craftable_card = all_cards.filter(synergy='ALL')

        self.craftable_hero = self.craftable_card.\
            filter(type=Type.HERO) #.exclude(dbfId=CardName.BOB) # test avec BOB ban

        self.minion_can_collect = self.craftable_card.\
            filter(type=Type.MINION, cant_collect=None)

        self.hand = Bob_hand()
        self.hand.owner = self

        for dbfId in self.minion_can_collect:
            for _ in range(dbfId.nb_copy):
                self.hand.create_card_in(int(dbfId))
            """
            *chain(*
            ([int(dbfId)]*dbfId.nb_copy
                for dbfId in self.minion_can_collect)))
            """

    def reinit(self):
        self.entities = Card_list()
        self._turn = 0
        self.action_stack = deque()
        self.players = Card_list()
        self.fields = Card_list()

    def party_begin(self, *players, hero_p1='', hero_p2='') -> None:
        #TODO: Players are assigned opponents for the first round when the game begins before the heroes are chosen.
        #TODO: Players will not face the same player, or Kel'Thuzad, more than once in every 3 combat rounds (unless there are 2 players remaining).
        if not players:
            return None

        self.all_in_bob()
        self.reinit()

        random.shuffle(self.craftable_hero)

        for nb, player_name in enumerate(players):
            bob = player.Bob(
                    minion_can_collect=self.minion_can_collect, 
                    type_present=self.type_present)

            # de base, 4 héros sont disponibles lors de la sélection
            if self.is_arene:
                if nb == 0 and hero_p1:
                    hero_chosen = CARD_DB[hero_p1]
                elif nb == 1 and hero_p2:
                    hero_chosen = CARD_DB[hero_p2]
                else:
                    hero_chosen = CARD_DB[CardName.DEFAULT_HERO]
            elif nb == 0 and hero_p1:
                hero_chosen = CARD_DB[hero_p1]
            else:
                hero_chosen = self.choose_one_of_them(self.craftable_hero[nb*4:nb*4+4],
                    pr=f'Choix du héros pour {player_name} :')

            plyr = Card(
                CardName.DEFAULT_PLAYER,
                pseudo=player_name,
                champion=hero_chosen,
                bob=bob,
                is_bot=True)
            self.players.append(plyr)

            new_field = Card(CardName.DEFAULT_FIELD, p1=plyr, p2=plyr.bob)
            self.append(new_field)

    def determine_present_type(self) -> int:
        lst = Race.battleground_race()
        random.shuffle(lst)

        return sum(lst[:NB_PRESENT_TYPE])

    def turn_start(self, sequence):
        self._turn += 1
        self.entities = Card_list()
        for player in self.players:
            self.append(Card(CardName.DEFAULT_FIELD, p1=player, p2=player.bob))

        self.temp_counter = 0
        for entity in self:
            entity.temp_counter = 0

    def turn_end(self, sequence):
        self.entities = Card_list()
        players = self.players
        for p1, p2 in zip(players[::2], players[1::2]):
            self.append(Card(CardName.DEFAULT_FIELD, p1=p1, p2=p2))

    def fight_start(self, sequence):
        for field in self.entities:
            field.combat = Combat(self, field.p1.board, field.p2.board)

    def fight(self, sequence):
        for field in self.entities:
            field.combat.fight_initialisation()

    def arene_on_creation(self):
        minion_rating = db_arene(
            version=self.version,
            type_ban=Race('ALL').hex - self.type_present)
        for card in self.minion_can_collect:
            try:
                card.all_rating = minion_rating[card]['rating']
            except KeyError:
                card.all_rating = {}


if __name__ == "__main__":
    g = Card(CardName.DEFAULT_GAME)
    g.party_begin('rivvers', 'notoum', hero_p1=58021)
    p1, p2 = g.players


