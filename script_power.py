import player
import random
import constants
import bob
import power

def no_power(self, event):
    pass

def Graveyard_shift(self, event):
    self.hp -= 2
    return self.hand.create_card("1001")

def Procrastinate(self, event):
    if self.nb_turn <= 2:
        self.gold = 0
    elif self.nb_turn == 3:
        self.hand.create_card("1010")
        self.hand.create_card("1010")

def Menagerist(self, event):
    if self.nb_turn == 1:
        self.board.create_card("151")

def Avatar_of_nzoth(self, event):
    if self.nb_turn == 1:
        self.board.create_card("154")

def Buried_treasure(self, event):
    self.power.quest_value += 1
    if self.power.quest_value%5 == 0 and self.hand.can_add_card():
        lst = self.bob.hand.cards_of_tier_max(tier_max=self.level)
        card = random.choice(lst)
        lst.remove(card)
        card_inn = [card]
        for minion in lst[::-1]:
            if minion.key_number == card.key_number:
                lst.remove(minion)
                card_inn.append(minion)
                if len(card_inn) > 2:
                    break
        card_p = self.hand.create_card(card.key_number + '_p')
        card_p.card_in = card_inn

def All_patched_up(self, event):
    self.init_hp = 55

def Manastorm(self, event):
    self.power.minion_cost = 2
    self.power.roll_cost = 2
    self.power.lst_bob_cost = constants.LEVEL_UP_COST_MILLHOUSE

def Piggy_bank(self, event):
    self.gold += self.nb_turn

def Boon_of_light(self, event):
    minion = self.minion_choice(self.board)
    if minion:
        minion.state |= constants.STATE_DIVINE_SHIELD
        return minion
    return None

def Pirate_parrrrty(self, event, card=None):
    if event == constants.EVENT_BUY and card.type & constants.TYPE_PIRATE:
        self.power.dec_power_cost()
    elif event == constants.EVENT_USE_POWER:
        self.power.cost = power.BDD_POWER[self.power.id]['cost']
        self.discover(self.power, nb=1, typ=constants.TYPE_PIRATE, lvl_max=self.level)

def Queen_of_dragons(self, event):
    if self.level == 5:
        self.discover(self.power, nb=3, typ=constants.TYPE_DRAGON, lvl_max=6)
        self.discover(self.power, nb=3, typ=constants.TYPE_DRAGON, lvl_max=6)

def Everbloom(self, event):
    self.gold += 2

def Clairvoyance(self, event):
    if self.nb_free_roll <= 0:
        self.nb_free_roll = 1

def Brick_by_brick(self, event):
    if self.board:
        random.choice(self.board).create_and_apply_enchantment("305")

def Tavern_ligthing(self, event):
    minion = self.minion_choice(self.board)
    if minion:
        minion.create_and_apply_enchantment("306", a=self.level, h=self.level)
        return minion
    return None

def Bloodfury(self, event):
    for minion in self.board:
        if minion.type & constants.TYPE_DEMON:
            minion.create_and_apply_enchantment("307")

def Lead_explorer(self, event):
    return self.hand.create_card("10"+str(self.level))

def Avalanche(self, event):
    self.power.quest_value += 1
    if self.power.quest_value%3 == 0:
        self.level_up_cost -= 3

def Stay_frosty(self, event):
    for minion in self.board.opponent:
        if minion.state & constants.STATE_FREEZE:
            minion.create_and_apply_enchantment("308")

def Tinker(self, event, card):
    if card.type & constants.TYPE_MECH:
        card.create_and_apply_enchantment("300")

def Die_insects(self, event):
    self.power.quest_value += 1
    if self.power.quest_value > 24:
        self.power = power.Power(38, self)

def Sulfuras(self, event):
    # le bonus s'active-t-il deux fois si le board ne contient qu'un serviteur ?
    if self.board:
        self.board[0].create_and_apply_enchantment("309")
        self.board[-1].create_and_apply_enchantment("309")

def Puzzle_box(self, event):
    op = self.bob.boards[self]
    if op:
        random_card = random.choice(op)
        self.hand.append(random_card)
        random_card.create_and_apply_enchantment("301")

