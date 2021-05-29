import random
import script_functions
import constants
import bob

class Combat:
    def __init__(self, *combattants):
        for player in combattants:
            if type(player) is bob.Bob:
                print("bob fight ??")
                return None

        # sauvegarde du board des joueurs
        # + rechargement du board à l'identique à la fin du combat
        self.combattants = self.calc_initiative(*combattants)
        j1, j2 = self.combattants
        self.attacker = j1
        self.defenser = j2
        self.attacker_minion = None
        self.defenser_minion = None

        j1.opponent = j2
        j2.opponent = j1
        j1.board.opponent = j2.board
        j2.board.opponent = j1.board
        j1.fight = self
        j2.fight = self

    def fight_initialisation(self):
        """
            *return: winner id and total damage to loser
            *rtype: tuple
        """
        #j1, j2 = self.combattants
        #print(f"Combat entre {j1.pseudo} ({j1.hero}) et {j2.pseudo} ({j2.hero}) !")
        winner, loser = self.begin_fight()

        for player in self.combattants:
            if player != winner:
                player.win_last_match = False

        if winner:
            winner.winning_streak += 1
            winner.win_last_match = True
            loser.winning_streak = 0

        return winner, self.calc_damage(winner)

    def fight_is_over(self):
        """
            return True if only one board is empty or no servant can attack (> tie)
            return False otherwise
        """
        for player in self.combattants:
            if not player.board:
                break

            for minion in player.board:
                if minion.can_attack():
                    return False

        return True

    def begin_fight(self):
        # power_event is actived before minion_event
        for player in self.combattants:
            player.active_power_event(constants.EVENT_FIRST_STRIKE)
            player.active_secret_event(constants.EVENT_FIRST_STRIKE)
            player.attack_case = 0 # servant in this case attack first

        for player in self.combattants:
            self.check_attack_immediatly(player)

        for player in self.combattants:
            player.active_minion_event(constants.EVENT_FIRST_STRIKE)

        while not self.fight_is_over():
            self.next_round()
            self.combattants = self.combattants[1], self.combattants[0]

        return self.who_is_winner()

    def who_is_winner(self):
        j1, j2 = self.combattants
        if j1.board:
            if j2.board:
                return None, None
            return self.combattants
        elif not j2.board:
            return None, None
        return j2, j1

    def calc_damage(self, winner):
        if not winner:
            return 0

        damage = winner.level
        for minion in winner.board:
            damage += minion.level

        return damage

    def next_round(self):
        #TODO: décomposer en phase ?

        for player in self.combattants:
            self.check_attack_immediatly(player)

        self.attacker, self.defenser = self.combattants
        attacker_minion = None
        nb_minion = len(self.attacker.board)

        # search first attacker
        for i in range(nb_minion):
            attacker_minion_position = (self.attacker.attack_case + i) % nb_minion
            minion_check = self.attacker.board[attacker_minion_position]
            if minion_check.can_attack():
                attacker_minion = minion_check
                break

        if not attacker_minion:
            return None

        self.attacker_minion = attacker_minion
        defenser_minion = self.search_target(attacker_minion, self.defenser)
        if not defenser_minion:
            return None

        self.defenser_minion = defenser_minion
        self.attacker.active_event(constants.EVENT_ATK_ALLY, attacker_minion)
        self.defenser.active_event(constants.EVENT_DEFEND_ALLY, defenser_minion)

        self.minion_fight()

    def search_target(self, attacker_minion, defenser):
        nb_attack_max = attacker_minion.how_many_time_can_I_attack()

        while nb_attack_max > 0 and attacker_minion.is_alive and defenser.board:
            nb_attack_max -= 1

            if not attacker_minion.state_fight & constants.STATE_ATTACK_WEAK: # attaque classique
                targets = [minion
                    for minion in defenser.board
                        if minion.state_fight & constants.STATE_TAUNT] or\
                        defenser.board[:] # minion with taunt or all minion

            else: # Zapp Mèche-Sournoise : attaque le plus faible
                targets = [defenser.board[0]]
                atk_min = defenser.board[0].attack
                for minion in defenser.board[1:]:
                    atk = minion.attack
                    if atk < atk_min:
                        atk_min = atk
                        targets = [minion]
                    elif atk == atk_min:
                        targets.append(minion)

            if targets:
                return random.choice(targets)

        return None

    def minion_fight(self):
        attacker_minion = self.attacker_minion
        defenser_minion = self.defenser_minion

        # servant trade
        self.take_damage(attacker_minion, defenser_minion)
        self.take_cleave_damage(attacker_minion, defenser_minion)
        self.take_damage(defenser_minion, attacker_minion, overkill=False) # dégâts défensifs, pas de brutalité

        attacker_minion.active_script_type(constants.EVENT_AFTER_ATK_MYSELF) # Ara monstrueux

        self.resolve_damage_event(attacker_minion.owner, attacker_minion)
        self.resolve_damage_event(defenser_minion.owner, attacker_minion)

        if attacker_minion.is_alive:
            self.combattants[0].attack_case = attacker_minion.position + 1
        else:
            self.combattants[0].attack_case = attacker_minion.position

    def take_cleave_damage(self, attacker_minion, defenser_minion, damage=None):
        if attacker_minion.state_fight & constants.STATE_CLEAVE: # cleave
            for minion in defenser_minion.adjacent_neighbors():
                self.take_damage(attacker_minion, minion, damage=damage)

    def check_attack_immediatly(self, player):
        for minion in player.board:
            if minion.state_fight & constants.STATE_ATTACK_IMMEDIATLY and minion.attack:
                self.search_target(minion, player.opponent)

    def create_single_damage_event(self, attacker, defenser, damage=None, overkill=False):
        self.take_damage(attacker, defenser, damage, overkill)
        self.resolve_single_damage_event(attacker, defenser)

    def take_damage(self, damager, damagee, damage=None, overkill=True):
        if damage is None:
            damage = damager.attack

        if not damage:
            return None

        if damagee.state_fight & constants.STATE_DIVINE_SHIELD: # bouclier divin
            damagee.remove_state(constants.STATE_DIVINE_SHIELD)
            damagee.owner.owner.active_event(constants.EVENT_LOSS_SHIELD)
        else:
            damagee.active_script_type(constants.EVENT_HIT_BY)
            damagee.health -= damage
            if damager.state_fight & constants.STATE_POISONOUS:
                damagee.state_fight |= constants.STATE_IS_POISONED

            if overkill and damagee.health < 0 and constants.EVENT_OVERKILL in damager.script:
                damager.active_script_type(constants.EVENT_OVERKILL, damagee)

    def resolve_damage_event(self, board, attacker):
        for defenser in board[::-1]:
            self.resolve_single_damage_event(attacker, defenser)

    def resolve_single_damage_event(self, attacker, defenser):
        if not defenser.is_alive:
            defenser.die(killer=attacker)

    def calc_initiative(self, j1, j2):
        j1_nb_cards, j2_nb_cards = len(j1.board), len(j2.board)
        if j1_nb_cards > j2_nb_cards:
            return j1, j2
        if j2_nb_cards > j1_nb_cards or random.randint(0, 1):
            return j2, j1
        return j1, j2
