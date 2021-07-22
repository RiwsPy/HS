from action import attack
import random
from enums import BATTLE_SIZE, LEVEL_MAX, Race, State, Type, CardName

class TB_BaconShop_HP_049:
    # Baz'hial
    def use_power(self):
        self.owner.health -= 2
        self.owner.hand.create_card_in(CardName.COIN)
        return True

class TB_BaconShop_HP_044:
    # AFK
    def begin_turn(self):
        if self.game.nb_turn < 3:
            self.owner.gold = 0
        elif self.game.nb_turn == 3:
            crd = self.owner.hand.create_card_in("59604")
            crd.quest_value = 3
            crd = self.owner.hand.create_card_in("59604")
            crd.quest_value = 3

class TB_BaconShop_HP_033:
    # Le Conservateur
    def begin_turn(self):
        if self.game.nb_turn == 1:
            self.owner.board.create_card_in("59202")

class TB_BaconShop_HP_105:
    # N'Zoth
    def begin_turn(self):
        if self.game.nb_turn == 1:
            self.owner.board.create_card_in("67213")

class TB_BaconShop_HP_074:
    # Capitaine Eudora
    #TODO : les cartes sont-elles issues/retirées de la main de bob ?
    #TODO : la probabilité d'obtention d'une carte dépend de sa présence dans la main ou sont équiprobables ?
    def use_power(self):
        self.quest_value += 1
        if self.quest_value % 5 == 0:
            card = random.choice(self.owner.bob.local_hand)
            g_card = self.create_card(card.battlegroundsPremiumDbfId)
            g_card.append(card)
            for entity in self.game.hand.cards_of_tier_max(card.level, card.level):
                if entity.dbfId == card.dbfId:
                    g_card.append(entity)
                    if len(g_card.entities) >= 3:
                        break
            self.owner.hand.append(g_card)
        return True

class TB_BaconShop_HP_054:
    # Millhouse
    # + utilisation de l'enchantment 60406
    def begin_turn(self):
        if self.game.nb_turn == 1:
            for index, _ in enumerate(self.owner.bob.level_up_cost_list):
                self.owner.bob.level_up_cost_list[index] += 1

class TB_BaconShop_HP_076:
    # Capitaine céleste Kragg
    def use_power(self):
        self.owner.gold += self.game.nb_turn
        return True

class TB_BaconShop_HP_010:
    # Georges
    def use_power(self):
        minion = self.choose_one_of_them(self.owner.board.cards)
        if minion:
            self.buff(self.enchantment_id, minion)

class TB_BaconShop_HP_072:
    # Neunoeil
    def buy(self, card):
        if card.race & Race.PIRATE:
            self.dec_power_cost()

    def use_power(self):
        self.cost = self.dbfId.cost
        self.owner.discover(self, nb=1, typ=Race.PIRATE, lvl_max=self.level)
        return True

class TB_BaconShop_HP_064:
    # Alexstrasa
    def levelup(self):
        if self.owner.level == 5:
            self.owner.discover(self, nb=3, typ=Race.DRAGON, lvl_max=6)
            self.owner.discover(self, nb=3, typ=Race.DRAGON, lvl_max=6)

class TB_BaconShop_HP_082:
    # Omu
    def levelup(self):
        self.owner.gold += 2

class TB_BaconShop_HP_063:
    # Nozdormu
    def begin_turn(self):
        if self.owner.bob.nb_free_roll < 1:
            self.owner.bob.nb_free_roll = 1

class TB_BaconShop_HP_040:
    # Pyraride
    def use_power(self):
        if self.owner.board.cards:
            self.buff(self.enchantment_id, random.choice(self.owner.board.cards))
            return True
        return False

class TB_BaconShop_HP_085:
    # Rakanishu
    def use_power(self):
        minion = self.choose_one_of_them(self.owner.board.cards)
        if minion:
            self.buff(self.enchantment_id, minion, attack=self.owner.level, health=self.owner.level)
            return True
        return False