def A_tale_of_kings(self, event, card=None):  # will not change into the same Hero Power twice in a row
    if event == constants.EVENT_BUY: # achat
        if card.is_type(self.power.quest_value):
            card.create_and_apply_enchantment("303")
    elif event == constants.EVENT_BEGIN_TURN: # détermination du type concerné
        possible_types = self.bob.type_not_ban & (0xFF - self.power.quest_value)
        if possible_types > 0:
            typ = 0
            while not typ & possible_types:
                typ = 2**random.randint(0, 6) # 1, 2, 4, 8, 16, 32, 64
            self.power.quest_value = typ

def Demon_hunter_training(self, event):
    self.power.quest_value += 1
    if self.power.quest_value > 4:
        self.power = power.Power(6, self)

def Prestidigitation(self, event):
    self.discover_secret(nb=3)

def Verdant_spheres(self, event, card):
    self.power.quest_value += 1
    if not self.power.quest_value % 3:
        card.create_and_apply_enchantment("302")

def Saturday_cthuns(self, event):
    if event == constants.EVENT_USE_POWER:
        self.power.quest_value += 1
    elif event == constants.EVENT_END_TURN and self.board and self.power.is_disabled:
        for _ in range(self.power.quest_value):
            minion = random.choice(self.board)
            minion.create_and_apply_enchantment("304")

def Sharpen_blades(self, event, card=None):
    if event == constants.EVENT_USE_POWER:
        if self.minion_buy_this_turn:
            minion = self.minion_choice(self.board)
            if minion:
                bonus = len(self.minion_buy_this_turn)
                minion.create_and_apply_enchantment("310", a=bonus, h=bonus)
                return minion
        return False
    return None

def Ill_take_that(self, event, attacker=None, victim=None):
    if event == constants.EVENT_KILLER_ALLY and self.power.quest_value:
        self.power.quest_value = 0
        key = victim.key_number
        if key in self.bob.card_can_collect:
            for card in self.bob.card_can_collect:
                if card.key_number == key:
                    self.hand.append(card)
                    return card
        card = self.hand.create_card(key)
        return card
    elif event == constants.EVENT_USE_POWER:
        if not self.power.quest_value:
            self.power.quest_value = 1
    elif event == constants.EVENT_BEGIN_TURN:
        self.power.quest_value = 0

def Sprout_it_out(self, event, repop_id):
    if self.opponent and type(self.opponent) is player.Player:
        repop_id.minion.create_and_apply_enchantment("310")
        repop_id.state_fight |= constants.STATE_TAUNT

def Dream_portal(self, event):
    dragon_lst = self.bob.hand.cards_type_of_tier_max(typ=constants.TYPE_DRAGON, tier_max=self.level)
    if dragon_lst:
        random.choice(dragon_lst).play(board=self.board.opponent)

def Battle_brand(self, event):
    self.board.opponent.drain_all_minion()
    self.board.opponent.fill_minion_battlecry()

def Temporal_tavern(self, event):
    self.board.opponent.drain_all_minion()
    self.board.opponent.fill_minion_temporal()

def Bananarama(self, event):
    if event == constants.EVENT_USE_POWER:
        for _ in range(2):
            if random.randint(1, 3) == 1:
                self.hand.create_card("1008")
            else:
                self.hand.create_card("1007")
    elif event == constants.EVENT_END_TURN and self.power.is_disabled:
        for player in self.bob.boards:
            if player != self:
                player.hand.create_card("1007")

def Hat_trick(self, event, card=None):
    brd = self.board.opponent
    if brd:
        for _ in range(2):
            minion = random.choice(brd)
            minion.create_and_apply_enchantment("312")

def All_will_burn(self, event):
    self.board.add_aura(self, method='Aile_de_mort')
    if self.board.opponent:
        self.board.opponent.add_aura(self, method='Aile_de_mort')

def Swatting_insects(self, event):
    if self.board:
        self.board[0].state_fight |= constants.STATE_ALAKIR

def Wingmen(self, event):
    if self.board:
        self.board[0].state_fight |= constants.STATE_ATTACK_IMMEDIATLY
        self.board[-1].state_fight |= constants.STATE_ATTACK_IMMEDIATLY

def active_nomi_bonus(self, event, target):
    pass
    #if target.type & constants.TYPE_ELEMENTAL:
    #    target.set_effect_on("14", self.bonus_nomi)
