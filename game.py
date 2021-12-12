#!/usr/bin/env python

from base.db_card import CardDB
from base.utils import Card_list
from base.enums import Race, Type, NB_PRESENT_TYPE, VERSION, CardName
import random
import base.player
from base.entity import Entity, Card
from base.hand import Bob_hand
from base.stats import *
import base.entity
from collections import deque
from base.combat import Combat
from typing import Any
from base.sequence import Sequence


class Game(Entity):
    default_attr = {
        "type": Type("GAME"),
        "is_arene": False,
        'no_bob': False,
        'version': VERSION,
        'current_sequence': '',
        'is_bot': True,
        'is_test': False,
    }

    def __init__(self, *args, types_ban=None, **kwargs):
        for kv in {**self.default_attr, **kwargs}.items():
            setattr(self, *kv)

        self.reinit()
        if types_ban is None:
            self.types_ban = self.determine_ban_type()
        else:
            self.types_ban = types_ban

        self.cards = CardDB(self.types_ban)
        self.craftable_heroes = self.cards.objects.filter(battlegroundsHero=True)
        self.minion_can_collect = self.cards.objects.exclude(techLevel=None)

        self.hand = Bob_hand()
        self.hand.owner = self

        for minion in self.minion_can_collect:
            for _ in range(minion.nb_copy):
                self.hand.create_card_in(minion)
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

    @property
    def all_cards(self) -> Meta_card_data:
        return self.cards

    @property
    def deck(self):
        return self.hand

    #def party_begin(self, *players, hero_p1=0, hero_p2=0) -> None:
    def party_begin(self, player_name_player_hero: dict) -> None:
        # TODO: Players are assigned opponents for the first round when the game begins before the heroes are chosen.
        # TODO: Players will not face the same player, or Kel'Thuzad, more than once in every 3 combat rounds (unless there are 2 players remaining).
        if not player_name_player_hero:
            return

        nb_hero_choice = 4

        self.all_in_bob()
        self.reinit()

        random_craftable_heroes = list(self.craftable_heroes)
        random.shuffle(random_craftable_heroes)

        for nb, (player_name, player_hero) in enumerate(player_name_player_hero.items()):
            bob = base.player.Bob(
                    minion_can_collect=self.minion_can_collect)

            if player_hero:
                hero_chosen = self.all_cards[player_hero]
            elif self.is_arene:
                hero_chosen = self.all_cards[CardName.DEFAULT_HERO]
            else:
                hero_chosen = self.choose_champion(
                    random_craftable_heroes[nb*nb_hero_choice:(nb+1)*nb_hero_choice],
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

    def determine_ban_type(self) -> list:
        if not self.is_test and not self.is_arene:
            lst = Race.battleground_race_name()
            random.shuffle(lst)
            return lst[NB_PRESENT_TYPE:]
        return []

    def remove(self, entity: Entity) -> None:
        pass

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


if __name__ == "__main__":
    g = Card(CardName.DEFAULT_GAME, types_ban=[], is_test=True)
    g.party_begin({'p1_name': 63601, 'p2_name': 0})
    p1, p2 = g.players

    print(Race('PIRATE'))
    print(Race('PIRATE') == 'PIRATE')
    print(Race('ALL') == 'PIRATE')
    print(Race('ALL').PIRATE)

    a = Card_list()
    a.append(p1.create_card(61444))
    print(a.one_minion_by_race())
    print(a.filter(race='PIRATE'))
    print(a.filter(race='ALL'))

    """
    from base.arene import arene
    arene(method='base_T1_to_T3_extended', types_ban=[], retro=6,
        p1=CardName.DEFAULT_HERO,
        p2=CardName.DEFAULT_HERO)
    """

    """
    p1 = g.players[0]
    old_hand_len = g.hand.size
    with Sequence('TURN', g):
        p1.draw(65658) # Acolyte de C'thun
        assert p1.hand.size == 1
        assert g.hand.size == old_hand_len - len(g.players)*3 - 3



    with Sequence('TURN', g):
        cha = p1.draw(41245) # Chasseur rochecave
        cha.play()
        yo = p1.draw(61060) # Yo-oh ogre
        yo.play()
        mou = p2.draw(61055) # Mousse du pont
        mou.play()
        mou = p2.draw(61055) # Mousse du pont
        mou.play()
        ele = p2.draw(64038) # ElémenPlus
        ele.play()

    with Sequence('FIGHT', g) as seq:
        print(yo.health)
        print(cha.health)
        print(p1.field.combat.damage)
    """