class TB_BaconShop_HP_036:
    # Jaraxxus
    def use_power(self):
        for minion in self.owner.board.cards:
            if minion.race & Race.DEMON:
                self.buff(self.enchantment_id, minion)
        return True

class TB_BaconShop_HP_047:
    # Elise
    def levelup(self):
        crd = self.hand.create_card_in("60265")
        crd.quest_value = self.owner.level

class TB_BaconShop_HP_088:
    # Chenva'laa
    def play(self, card):
        if card.race & Race.ELEMENTAL:
            self.quest_value += 1
            if self.quest_value % 3 == 0:
                self.owner.bob.level_up_cost -= 3

class TB_BaconShop_HP_014:
    # Sindragosa
    def end_turn(self):
        for minion in self.owner.bob.board.cards:
            if minion.state & State.FREEZE:
                self.buff(self.enchantment_id, minion)

class TB_BaconShop_HP_015:
    # Millificent
    def play_aura(self):
        self.controller.bob.aura_active[self] = TB_BaconShop_HP_015.aura

    def aura(self, target):
        if target.type == Type.MINION and \
                target in target.controller.board.cards and \
                target.race & Race.MECH:
            self.buff(self.enchantment_id, target)

    def begin_turn(self):
        if self.game.nb_turn == 1:
            TB_BaconShop_HP_015.play_aura(self)

class TB_BaconShop_HP_087:
    # Ragnaros
    def die(self, source, killer):
        self.quest_value += 1
        if self.quest_value >= 25:
            self = self.create_card("64426")

class TB_BaconShop_HP_087t:
    # Ragnaros II
    def end_turn(self):
        # le bonus s'active-t-il deux fois si le board ne contient qu'un seul serviteur ?
        if self.owner.board.cards:
            self.buff(self.enchantment_id, self.owner.board[0])
            self.buff(self.enchantment_id, self.owner.board[-1])

class TB_BaconShop_HP_039:
    # Yogg
    def use_power(self):
        op = self.owner.bob.board.cards
        if op:
            random_card = random.choice(op)
            self.owner.hand.append(random_card)
            self.buff(self.enchantment_id, random_card)
            return True
        return False

class TB_BaconShop_HP_041:
    # 1 pouvoir pour chaque type: 59839, 59853, 59852, 59854, 62277, 64220, 71081, 60922

    # Le roi des Rats
    # will not change into the same Hero Power twice in a row
    def buy(self, card):
        if card.type & self.quest_value:
            self.buff(self.enchantment_id, card)

    def begin_turn(self):
        possible_types = self.game.type_present & (Race.ALL - self.quest_value)
        random_type = list(range(0, 8))
        random.shuffle(random_type)
        for typ in random_type:
            if 2**typ & possible_types:
                self.quest_value = 2**typ
                break

class TB_BaconShop_HP_065:
    # Aranna
    def roll(self):
        self.quest_value += 1
        if self.quest_value >= 5:
            self = self.create_card("62035")

class TB_BaconShop_HP_020:
    # Akazamzarak
    use_power = lambda x: x.discover_secret(nb=3)

class TB_BaconShop_HP_066:
    # Kael Thas
    def buy(self, card):
        self.quest_value += 1
        if not self.quest_value % 3:
            self.buff(self.enchantment_id, card)

class TB_BaconShop_HP_104:
    # C'Thun
    def use_power(self):
        self.quest_value += 1
        return True

    def end_turn(self):
        minions = self.owner.board.cards
        if minions and not self.is_enabled:
            for _ in range(self.quest_value):
                self.buff(self.enchantment_id, random.choice(minions))

class TB_BaconShop_HP_001:
    # Edwin
    def use_power(self):
        nb_minion = len(self.owner.bought_minions[self.owner.nb_turn])
        if nb_minion >= 1:
            minion = self.choose_one_of_them(self.owner.board.cards,
                pr=f"Hero power : choisissez une cible :")
            if minion:
                self.buff(self.enchantment_id, minion, attack=nb_minion, health=nb_minion)
                return True
        return False

