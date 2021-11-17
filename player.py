from collections import defaultdict
from enums import LEVELUP_COST, NB_CARD_BY_LEVEL, MAX_GOLD, \
    GOLD_BY_TURN, LEVEL_MAX, CardName, Type, BOARD_SIZE
import hand
from entity import Entity
from utils import Card_list
from stats import *
from sequence import Sequence

class Player(Entity):
    default_attr = {
        '_max_health': 40,
        '_health': 40,
        '_gold': 0,
        'is_bot': False,
        'combat': None,
        'field': None,
        'bonus_nomi': 0,
        #'method': 'player', # ??
        'levelup_cost_mod': 0,
        'card_by_roll_mod': 0,
    }
    def __init__(self, dbfId, **kwargs):
        champion = kwargs.pop('champion')
        pseudo = kwargs.pop('pseudo')
        super().__init__(champion,
            fights=[],
            gold_by_turn=GOLD_BY_TURN[:],
            bought_minions=defaultdict(Card_list),
            sold_minions=defaultdict(Card_list),
            played_cards=defaultdict(Card_list),
            **kwargs)

        self.pseudo = pseudo
        self.health = self.max_health
        if self.dbfId != CardName.BOB:
            self.hand = hand.Player_hand()
            self.append(self.hand)
            self.board = self.create_card(CardName.DEFAULT_BOARD)
            self.secret_board = self.create_card(CardName.DEFAULT_SECRET_BOARD)
            self.graveyard = self.create_card(CardName.DEFAULT_GRAVEYARD)
            self.graveyard.owner = self

            self.append(self.board)
            self.append(self.secret_board)
        self.power = self.create_card(self.power_id)
        #self.method = 'player'
        self.append(self.power)

    def __repr__(self) -> str:
        return f'{self.pseudo} {self.name} (pv: {self.health})'

    @property
    def max_health(self) -> int:
        return self._max_health

    @max_health.setter
    def max_health(self, value) -> None:
        bonus = value - self.max_health
        self._max_health = value
        if bonus < 0:
            self.health = min(self.health, value)

    @property
    def is_alive(self):
        return self.health > 0

    @property
    def minion_cost(self) -> int:
        return self.power.minion_cost

    @property
    def level(self) -> int:
        return self.bob.level

    @level.setter
    def level(self, value) -> None:
        self.bob.level = value

    @property
    def opponent(self):
        if self is not self.field.p1:
            return self.field.p1
        return self.field.p2

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value) -> None:
        self._health = value

    def dec_health(self, value):
        self.health -= value

    @property
    def winning_streak(self) -> int:
        ret = 0
        for fight in self.fights:
            if fight.winner is self.board:
                ret += 1
            elif fight.loser is self.board:
                break

        return ret

    @property
    def win_last_match(self) -> bool:
        if self.fights:
            return self.fights[-1].winner is self.board
        return False

    @property
    def gold(self) -> int:
        return self._gold

    @gold.setter
    def gold(self, value) -> None:
        gold_spend = self._gold - value
        """
        if gold_spend > 0:
            for origin, info in self.board.aura:
                if info['spend_gold']:
                    origin.quest_value += gold_spend
                    if info['check']:
                        getattr(script_minion, info['check'])(origin)
        """
        self._gold = max(0, min(MAX_GOLD, value))

    def nb_gold_by_turn(self) -> int:
        try:
            return GOLD_BY_TURN[self.nb_turn]
        except IndexError:
            return GOLD_BY_TURN[-1]

    @property
    def levelup_cost(self) -> int:
        return max(0, 
            LEVELUP_COST[self.level] +\
            self.power.levelup_cost_mod +\
            self.levelup_cost_mod)

    def can_buy_minion(self, cost=None) -> bool:
        return not self.hand.is_full and\
            (cost is None and self.gold >= self.minion_cost or
            self.gold >= cost)

    def die(self, *args, **kwargs) -> None:
        # s'active au début du tour ?
        # gestion bloc de glace > ne s'active que lors de 'FIGHT'
        pass

    def roll(self, sequence: Sequence=None) -> None:
        if sequence is None:
            Sequence('ROLL', self, cost=self.cost_next_roll).start_and_close()
        else:
            if self.gold >= sequence.cost:
                self.gold -= max(0, sequence.cost)
                self.bob.board.roll(sequence)
            else:
                sequence.is_valid = False

    @property
    def cost_next_roll(self) -> int:
        #TODO: rajouter un moyen de connaître le vrai coût du roll avant de l'effectuer
        return max(0, self.power.roll_cost)

    def roll_start(self, sequence: Sequence=None) -> None:
        sequence.is_valid = not self.in_fight_sequence

    def levelup(self, sequence=None):
        if sequence is None:
            Sequence('LEVELUP', self).start_and_close()

    def levelup_start(self, sequence) -> None:
        if self.level >= LEVEL_MAX or\
                self.gold < self.levelup_cost:
            sequence.is_valid = False
            return

        self.gold -= self.levelup_cost
        self.levelup_cost_mod = 0
        self.level += 1

    @property
    def nb_card_by_roll(self) -> int:
        return min(BOARD_SIZE, 
            NB_CARD_BY_LEVEL[self.level] +
            self.card_by_roll_mod +
            self.power.card_by_roll_mod)



class Bob(Player):
    default_attr = {
        '_max_health': 40,
        '_health': 40,
        'level': 1,
        #'method': "bob",
    }

    def __init__(self, **attr) -> None:
        super().__init__(
            CardName.DEFAULT_PLAYER, 
            pseudo='Bob', 
            champion=CardName.BOB, 
            **attr,
            nb_minion_by_refresh_list=NB_CARD_BY_LEVEL[:],
            )
        self.type = Type.BOB
        self.id = 'bob'
        self.board = self.create_card(CardName.DEFAULT_BOB_BOARD)
        self.append(self.board)
        self.power = self.create_card(self.power_id)
        self.append(self.power)

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value) -> None:
        self._level = max(1, min(LEVEL_MAX, value))

    @property
    def is_alive(self):
        return True

    @property
    def hand(self) -> hand:
        return self.game.hand

    @property
    def local_hand(self) -> Card_list:
        return self.hand.cards_of_tier_max(tier_max=self.level, tier_min=1)

    @property
    def nb_card_by_refresh(self) -> int:
        return min(BOARD_SIZE, self.nb_minion_by_refresh_list[self.level])

    @property
    def gold(self) -> int:
        return MAX_GOLD

    @gold.setter
    def gold(self, _) -> None:
        pass

    def can_buy_minion(self, *args, **kwargs) -> bool:
        return True

    def die(self, *args, **kwargs) -> None:
        pass
    summon_on= die
