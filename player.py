import random
import card
import script_functions
import script_minion
import constants
import stats
from copy import deepcopy
import board
from operator import itemgetter
import compo
import hero
import hand
import power
import script_power
import script_spell

class Player:
    def __init__(self, bob, pseudo, champion=''):
        self.bob = bob
        self.pseudo = pseudo
        self.hero = hero.Hero(bob, champion, self)
        self._power = None
        self.is_bot = False
        self.board = board.Board(self)
        self.power = power.Power(self.hero.script_power, self)
        self.initialize()

        self.active_event(constants.EVENT_CREATION)

    def initialize(self, hp=None):
        self.real_board = board.Board(self)
        self.level = 1
        self._gold = 0
        self.init_hp = 40
        self.nb_free_roll = 0
        self.level_up_cost = None # réinit
        self._hp = hp or self.init_hp
        self.hand = hand.Player_hand(self)
        self.opponent = self.bob # adversaire en cours
        self.fight = None
        self.winning_streak = 0 # série de victoire
        self.win_last_match = False
        self._next_opponent = None # adversaire rencontré après un end_turn
        self.last_opponent = None
        #self.nb_lapin = 0
        self.attack_case = 0
        self.minion_buy_this_turn = []
        self.minion_play_this_turn = []
        self.bonus_nomi = 0
        self.all_in_bob()

        return self

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, id):
        if self._power:
            self.board.refresh_aura() # Dangerous ???!
        self._power = id

    @property
    def next_opponent(self):
        return self._next_opponent

    @next_opponent.setter
    def next_opponent(self, player):
        self._next_opponent = player
        player._next_opponent = self

    @property
    def nb_card_by_refresh(self):
        if self.power.id == 6: # vision spectrale
            return 7
        return constants.NB_CARD_BY_LEVEL[self.level]

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if not self.is_insensible:
            if value != self._hp:
                self.active_event(constants.EVENT_LOSS_HP)
            self._hp = value
            if self._hp <= 0:
                self.active_event(constants.EVENT_DIE_PLAYER)
                #print(f"{self.pseudo} meurt !")

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        self._gold = max(0, min(constants.MAX_GOLD, value))

    @property
    def is_insensible(self):
        if self.board:
            for value in self.board.aura.values():
                if value['insensible']:
                    return True
        return False

    def end_turn(self):
        if self.is_bot:
        #if True:
            self.auto_placement_card()

        self.active_event(constants.EVENT_END_TURN)

        # sauvegarde des valeurs et du board
        self.real_board.copy(self.board)

        for minion in self.board:
            minion.state_fight = minion.state
        #    minion.init_state |= minion.state
        #    minion.reinitialize(self.board)

        self.opponent = self.next_opponent

    @property
    def minion_cost(self):
        return self.power.minion_cost

    @property
    def nb_turn(self):
        return self.bob.nb_turn

    def begin_turn(self, recursive=True, opponent_board=None):
        self.minion_buy_this_turn = []
        self.minion_play_this_turn = []
        self.power.reset_power()
        self.level_up_cost -= 1
        self.gold = self.nb_gold_by_turn()

        self.board.copy(self.real_board)
        self.last_opponent = self.opponent
        self.opponent = self.bob
        if opponent_board is None:
            self.board.opponent = self.bob.boards[self]
        else:
            self.board.opponent = opponent_board

        for minion in self.board:
            minion.purge_fight_effects(minion.owner)

        self.active_event(constants.EVENT_BEGIN_TURN)

        if self.is_bot and not self.bob.arene:
            self.power.active_script(recursive)

    def nb_gold_by_turn(self):
        lst = constants.GOLD_BY_TURN

        try:
            result = lst[self.nb_turn]
        except IndexError:
            return lst[-1]
        return result

    @property
    def bob_board(self):
        return self.bob.boards.get(self)

    def level_up(self):
        if self.level > 5:
            return False

        if self.gold < self.level_up_cost:
            print("Levelup impossible !")
            return False

        self.gold -= self.level_up_cost
        self.level += 1
        self.level_up_cost = None

        self.active_event(constants.EVENT_LEVELUP)

        return True

    def roll(self, nb=1):
        if nb <= 0:
            return False

        for _ in range(nb):
            if self.nb_free_roll > 0:
                self.nb_free_roll -= 1
            elif self.gold < self.power.roll_cost:
                #print("Roll impossible !")
                return False
            else:
                self.gold -= self.power.roll_cost

            self.active_event(constants.EVENT_ROLL)

            #self.bob.refresh_all_board(self)
            self.board.opponent.drain_all_minion()
            self.board.opponent.fill_minion()
        return True

    def buy_card(self, card, cost):
        self.gold -= cost
        self.active_event(constants.EVENT_BUY, card)
        self.minion_buy_this_turn.append(card)

        return card

    def sell_card(self, card, cost):
        self.gold += cost
        self.active_event(constants.EVENT_SELL, card)
        return card

    def all_in_bob(self):
        while self.board or self.real_board or self.hand:
            for minion in self.hand[::-1]:
                self.bob.hand.append(minion)
            for minion in self.real_board[::-1]:
                self.bob.hand.append(minion)
            for minion in self.board[::-1]:
                self.bob.hand.append(minion)
            self.real_board.copy(self.board)

    def can_buy_minion(self):
        if self.gold >= self.minion_cost:
            if self.hand.can_add_card():
                return True
            else:
                pass
                #print(f"Main pleine !")
        else:
            pass
            #print("Pas assez d'or !")

        return False

    def force_buy_card(self, key_number, position=constants.BATTLE_SIZE):
        """
            Ajoute une carte de key_number dans le board de bob, l'achète et la joue pour le joueur
            La carte est créée si nécessaire sinon elle est retirée de la main de bob
        """
        find = False
        serv = self.bob.card_can_collect.get(key_number)
        if serv:
            for minion in self.bob.hand.cards_of_tier(serv['level']):
                if minion.key_number == key_number:
                    find = True
                    break
        if not find:
            minion = card.Card(key_number, self.bob)

        minion.play(board=self.board.opponent)

        if minion.trade():
            minion.play(position=position)
            return minion
        print(f"cant trade {key_number} {minion.owner}")
        return None

    @property
    def level_up_cost(self):
        return self._level_up_cost

    @level_up_cost.setter
    def level_up_cost(self, value):
        if value is None:
            value = self.power.lst_bob_cost[self.level]
        self._level_up_cost = max(0, value)

    def auto_placement_card(self): # tri du plus fort au plus faible
        if not self.board or len(self.board) < 2:
            return None

        lst_atk = [[serviteur, serviteur.attack, serviteur.health]
            for serviteur in self.board]

        # placement initial de la plus forte attaque à la moins
        lst_atk_asc = sorted(lst_atk, key=itemgetter(1, 2), reverse=True)
        for key, serviteur in enumerate(lst_atk_asc):
            self.board[key] = serviteur[0]

        copy_board = self.board[:]
        for minion in copy_board: # placement du gros boum au début
            #TODO moyen de connaître efficacement l'effet du râle ??
            if minion.key_number in ('206', '206_p'):
                minion.play(board=self.board, position=0)

        copy_board = self.board[:]
        for minion in copy_board: # placement des râles au début
            #TODO moyen de connaître efficacement l'effet du râle ??
            if minion.key_number in ('207', '207_p', '221', '221_p', '108', '108_p'):
                minion.play(board=self.board, position=0)

        copy_board = self.board[:]
        for minion in copy_board[:-1]: # placement des hiteurs à la fin
            if minion.have_script_type(constants.EVENT_HIT_BY):
                minion.play(board=self.board)

        copy_board = self.board[:]
        for minion in copy_board[:-1]: # placement des enchanteurs à la fin
            if minion.have_script_type(constants.EVENT_PLAY_AURA):
                minion.play(board=self.board)

        copy_board = self.board[:]
        for minion in copy_board[:-1]: # placement des bonus d'invocation à la fin
            if minion.have_script_type(constants.EVENT_INVOC):
                minion.play(board=self.board)

        copy_board = self.board[:]
        for minion in copy_board[:-1]: # placement des charognards à la fin
            if minion.have_script_type(constants.EVENT_DIE_ALLY) or\
                minion.have_script_type(constants.EVENT_KILLER_ALLY):
                minion.play(board=self.board)

        copy_board = self.board[:]
        for minion in copy_board: # placement des charognards à la fin
            if minion.key_number in ('222', '222_p'):
                if len(copy_board) > 2:
                    minion.play(board=self.board, position=len(copy_board)-2)
                else: # en dernier
                    minion.play(board=self.board)

        # placement d'un fusible devant en cas de bouclier divin
        # + or compo mech with level >= 4
        if self.next_opponent and self.next_opponent.power.id == 4: # Al'Akir
            for fusible in lst_atk_asc[::-1]:
                if fusible[0].attack > 0 and not fusible.have_script_type(constants.EVENT_DIE_ALLY):
                    fusible.play(position=0, board=fusible.owner)
                    break

    def minion_choice(self, target, *exception, restr=0):
        target = [minion
            for minion in target
                if (not restr or minion.type & restr) and minion not in exception]
        if target:
            if self.is_bot:
                return random.choice(target)
            elif len(target) == 1:
                return target[0]

            print('Quelle cible choissisez-vous ?')
            for nb, minion in enumerate(target):
                print(f'{nb}- {minion}')
            while True:
                try:
                    ch = int(input())
                    minion = target[ch]
                except IndexError:
                    print('Valeur incorrecte.')
                else:
                    break
            return minion
        return None

    def active_event(self, event, *arg):
        self.active_power_event(event, *arg)
        self.active_secret_event(event, *arg)
        self.active_minion_event(event, *arg)

    def active_power_event(self, event, *arg):
        if self.power and self.power.script:
            if event & self.power.type:
                getattr(script_power, self.power.script,
                    getattr(script_power, 'no_power'))(self, event, *arg)
        if self.bonus_nomi:
            script_power.active_nomi_bonus(self, event, *arg)

    def active_secret_event(self, event, *arg):
        if self.board.secret and event in self.board.secret:
            for secret in self.board.secret[event]:
                result = getattr(script_spell, secret.script[event])(self, *arg)
                if result:
                    self.board.secret[event].discard(secret.script[event])

    def active_minion_event(self, event, *arg):
        for minion in self.board:
            minion.active_script_type(event, *arg)

    def pick_random_card(self, lst_card):
        # proba tirage aléatoire
        bob = self.bob
        nb_card_in_bob = bob.nb_card_of_tier_max(tier_max=self.level)
        lst_proba = [
            constants.CARD_NB_COPY[bob.card_can_collect[card]["level"]]/nb_card_in_bob
            for card in lst_card
                if card]
        return lst_proba

    def pick_best_card(self, lst):
        # pour le moment, ne pick aucune carte !
        # fait un classement des meilleures cartes théoriques en fonction des types bannis
        # calcul ensuite la probabilité d'obtention de chaque carte
        # par la suite lancera une nouvelle arène pour déterminer la meilleure carte en fonction du % de pick
        bob = self.bob
        nb_card_in_bob = bob.nb_card_of_tier_max(tier_max=self.level)
        cumul_proba = 1
        new_lst = []
        # problème si la liste est vide (AFKah...)
        for card in lst:
            #if card and card in bob.card_can_collect:
            proba_obtention = cumul_proba *(1 - stats.hypgeo(0, self.nb_card_by_refresh,\
                constants.CARD_NB_COPY[bob.card_can_collect[card]["level"]], nb_card_in_bob))
            cumul_proba -= proba_obtention
            new_lst.append(proba_obtention)
            #else:
            #    print(card)
            #    # /!\ fonctionnel uniquement car tier_min == tier_max
            #    nb_unique_card_T1 = int(bob.nb_card_of_tier_max(1)/constants.CARD_NB_COPY[1])
            #    new_lst = [1/nb_unique_card_T1]*nb_unique_card_T1
        return new_lst

        # génération des combats correspondant au tour du joueur
        # probabilité d'obtention de chaque carte

    def discover(self, origin, nb=3, typ=0, lvl_max=constants.LEVEL_MAX, lvl_min=1):
        """
            Découvre nb cartes de type typ, de niveau maximum lvl_max et de niveau minimum lvl_min
            Le joueur choisit ensuite l'une d'entre elle et l'ajoute dans sa main
            *param typ: (cf constants.TYPE_XXX)
            *return: liste des cartes à choisir
        """
        if nb < 1:
            return None

        lst_key_ban = []
        if type(origin) is card.Card and origin.general == "minion":
            lvl_max = min(lvl_max, self.level)
            lst_key_ban.append(origin.key_number) # une carte ne peut se découvrir elle-même

        lvl_min = min(lvl_min, lvl_max)
        copy_bob = self.bob.hand.cards_type_of_tier_max(typ, lvl_max, lvl_min)
        lst_id = []
        while copy_bob and nb:
            random_card = random.choice(copy_bob)
            copy_bob.remove(random_card)
            if random_card.key_number not in lst_key_ban:
                nb -= 1
                random_card.owner = None
                self.bob.hand.remove(random_card)
                lst_id.append(random_card)
                lst_key_ban.append(random_card.key_number)

        self.discover_choice(lst_id)

    def discover_choice(self, lst):
        if not lst:
            return None

        #TODO !
        if self.is_bot:
            choice = lst[-1] # statistiquement, la dernière carte est la meilleure
        else:
            choice = random.choice(lst)

        # c'est à la résolution que l'on vérifie que la main du joueur peut contenir la-dite carte
        if self.hand.append(choice):
            lst.remove(choice)

        for card in lst:
            self.bob.hand.append(card)

    def discover_secret(self, nb=3): # Akazamzarak
        lst = self.bob.all_secret_key[:]
        for secret_key in set(self.board.secret_key+self.power.secret_limitation):
            lst.remove(secret_key)

        random.shuffle(lst)
        self.discover_secret_choice(lst[:nb])

    #TODO
    def discover_secret_choice(self, lst):
        if not lst:
            return None

        # TODO
        choice = lst[-1]

        self.board.append(card.Card(choice, self.bob, self))

    def best_card_T1(self, *players, nb_turn=2):
        # renvoie la "meilleure" carte que peut choisir un héros qui rencontre un héros précis au tour n°2
        # puis un héros "classique" au tour n°3

        bob = self.bob.__class__(constants.TYPE_ALL - self.bob.type_not_ban)
        players = [self.__class__(bob, plyr.pseudo, plyr.hero.key)
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
        esperance = stats.esperance(proba_key, new_dict.values())

        return new_dict, esperance
        