class TB_BaconShop_HP_053:
    # Rafaam
    def use_power(self):
        self.temp_counter = 1
        return True

    def die(self, source, killer):
        if self.temp_counter == 1 and source.owner is not self.owner.board:
            self.temp_counter = 0
            self.owner.hand.append(
                self.game.hand.search(source.dbfId) or
                self.create_card(source.dbfId)
            )

class TB_BaconShop_HP_107:
    # Grisebranche
    def invoc(self, source):
        if self.owner.fight:
            self.buff(self.enchantment_id, source)

class TB_BaconShop_HP_062:
    # Ysera
    def begin_turn(self):
        dragon_lst = self.owner.bob.local_hand.filter_hex(race=Race.DRAGON)
        if dragon_lst:
            random.choice(dragon_lst).play(board=self.owner.bob.board)

class TB_BaconShop_HP_048:
    # Brann
    def use_power(self):
        self.owner.bob.board.drain_all_minion()
        self.owner.bob.board.fill_minion_battlecry()
        return True

class TB_BaconShop_HP_028:
    # Toki
    def use_power(self):
        self.owner.bob.board.drain_all_minion()
        self.owner.bob.board.fill_minion_temporal()
        return True

class TB_BaconShop_HP_038:
    # Mukla
    def use_power(self):
        for _ in range(2):
            if random.randint(1, 2) == 1:
                self.owner.hand.create_card_in("65230")
            else:
                self.owner.hand.create_card_in("53215")
        return True

    def end_turn(self):
        if not self.is_enabled:
            for entity in self.game.entities.filter(type=Type.HERO).exclude(self):
                entity.hand.create_card_in("53215")

class TB_BaconShop_HP_042:
    # Daryl
    def sell(self, card):
        brd = self.owner.opponent.board.cards
        if brd:
            for _ in range(2):
                self.buff(self.enchantment_id, random.choice(brd))

class TB_BaconShop_HP_061:
    # Aile de mort
    def play_aura(self):
        self.aura_target = [self.controller, self.controller.opponent]
        for entity in self.aura_target:
            if self not in entity.aura_active:
                entity.aura_active[self] = TB_BaconShop_HP_061.aura
                self.apply_met_on_all_children(TB_BaconShop_HP_061.aura, entity)

    def aura(self, target):
        if target.type == Type.MINION and \
                target in target.controller.board.cards:
            self.buff(self.enchantment_id, target, aura=True)

    def end_fight(self):
        self.aura_target = [self.controller, self.controller.opponent]
        for entity in self.aura_target:
            del entity.aura_active[self]

    def end_turn(self):
        del self.controller.opponent.aura_active[self]

    def first_strike(self):
        TB_BaconShop_HP_061.play_aura(self)
    begin_turn = first_strike

class TB_BaconShop_HP_086:
    # Al'Akir
    def first_strike(self):
        if self.owner.board.cards:
            self.buff(self.enchantment_id, self.owner.board.cards[0])

class TB_BaconShop_HP_069:
    # Illidan
    #TODO: non fonctionnel
    def first_strike(self):
        if self.board.cards:
            self.buff('63161', self.owner.board.cards[0])
            if len(self.board.cards) >= 2:
                self.buff('63161', self.owner.board.cards[-1])

class TB_BaconShop_HP_068:
    # Maiev
    #TODO: non fonctionnel
    def use_power(self):
        minion = self.choose_one_of_them(self.owner.board.opponent)
        if minion:
            self.buff(self.enchantment_id, minion)
            #minion.add_script({str(Event.WAKE_UP): 'wake_up'})
            return True
        return False

class TB_BaconShop_HP_024:
    # Roi-liche
    def use_power(self):
        minion = self.choose_one_of_them(self.owner.board)
        if minion:
            self.buff(self.enchantment_id, minion)
            return True
        return False

