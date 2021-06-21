from script_minion import *
from script_power import *

class no_method:
    pass

class player_board:
    def begin_turn(self):
        self.last_opponent = self.opponent
        self.opponent = self.owner.bob.board
        #self.next_opponent = ??

    def end_fight(self):
        self.cards = self.cards_copy[:]
        self.entities = self.entities_copy[:]

    def end_turn(self):
        self.cards_copy = self.cards[:]
        self.entities_copy = self.entities[:]
        #if self.is_bot:
        if True:
            self.auto_placement_card()

class bob:
    end_turn = lambda x: x.board.drain_minion()

    def begin_turn(self):
        self.board.fill_minion()
        for entity in self.board.cards:
            entity.calc_stat_from_scratch(heal=True)

    def roll(self):
        self.board.drain_all_minion()
        self.board.fill_minion()

class player:
    def begin_turn(self):
        self.bob.level_up_cost -= 1
        self.gold = self.nb_gold_by_turn()
        self.power.enable()
        self.power.temp_counter = 0
        for entity in self.board.cards:
            entity.calc_stat_from_scratch(heal=True)
