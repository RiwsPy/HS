import random
from .enums import BOARD_SIZE
from .utils import *
from .action import *
from typing import Tuple
from .board import Board
from .entity import Minion

class Combat:
    def __init__(self, field, board_p1: Board, board_p2: Board) -> None:
        self.loser = None
        self.winner = None
        self.damage = 0
        self.owner = field

        self.entities = (board_p1, board_p2)
        board_p1.owner.combat = self
        board_p2.owner.combat = self
        board_p1.owner.fights.append(self)
        board_p2.owner.fights.append(self)

    def fight_initialisation(self) -> None:
        # TODO: sauvegarde des résultats de tous les combats
        """
            Start the fight and save result
        """
        self.winner, self.loser = self.begin_fight()
        self.damage = self.end_fight_damage()

    def fight_is_over(self) -> bool:
        """
            return True if one board is empty or minions cant attack (> tie)
            return False otherwise
        """
        for board in self.entities:
            if board.size == 0:
                return True

        for board in self.entities:
            for minion in board.cards:
                if minion.can_attack:
                    return False

        return True

    def begin_fight(self) -> Tuple[Board, Board] or Tuple[None, None]:
        for board in self.entities:
            board.attack_case = 0 # servant in this case attack first

        self.attacker = self.who_attacks_first(*self.entities)

        while not self.fight_is_over():
            self.next_round()
            damage_resolve(self, *self.owner.cards)

            self.owner.active_action()
            self.attacker = self.attacker.opponent

        return self.who_is_the_winner()

    def who_is_the_winner(self) -> Tuple[Board, Board] or Tuple[None, None]:
        p1, p2 = self.entities
        if p1.size > 0:
            if p2.size > 0:
                return None, None
            return self.entities
        elif p2.size <= 0:
            return None, None
        return p2, p1

    def end_fight_damage(self) -> int:
        """
            Returns the amount of damage to the player 
        """
        if self.winner is None:
            return 0

        return self.winner.cumulative_level + self.winner.level

    def next_round(self) -> None:
        # search first attacker
        for i in range(BOARD_SIZE):
            attacker_minion_position = (self.attacker.attack_case + i) % BOARD_SIZE
            minion = self.attacker.cards[attacker_minion_position]
            if minion and minion.can_attack:
                self.minion_attack(minion)
                break

    def minion_attack(self, attacker_minion: Minion) -> None:
        for _ in range(attacker_minion.how_many_time_can_I_attack()):
            attacker_minion.combat()

        if attacker_minion.is_alive:
            self.attacker.attack_case += 1
            if self.attacker.size > 0:
                self.attacker.attack_case %= self.attacker.size

    def who_attacks_first(self, board_p1: Board, board_p2: Board, *args) -> Board:
        """
            Returns the first board to attack
        """
        if board_p1.size > board_p2.size or \
                random.randint(0, 1) and board_p2.size == board_p1.size:
            return board_p1
        return board_p2
