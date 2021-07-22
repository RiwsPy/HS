from collections import defaultdict
from enums import Event, Type, LEVEL_UP_COST, State, NB_CARD_BY_LEVEL, MAX_GOLD, \
    GOLD_BY_TURN, LEVEL_MAX
import board
import hand
from entity import Card, Entity
from utils import Card_list
from stats import *
import random

class Player(Entity):
    default_attr = {
        '_max_health': 40,
        '_health': 40,
        'state': State.DEFAULT,
        'event': Event.ALL,
        '_gold': 0,
        'is_bot': False,
        'state': State.DEFAULT,
        'winning_streak': 0, # série de victoire
        'win_last_match': False,
        'fight': None,
        'bonus_nomi': 0,
        'method': 'player',
    }
    def __init__(self, pseudo, champion, **kwargs):
        super().__init__(champion,
            gold_by_turn=GOLD_BY_TURN[:],
            bought_minions=defaultdict(Card_list),
            sold_minions=defaultdict(Card_list),
            played_minions=defaultdict(Card_list),
            aura_active={},
            **kwargs)

        self.pseudo = pseudo
        self.health = self.max_health
        if self.type == Type.HERO:
            self.hand = hand.Player_hand()
            self.append(self.hand)
            self.board = board.Board(event=Event.ALL, method="player_board")
            self.append(self.board)
        self.power = Card(self.power_id)
        self.method = 'player'
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
    def minion_cost(self) -> int:
        return self.power.minion_cost

    @property
    def level(self) -> int:
        return self.bob.level

    @level.setter
    def level(self, value) -> None:
        self.bob.level = value

    @property
    def opponent(self) -> board.Board:
        return self.board.opponent.owner

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value) -> None:
        #if value < self._health:
        #    self.active_global_event(Event.LOSS_HP, self)
        self._health = value
        if self._health <= 0:
            # Event DIE ?
            self.active_global_event(Event.DIE_PLAYER, self.game, victim=self)

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
    def roll_cost(self) -> int:
        return self.power.roll_cost

    def can_buy_minion(self, cost=None) -> bool:
        if self.hand.can_add_card():
            if cost is None:
                if self.gold >= self.minion_cost:
                    return True
            elif self.gold >= cost:
                return True
        return False

    def sell_minion(self, card, buyer, cost=None) -> Entity:
        if card.type == Type.MINION and card in self.board.cards:
            if cost is None:
                cost = buyer.minion_cost
            if buyer.can_buy_minion(cost=cost):
                buyer.gold -= cost
                self.gold += cost

                card.active_local_event(Event.SELL, source=card)
                self.active_global_event(Event.SELL, self.controller, source=card)
                buyer.active_global_event(Event.BUY, buyer, source=card)

                buyer.hand.append(card)
                self.sold_minions[self.nb_turn].append(card)
                buyer.bought_minions[self.nb_turn].append(card)
                return card
        return None

    def buy_minion(self, card, cost=None) -> Entity:
        return card.controller.sell_minion(card, self, cost=cost)

    def die(self) -> None:
        # s'active au début du tour ?
        # gestion bloc de glace
        self.active_global_event(Event.DIE, self.game, victim=self)


class Bob(Player):
    default_attr = {
        '_max_health': 40,
        '_health': 40,
        'level': 1,
        'state': State.DEFAULT,
        'event': Event.ALL,
        'nb_free_roll': 0,
        'method': "bob",
    }

    def __init__(self, **attr) -> None:
        super().__init__('Bob', "57110", **attr,
            level_up_cost_list=LEVEL_UP_COST[:],
            nb_minion_by_refresh_list=NB_CARD_BY_LEVEL[:],
            )
        self.level_up_cost = self.level_up_cost_list[self.level]

        self.type = Type.BOB
        self.method = 'bob'
        self.board = board.Bob_board()
        self.append(self.board)
        self.power = Card(self.power_id)
        self.append(self.power)

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value) -> None:
        self._level = max(1, min(LEVEL_MAX, value))

    def level_up(self) -> bool:
        if self.level >= LEVEL_MAX:
            return False

        if self.opponent.gold < self.level_up_cost:
            print(f"Levelup impossible ! {self.opponent.gold} gold")
            return False

        self.opponent.gold -= self.level_up_cost
        self.level += 1
        self.level_up_cost = self.level_up_cost_list[self.level]

        self.active_global_event(Event.LEVELUP, self.opponent)

        return True

    def roll(self, nb=1) -> bool:
        if nb < 1:
            return False

        for _ in range(nb):
            if self.nb_free_roll >= 1:
                self.nb_free_roll -= 1
            elif self.opponent.gold < self.roll_cost:
                return False
            else:
                self.opponent.gold -= self.roll_cost

            self.active_global_event(Event.ROLL, self, self.opponent, source=self.opponent)
        return True

    @property
    def level_up_cost(self) -> int:
        return self._level_up_cost

    @level_up_cost.setter
    def level_up_cost(self, value) -> None:
        self._level_up_cost = max(0, value)

    @property
    def hand(self) -> hand:
        return self.owner.hand

    @property
    def local_hand(self) -> Card_list:
        return self.hand.cards_of_tier_max(tier_max=self.level, tier_min=1)

    @property
    def nb_card_by_refresh(self) -> int:
        return self.nb_minion_by_refresh_list[self.level]

    @property
    def gold(self) -> int:
        return MAX_GOLD

    @gold.setter
    def gold(self, _) -> None:
        pass

    def can_buy_minion(self, *args, **kwargs) -> bool:
        return True

    def die(self) -> None:
        pass



