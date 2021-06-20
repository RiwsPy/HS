import random
from constants import BATTLE_SIZE, Event, State, General
from utils import *
from action import *
from typing import Tuple

class Combat:
    def __init__(self, game, board_j1, board_j2):
        self.game = game

        self.combattants = (board_j1, board_j2)
        self.combattants_player = (board_j1.owner, board_j2.owner)
        board_j1.opponent = board_j2
        board_j2.opponent = board_j1
        board_j1.owner.fight = self
        board_j2.owner.fight = self

    def fight_initialisation(self) -> Tuple[object, int]:
        """
            *return: winner id and total damage to loser
            *rtype: tuple
        """
        winner, loser = self.begin_fight()

        for board in self.combattants:
            board.owner.win_last_match = False
            board.owner.fight = None

        damage = self.calc_damage(winner)
        if winner:
            winner = winner.owner
            winner.winning_streak += 1
            winner.win_last_match = True
            loser.owner.winning_streak = 0
            loser.owner.health -= damage

        return winner, damage

    def fight_is_over(self) -> bool:
        """
            return True if one board is empty or minions cant attack (> tie)
            return False otherwise
        """
        for board in self.combattants:
            if not board.cards:
                return True

        for board in self.combattants:
            for minion in board.cards:
                if minion.can_attack:
                    return False

        return True

    def begin_fight(self) -> tuple:
        for board in self.combattants:
            board.attack_case = 0 # servant in this case attack first

        self.attacker = self.calc_initiative(*self.combattants)
        self.game.active_global_event(Event.FIRST_STRIKE, *self.combattants_player)

        while not self.fight_is_over():
            self.next_round()
            self.game.active_action()
            self.attacker = self.attacker.opponent

        return self.who_is_winner()

    def who_is_winner(self) -> Tuple[object, object] or Tuple[None, None]:
        j1, j2 = self.combattants
        if j1.cards:
            if j2.cards:
                return None, None
            return self.combattants
        elif not j2.cards:
            return None, None
        return j2, j1

    def calc_damage(self, winner):
        if winner is None:
            return 0

        return sum([entity.level for entity in [winner.owner]+winner.cards])

    def next_round(self):
        # search first attacker
        attacker_minion = None
        for i in range(BATTLE_SIZE):
            attacker_minion_position = (self.attacker.attack_case + i) % BATTLE_SIZE
            minion = self.attacker.cards[attacker_minion_position]
            if minion and minion.can_attack:
                attacker_minion = minion
                break

        if attacker_minion:
            self.minion_attack(attacker_minion)

    def minion_attack(self, attacker_minion):
        for _ in range(attacker_minion.how_many_time_can_I_attack()):
            self.game.append_action(attacker_minion.prepare_attack)
            attacker_minion.active_action()

        if attacker_minion.is_alive:
            self.attacker.attack_case += 1
            self.attacker.attack_case %= len(self.attacker.cards)

    def calc_initiative(self, board_j1, board_j2):
        if len(board_j1.cards) > len(board_j2.cards) or \
                random.randint(0, 1) and len(board_j2.cards) == len(board_j1.cards):
            return board_j1
        return board_j2
