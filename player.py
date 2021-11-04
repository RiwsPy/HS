from collections import defaultdict
from enums import LEVELUP_COST, NB_CARD_BY_LEVEL, MAX_GOLD, \
    GOLD_BY_TURN, LEVEL_MAX, CardName, Type, FIELD_SIZE
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
        'method': 'player',
        'roll_nb_free': 0,
        'roll_cost_mod': 0,
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
            self.board.opponent.roll(sequence)

    @property
    def cost_next_roll(self) -> int:
        if self.roll_nb_free >= 1:
            return 0
        return max(0, self.power.roll_cost + self.roll_cost_mod)

    def roll_start(self, sequence: Sequence=None) -> None:
        if self.in_fight_sequence or self.gold < sequence.cost:
            sequence.is_valid = False
            return

        self.roll_cost_mod = 0
        self.roll_nb_free = max(0, self.roll_nb_free-1)
        self.gold -= sequence.cost

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
        return min(FIELD_SIZE, 
            NB_CARD_BY_LEVEL[self.level] +
            self.card_by_roll_mod +
            self.power.card_by_roll_mod)



class Bob(Player):
    default_attr = {
        '_max_health': 40,
        '_health': 40,
        'level': 1,
        'method': "bob",
    }

    def __init__(self, **attr) -> None:
        super().__init__(
            CardName.DEFAULT_PLAYER, 
            pseudo='Bob', 
            champion=57110, 
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
    def hand(self) -> hand:
        return self.game.hand

    @property
    def local_hand(self) -> Card_list:
        return self.hand.cards_of_tier_max(tier_max=self.level, tier_min=1)

    @property
    def nb_card_by_refresh(self) -> int:
        return min(FIELD_SIZE, self.nb_minion_by_refresh_list[self.level])

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