class BG20_HERO_103p:
    # Nécrorateur
    levelup = lambda self: self.owner.hand.create_card_in("70136", "70136")

class BG20_HERO_102p:
    # Saurcroc
    def use_power(self):
        self.temp_counter = 1
        return True

    def buy(self, card):
        if self.temp_counter == 1:
            self.temp_counter = 0
            self.buff(self.enchantment_id, card, attack=self.game.nb_turn+1)

class TB_BaconShop_HP_037a:
    # Cirène
    def use_power(self):
        for minion in self.owner.board.one_minion_by_type():
            self.buff(self.enchantment_id, minion)

class BG20_HERO_201p: # + BG20_HERO_201p2
    # Vol'jin
    def use_power(self):
        if self.temp_counter == 0:
            minion = self.choose_one_of_them(self.owner.board.cards + self.owner.board.opponent.cards)
            if minion:
                self.temp_counter = minion
        else:
            first_minion = self.temp_counter
            second_minion = self.choose_one_of_them(
                        self.owner.board.cards.exclude(first_minion) + \
                        self.owner.board.cards.opponent)
            if second_minion:
                self.buff(self.enchantment_id, second_minion, attack=first_minion.attack, health=first_minion.health)
                self.buff(self.enchantment_id, first_minion, attack=second_minion.attack, health=second_minion.health)
                self.temp_counter = 0
                return True
        return False

class BG20_HERO_101p:
    # Xyrella
    def use_power(self):
        minion = self.choose_one_of_them(self.owner.board.opponent)
        if minion:
            self.buff(self.enchantment_id, minion)
            self.owner.hand.append(minion)
            return True
        return False

class TB_BaconShop_HP_106:
    # Tickatus
    pass

class TB_BaconShop_HP_057:
    # Sir Finley
    pass

class TB_BaconShop_HP_075:
    # Double-crochet
    # découverte par le pouvoir, une carte peut se redécouvrir
    pass

class TB_BaconShop_HP_035:
    # Le Recousu
    pass

class TB_BaconShop_HP_103:
    # Y'Sharrj
    def use_power(self):
        self.temp_counter = 1
        return True

    def first_strike(self):
        if self.temp_counter:
            card_lst = self.game.hand.cards_of_tier_max(
                    tier_max=self.owner.level,
                    tier_min=self.owner.level)
            crd = random.choice(card_lst)
            self.owner.board.create_card_in(crd.entity_id)
            self.owner.hand.append(crd)

class TB_BaconShop_HP_065t2:
    # Aranna II
    #TODO, non fonctionnel > activation ?
    def play_aura(self):
        self.owner.bob.level_up_cost_list = [BATTLE_SIZE]*(LEVEL_MAX+1)
        self.owner.bob.board.fill_minion()

class TB_BaconShop_HP_022:
    # Carniflore
    pass

class TB_BaconShop_HP_056:
    # Fongimancien
    pass

class TB_BaconShop_HP_084:
    # Jandice
    pass

class TB_BaconShop_HP_080:
    # Chaton
    pass

class TB_BaconShop_HP_052:
    # Malygos
    pass

class TB_BaconShop_HP_046:
    # Reno Jackson
    pass

class TB_BaconShop_HP_081:
    # Seigneur Barov
    pass

class TB_BaconShop_HP_101:
    # Silas
    pass

class TB_BaconShop_HP_077:
    # Tess
    pass

class TB_BaconShop_HP_102:
    # Zephris
    pass

class BG20_HERO_280p:
    # Kurtrus I
    pass

class BG20_HERO_280p2:
    # Kurtrus II
    pass

class BG20_HERO_280p2e2:
    # Kurtrus III
    pass

class BG20_HERO_242p:
    # Guff Totem-Runique
    pass

class BG20_HERO_301p:
    # Mutanus le Dévoreur
    pass

