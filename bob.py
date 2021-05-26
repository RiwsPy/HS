import json
import constants
import random
import card
import board
import hand
import power
import hero

class Bob:
    def __init__(self, type_ban=0):
        self.pseudo = 'Bob'
        self.nb_turn = 0
        self.arene = False

        self.all_card = self.normalize_bdd_card()
        self.all_hero = self.normalize_bdd_hero()
        self.all_effect = self.normalize_bdd_effect()
        self.all_secret_key = []

        self.type_not_ban = constants.TYPE_ALL - type_ban
        self.hand = hand.Bob_hand(self)

        self.card_can_collect = {}
        self.nb_card_by_syn = { nb: [0]*(constants.LEVEL_MAX+1)
            for nb in constants.TYPE_NAME }

        for key, info in self.all_card.items():
            if info['general'] == 'secret':
                self.all_secret_key.append(key)

            if 'cant_collect' in info:
                continue

            card_synergy = info["synergy"]
            card_level = info["level"]
            self.nb_card_by_syn[card_synergy][card_level] += constants.CARD_NB_COPY[card_level]

            if not card_synergy or card_synergy & self.type_not_ban:
                self.card_can_collect[key] = info

                for _ in range(constants.CARD_NB_COPY[card_level]):
                    crd = card.Card(key, self)
                    crd.from_bob = True
                    self.hand.append(crd)

        self.minion_cost = constants.BOB_MINION_COST
        self.print_bdd_card()

        self.hero_can_collect = {}
        for hero_key, hero_info in self.all_hero.items():
            if 'cant_collect' in hero_info or hero_info['synergy'] & type_ban:
                continue
            self.hero_can_collect[hero_key] = hero_info

        self.hero = hero.Hero(self, "", None)
        self.power = power.Power(self.hero.script_power, self)
        self.boards = {} # contient le board de bob pour chaque joueur

    def normalize_bdd_card(self):
        with open("bdd_card.json", "r", encoding="utf-8") as file:
            all_card = json.load(file)

        for key, value in all_card.copy().items():
            if value['general'] == 'minion':
                for info in ['init_state', 'type', 'synergy']:
                    v = value.get(info, '0x0')
                    all_card[key][info] = int(v, 16)

                v = value.get('script')
                if v:
                    all_card[key]['script'] = {int(k, 16): v for k, v in v.items()}
        return all_card

    def normalize_bdd_hero(self):
        # chargement heroes
        with open("bdd_hero.json", "r", encoding="utf-8") as file:
            dic = json.load(file)

        for key, hero in dic.items():
            dic[key]['synergy'] = int(hero.get('synergy', '0x0'), 16)
        return dic

    def normalize_bdd_effect(self):
        with open("bdd_effect.json", "r", encoding="utf-8") as file:
            dic = json.load(file)

        return dic

    def print_bdd_card(self):
        len_max = 0
        for synergy_name in constants.TYPE_NAME.values():
            len_max = max(len_max, len(synergy_name))
        separator = ' :'

        with open('bdd_card', 'w', encoding='utf-8') as file:
            title = 'Présence des différentes synergies :\n'
            line_1 = ' '*(len_max+len(separator))
            for i in range(1, constants.LEVEL_MAX+1):
                line_1 += f'T{i}'.center(4)
            line_1 += 'Total\n'

            file.write(title)
            file.write(line_1)

            line_x = ''
            check_all_cards = self.nb_card_by_syn
            for key, value in check_all_cards.items():
                line_x += constants.TYPE_NAME[key].ljust(len_max) + separator

                value = value[1:] # exclusion des cartes de niveau 0
                line_x += ''.join(map(lambda x: str(x).rjust(4), value))
                line_x += str(sum(value)).rjust(5) + '\n'
            file.write(line_x)

            last_line = 'Total'.ljust(len_max) + separator
            som = 0
            for i in range(1, constants.LEVEL_MAX+1):
                total = 0
                for j in check_all_cards.values():
                    total += j[i]
                last_line += str(total).rjust(4)
                som += total
            last_line += str(som).rjust(5)
            file.write(last_line)        

    @property
    def bob(self):
        return self

    @property
    def gold(self):
        return constants.MAX_GOLD

    @gold.setter
    def gold(self, value):
        pass

    def buy_card(self, card, cost):
        pass

    def sell_card(self, card, cost):
        pass

    def begin_turn(self, no_bob=False, recursive=True):
        self.nb_turn += 1
        for player, board in self.boards.items():
            board.drain_minion() # facultatif / sécurité ?
            if not no_bob:
                board.fill_minion()
            player.begin_turn(recursive=recursive, opponent_board=board)

    def end_turn(self, no_bob=False):
        for player, board in self.boards.items():
            player.end_turn()
            board.drain_minion()

    def can_buy_minion(self):
        return True

    def go_party(self, *player_lst):
        """
            Crée un board de bob pour chaque joueur, contenu dans self.boards
        """
        #NB_PLAYER = constants.NB_PLAYER
        #if len(player_lst) != NB_PLAYER:
        #    print(f"{NB_PLAYER} joueurs attendus pour la partie !")
        #    return None

        for player in self.boards:
            player.all_in_bob()

        self.nb_turn = 0
        self.boards = {player: board.Board(self)
            for player in player_lst}
        for player, brd in self.boards.items():
            brd.opponent = player.board
            player.initialize()

        # non aleatoire, provisoire pour test
        for i in range(0, len(player_lst), 2):
            player_lst[i].next_opponent = player_lst[i+1]
        """ alea
        for i in range(NB_PLAYER//2):
            j1 = player_lst.pop(random.randint(0, len(player_lst)-1))
            j2 = player_lst.pop(random.randint(0, len(player_lst)-1))
            j1.next_opponent = j2
            j2.next_opponent = j1
        """

    def nb_card_of_tier_max(self, tier_max=constants.LEVEL_MAX, tier_min=1):
        # renvoie le nombre de cartes théoriques présentes dans la taverne de bob de niveau tier_max ou moins
        som = 0
        for syn, nb_card_by_level in self.nb_card_by_syn.items():
            if not syn or syn & self.type_not_ban:
                som += sum(nb_card_by_level[tier_min:max(tier_min, tier_max)+1])
        return som

    def card_of_tier_max(self, tier_max=constants.LEVEL_MAX, tier_min=1):
        # renvoie le dictionnaire de toutes les cartes de niveau ou égal à celui de tier_max
        return {key: value
            for key, value in self.card_can_collect.items()
                if tier_min <= value["level"] <= tier_max}

    def card_synergy_by_level(self, type_, tier_max=constants.LEVEL_MAX, tier_min=1):
        # renvoie le dictionnaire des cartes d'une synergie précise et d'un niveau compris entre tier_min et tier_max
        # retire toutes les autres
        return {key: value
            for key, value in self.card_can_collect.items()
                if value['synergy'] == type_ and tier_min <= value['level'] <= tier_max}

    def card_type_by_level(self, type_, tier_max=constants.LEVEL_MAX, tier_min=1):
        # renvoie le dictionnaire des cartes d'un type précis et d'un niveau compris entre tier_min et tier_max
        # retire toutes les autres
        return {key: value
            for key, value in self.card_can_collect.items()
                if value['type'] & type_ and tier_min <= value['level'] <= tier_max}

    def active_event(self, event, *arg):
        pass
