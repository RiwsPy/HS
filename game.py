#!/usr/bin/env python

from base.db_card import CARD_DB
from base.utils import Card_list, db_arene
from base.enums import Race, Type, NB_PRESENT_TYPE, VERSION, CardName
import random
import base.player
from base.entity import Entity, Card, card_db
from base.hand import Bob_hand
from base.stats import *
import base.entity
from collections import deque
from base.combat import Combat
from typing import Any
from base.sequence import Sequence


class Game(Entity):
    default_attr = {
        "test": False,
        "is_arene": False,
        'no_bob': False,
        'version': VERSION,
        'current_sequence': '',
        'is_bot': True,
        'is_test': False,
    }

    def __init__(self, *args, **attr):
        super().__init__(CardName.DEFAULT_GAME, **attr)

        self.reinit()

        self.type_ban = attr.get('type_ban', self.determine_present_type())

        all_cards = card_db()
        self.craftable_cards = all_cards
        #self.craftable_cards = all_cards.exclude_hex(synergy=self.type_ban)
        self.craftable_heroes = CARD_DB.filter(battlegroundsHero=True)
        #self.craftable_heroes = self.craftable_cards.filter(battlegroundsHero=True)
        self.minion_can_collect = self.craftable_cards.exclude(techLevel=None)

        self.hand = Bob_hand()
        self.hand.owner = self

        for minion in self.minion_can_collect:
            for _ in range(minion.nb_copy):
                #self.hand.create_card_in(int(dbfId))
                self.hand.create_card_in(minion.dbfId)
            """
            *chain(*
            ([int(dbfId)]*dbfId.nb_copy
                for dbfId in self.minion_can_collect)))
            """

    def reinit(self):
        self.fights = defaultdict(list)
        self.entities = Card_list()
        self._turn = 0
        self.action_stack = deque()
        self.players = Card_list()
        self.fields = Card_list()

    def party_begin(self, *players, hero_p1=0, hero_p2=0) -> None:
        #TODO: Players are assigned opponents for the first round when the game begins before the heroes are chosen.
        #TODO: Players will not face the same player, or Kel'Thuzad, more than once in every 3 combat rounds (unless there are 2 players remaining).
        if not players:
            return None

        self.all_in_bob()
        self.reinit()

        random_craftable_heroes = list(self.craftable_heroes)
        random.shuffle(random_craftable_heroes)

        for nb, player_name in enumerate(players):
            bob = base.player.Bob(
                    minion_can_collect=self.minion_can_collect)
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
                hero_chosen = self.choose_champion(random_craftable_heroes[nb*4:nb*4+4],
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

    def choose_champion(self, choice_list: Card_list, pr: str = '') -> Any:
        """
            player chooses one card among ``choice_list`` list
            *return: chosen card id or None
            *rtype: list content
        """
        if self.is_arene or self.is_test:
            return random.choice(choice_list)

        if pr:
            print(pr)
        for nb, entity in enumerate(choice_list):
            print(f'{nb}- {entity}')
        while True:
            try:
                return choice_list[int(input())]
            except IndexError:
                print('Valeur incorrecte.')
            except ValueError:
                print('Saississez une valeur.')

    def fight_start(self, sequence):
        self.entities = Card_list()
        for p1, p2 in zip(self.players[::2], self.players[1::2]):
            field = Card(CardName.DEFAULT_FIELD, p1=p1, p2=p2)
            self.append(field)
            field.combat = Combat(field, p1.board, p2.board)
            self.fights[self._turn].append(field)

    def fight(self, sequence):
        for field in self.entities:
            field.combat.fight_initialisation()

    def arene_on_creation(self):
        minion_rating = db_arene(
            version=self.version,
            type_ban=self.type_ban)
        for card in self.minion_can_collect:
            try:
                card.all_rating = minion_rating[card]['rating']
            except KeyError:
                card.all_rating = {}


if __name__ == "__main__":
    g = Card(CardName.DEFAULT_GAME, is_test=True)
    g.party_begin('p1_name', 'p2_name', hero_p1=63601)
    p1, p2 = g.players

    with Sequence('TURN', g):
        cha = p1.hand.create_card_in(41245) # Chasseur rochecave
        cha.play()
        yo = p1.hand.create_card_in(61060) # Yo-oh ogre
        yo.play()
        mou = p2.hand.create_card_in(61055) # Mousse du pont
        mou.play()
        mou = p2.hand.create_card_in(61055) # Mousse du pont
        mou.play()
        ele = p2.hand.create_card_in(64038) # ElémenPlus
        ele.play()

    with Sequence('FIGHT', g) as seq:
        print(yo.health)
        print(cha.health)
        print(p1.field.combat.damage)