"""

    def pick_random_card(self, lst_card):
        # proba tirage aléatoire
        bob = self.bob
        nb_card_in_bob = bob.nb_card_of_tier_max(tier_max=self.level)
        lst_proba = [
            CARD_NB_COPY[bob.card_can_collect[card]["level"]]/nb_card_in_bob
            for card in lst_card
                if card]
        return lst_proba

    def minion_choice(self, target, *exception, restr=0):
        #TODO: delete
        return self.choose_one_of_them([minion
            for minion in target
                if (not restr or minion.type & restr) and minion not in exception])

    def discover(self, origin, nb=3, typ=0, lvl_max=LEVEL_MAX, lvl_min=1):
            Découvre nb cartes de type typ, de niveau maximum lvl_max et de niveau minimum lvl_min
            Le joueur choisit ensuite l'une d'entre elle et l'ajoute dans sa main
            *param typ: (cf enums.Race.XXX)
            *return: liste des cartes à choisir
        if nb < 1:
            return None

        lst_key_ban = []
        if origin:
            lst_key_ban = [origin.dbfId]
        if type(origin) is Card and origin.general == General.MINION:
            lvl_max = min(lvl_max, self.level)

        lvl_min = min(lvl_min, lvl_max)
        copy_bob = self.bob.hand.cards_type_of_tier_max(typ, lvl_max, lvl_min)
        random.shuffle(copy_bob)

        lst_id = []
        for crd in copy_bob:
            if crd.dbfId not in lst_key_ban:
                if crd.owner:
                    crd.owner.remove(crd)
                crd.owner = None
                lst_id.append(crd)
                if len(lst_id) >= nb:
                    break
                lst_key_ban.append(crd.dbfId)

        self.discover_choice(lst_id)

    def discover_choice(self, lst):
        choice = self.choose_one_of_them(lst)

        if choice:
            if self.hand.append(choice):
                lst.remove(choice)

            for card in lst:
                self.bob.hand.append(card)

    def discover_secret(self, nb=3): # Akazamzarak
        lst = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007"]
        for secret_key in set(self.board.secret_key+self.power.secret_limitation):
            lst.remove(secret_key)

        random.shuffle(lst)
        self.discover_secret_choice(lst[:nb])

    def discover_secret_choice(self, lst):
        choice = self.choose_one_of_them(lst, "Découverte d'un secret")

        if choice:
            card_id = Card(choice)
            card_id.owner = self.board

    def best_card_T1(self, *players, nb_turn=2):
        # renvoie la "meilleure" carte que peut choisir un héros qui rencontre un héros précis au tour n°2
        # puis un héros "classique" au tour n°3

        bob = self.bob.__class__(Race.ALL - self.bob.type_present)
        players = [self.__class__(bob, plyr.name, plyr.hero.dbfId)
            for plyr in players]

        j1, j2, j3, j4, j5 = players[:5]
        bob.go_party(*players)

        opponents = [j1, j2, j3, j4]

        lst = bob.card_of_tier_max(tier_max=1).keys()
        # crée une liste où chaque carte à une chance équiprobable d'être achetée
        proba_lst = j1.pick_random_card(lst)

        dict_lst = {}
        # match 1, j2 contre j1 puis un joueur standard
        result = compo.arene_pondere([j2, j1, j3, j4], [lst]*3, [proba_lst]*3, nb_turn=2, pr=False)
        dict_lst[j2.power.id] = result

        # joueur test
        if j3.power.id != j2.power.id:
            # match 2, j3 contre j4 puis j5
            result = compo.arene_pondere([j3, j4, j5, j3], [lst]*3, [proba_lst]*3, nb_turn=2, pr=False)
            dict_lst[j3.power.id] = result

        proba_lst = [proba_lst] # proba non pondérée pour j1
        lst = [lst]
        for opponent in opponents[1:-1]:
            # stocke le key des cartes listée et triée selon leur classement de l'étape 1
            new_lst = [info[5][0]
                for info in dict_lst[opponent.power.id]]
            lst.append(new_lst)

            opponent.initialize()
            result = opponent.pick_best_card(new_lst) # crée une liste où chaque carte a % d'apparition dépendant de la puissance théorique de la carte  
            proba_lst.append(result)

        result = compo.arene_pondere(opponents, lst, proba_lst, nb_turn) # détermine la "meilleure" carte contre l'adversaire

        new_dict = {info[5][0]: info[1]
            for info in result}

        j1.initialize()
        proba_key = j1.pick_best_card(new_dict.keys())

        return new_dict, esperance(proba_key, new_dict.values())

"""