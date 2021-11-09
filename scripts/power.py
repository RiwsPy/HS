from entity import Hero_power
from action import attack
import random
from enums import FIELD_SIZE, LEVEL_MAX, Race, Type, CardName, AKAZAM_SECRETS
from utils import repeat_effect
from sequence import Sequence

class TB_BaconShop_HP_049(Hero_power):
    # Baz'hial
    def use_power(self, sequence: Sequence):
        self.owner.health -= 2
        self.owner.hand.create_card_in(CardName.COIN)


class TB_BaconShop_HP_044(Hero_power):
    # AFK
    def turn_on(self, sequence: Sequence):
        if self.nb_turn < 3:
            self.owner.gold = 0
        elif self.nb_turn == 3:
            self.owner.hand.create_card_in(59604, quest_value=3)
            self.owner.hand.create_card_in(59604, quest_value=3)


class TB_BaconShop_HP_033(Hero_power):
    # Le Conservateur
    def turn_on(self, sequence: Sequence):
        if self.nb_turn == 1:
            self.board.create_card_in(59202)


class TB_BaconShop_HP_105(Hero_power):
    # N'Zoth
    def turn_on(self, sequence: Sequence):
        if self.nb_turn == 1:
            self.board.create_card_in(67213)


class TB_BaconShop_HP_074(Hero_power):
    # Capitaine Eudora
    #TODO : les cartes sont-elles issues/retirées de la main de bob ?
    #TODO : la probabilité d'obtention d'une carte dépend de sa présence dans la main ou sont équiprobables ?
    def use_power(self, sequence: Sequence):
        self.quest_value += 1
        if self.quest_value % 5 == 0:
            card = self.owner.bob.local_hand.choice()
            g_card = self.create_card(card.battlegroundsPremiumDbfId)
            g_card.append(card)
            card_remain = 2
            for entity in self.game.hand.cards_of_tier_max(card.level, card.level):
                if entity.dbfId == card.dbfId:
                    card_remain -= 1
                    g_card.append(entity)
                    if card_remain <= 0:
                        break
            self.owner.hand.append(g_card)
        return True


class TB_BaconShop_HP_054(Hero_power):
    # Millhouse
    # + utilisation de l'enchantment 60406
    pass


class TB_BaconShop_HP_076(Hero_power):
    # Capitaine céleste Kragg
    def use_power(self, sequence: Sequence):
        self.owner.gold += self.nb_turn


class TB_BaconShop_HP_010(Hero_power):
    # Georges
    def use_power_start(self, sequence: Sequence):
        minion = self.choose_one_of_them(self.board.cards)
        if minion:
            sequence.add_target(minion)
        else:
            sequence.is_valid = False

    def use_power(self, sequence: Sequence):
        self.buff(self.enchantment_dbfId, sequence.target)


class TB_BaconShop_HP_072(Hero_power):
    # Neunoeil
    def buy_on(self, sequence: Sequence):
        if sequence.source.race.PIRATE:
            self.dec_power_cost()

    def use_power(self, sequence: Sequence):
        self.cost = self.dbfId.cost
        self.owner.discover(self, nb=1, typ=Race.PIRATE, lvl_max=self.level)


class TB_BaconShop_HP_064(Hero_power):
    # Alexstrasa
    def levelup_off(self, sequence: Sequence):
        if self.owner.level == 5:
            self.owner.discover(self, nb=3, typ=Race.DRAGON, lvl_max=6)
            self.owner.discover(self, nb=3, typ=Race.DRAGON, lvl_max=6)


class TB_BaconShop_HP_082(Hero_power):
    # Omu
    def levelup_off(self, sequence: Sequence):
        self.owner.gold += 2


class TB_BaconShop_HP_063(Hero_power):
    # Nozdormu
    def roll_on(self, sequence: Sequence):
        if self.temp_counter == 0:
            sequence.cost = 0

    def roll_off(self, sequence: Sequence):
        self.temp_counter += 1


class TB_BaconShop_HP_040(Hero_power):
    # Pyraride
    def use_power_start(self, sequence: Sequence):
        sequence.is_valid = self.board.size > 0

    def use_power(self, sequence: Sequence):
        self.buff(
            self.enchantment_dbfId,
            self.board.cards.choice()
        )


class TB_BaconShop_HP_085(Hero_power):
    # Rakanishu
    def use_power_start(self, sequence: Sequence):
        minion = self.choose_one_of_them(self.board.cards)
        if minion:
            sequence.add_target(minion)
        else:
            self.is_valid = False

    def use_power(self, sequence: Sequence):
        self.buff(self.enchantment_dbfId,
            sequence.target,
            attack=self.bonus_value,
            max_health=self.bonus_value)

    @property
    def bonus_value(self) -> int:
        return self.owner.level


class TB_BaconShop_HP_036(Hero_power):
    # Jaraxxus
    def use_power(self, sequence: Sequence):
        for minion in self.board.cards.filter(race='DEMON'):
            self.buff(self.enchantment_dbfId, minion)


class TB_BaconShop_HP_047(Hero_power):
    # Elise
    def levelup_off(self, sequence: Sequence):
        self.hand.create_card_in(60265, quest_value=self.owner.level)


class TB_BaconShop_HP_088(Hero_power):
    # Chenva'laa
    def play_off(self, sequence: Sequence):
        if sequence.source.race.ELEMENTAL:
            self.quest_value += 1
            if self.quest_value % 3 == 0:
                self.owner.levelup_cost_mod -= 3


class TB_BaconShop_HP_014(Hero_power):
    # Sindragosa
    def turn_off(self, sequence: Sequence):
        for minion in self.owner.bob.board.cards:
            if minion.FREEZE:
                self.buff(self.enchantment_dbfId, minion)


class TB_BaconShop_HP_015(Hero_power):
    # Millificent
    def summon_on(self, sequence: Sequence):
        if not self.in_fight_sequence and\
                sequence.source.controller is self.controller.bob:
            if sequence.source.race.MECHANICAL:
                self.buff(self.enchantment_dbfId, sequence.source)


class TB_BaconShop_HP_087(Hero_power):
    # Ragnaros
    def die_off(self, sequence: Sequence):
        self.quest_value += 1
        if self.quest_value >= 25:
            self.change(64426)


class TB_BaconShop_HP_087t(Hero_power):
    # Ragnaros II
    def turn_off(self, sequence: Sequence):
        # le bonus s'active-t-il deux fois si le board ne contient qu'un seul serviteur ?
        if self.board.size > 0:
            self.buff(self.enchantment_dbfId, self.board[0])
            self.buff(self.enchantment_dbfId, self.board[-1])


class TB_BaconShop_HP_039(Hero_power):
    # Yogg
    def use_power(self):
        minion = self.controller.bob.board.cards.choice()
        if minion:
            self.controller.hand.append(minion)
            self.buff(self.enchantment_dbfId, minion)


class TB_BaconShop_HP_041(Hero_power):
    # TODO
    # 1 pouvoir pour chaque type: 59839, 59853, 59852, 59854, 62277, 64220, 71081, 60922

    # Le roi des Rats
    # will not change into the same Hero Power twice in a row
    def buy_off(self, card):
        if card.type & self.quest_value:
            self.buff(self.enchantment_dbfId, card)

    def turn_on(self, sequence: Sequence):
        possible_types = self.game.type_present & (0xFF - self.quest_value)
        random_type = list(range(0, 8))
        random.shuffle(random_type)
        for typ in random_type:
            if 2**typ & possible_types:
                self.quest_value = 2**typ
                break


class TB_BaconShop_HP_065(Hero_power):
    # Aranna
    def roll_on(self, sequence: Sequence):
        self.quest_value += 1
        if self.quest_value >= 5:
            self.change(62035)


class TB_BaconShop_HP_020(Hero_power):
    # Akazamzarak
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secrets_choice = AKAZAM_SECRETS[:]

    def use_power(self, sequence: Sequence):
        available_secret = self.secrets_choice[:]
        random.shuffle(available_secret)
        for entity in self.owner.secret_board.entities:
            if entity.SECRET and entity.dbfId in available_secret:
                available_secret.remove(entity.dbfId)

        choice = self.choose_one_of_them(available_secret[:3], "Découverte d'un secret")
        if choice:
            card_id = self.create_card(choice)
            # Only one Ice Block / game
            if choice == CardName.ICE_BLOCK:
                self.secrets_choice.remove(choice)
            self.owner.secret_board.append(card_id)


class TB_BaconShop_HP_066(Hero_power):
    # Kael Thas
    def buy_off(self, sequence: Sequence):
        self.quest_value += 1
        if self.quest_value % 3 == 0:
            self.buff(self.enchantment_dbfId, sequence.source)


class TB_BaconShop_HP_104(Hero_power):
    # C'Thun
    def use_power(self, sequence: Sequence):
        self.quest_value += 1
        self.temp_counter = True

    def turn_off(self, sequence: Sequence):
        if self.board.size > 0 and self.temp_counter is True:
            for _ in range(self.quest_value):
                self.buff(self.enchantment_dbfId,
                    random.choice(self.board.cards))


class TB_BaconShop_HP_001(Hero_power):
    # Edwin
    def use_power_start(self, sequence: Sequence):
        if self.bonus_value >= 1:
            minion = self.choose_one_of_them(
                self.board.cards,
                pr=f"Hero power : choisissez une cible :")
            sequence.add_target(minion)
        else:
            sequence.is_valid = False

    def use_power(self, sequence: Sequence):
        bonus_attack = self.enchantment_dbfId.attack*self.bonus_value
        bonus_health = self.enchantment_dbfId.max_health*self.bonus_value
        self.buff(self.enchantment_dbfId, sequence.target,
            attack=bonus_attack,
            max_health=bonus_health)

    @property
    def bonus_value(self) -> int:
        return len(self.owner.bought_minions[self.nb_turn])


class TB_BaconShop_HP_053(Hero_power):
    # Rafaam
    def use_power(self, sequence: Sequence):
        self.temp_counter = 1

    def die_off(self, sequence: Sequence):
        source = sequence.source
        if self.temp_counter == 1 and source.controller is self.owner.opponent:
            self.temp_counter = 0
            self.owner.hand.append(
                self.game.hand.search(source.dbfId) or
                self.create_card(source.dbfId)
            )


class TB_BaconShop_HP_107(Hero_power):
    # Grisebranche
    def summon_on(self, sequence: Sequence):
        if self.in_fight_sequence and self.owner is sequence.source.controller:
            self.buff(self.enchantment_dbfId, sequence.source)


class TB_BaconShop_HP_062(Hero_power):
    # Ysera
    def turn_on(self, sequence: Sequence):
        self.controller.bob.board.append(
            self.controller.bob.local_hand.filter(race='DRAGON').choice()
        )
    roll_off = turn_on


class TB_BaconShop_HP_048(Hero_power):
    # Brann
    def buy_on(self, sequence: Sequence):
        if self.is_enabled and sequence.source.BATTLECRY:
            self.quest_value += 1
            if self.quest_value % 5 == 0:
                self.owner.hand.create_card_in(2949)
                self.dec_remain_use()


class TB_BaconShop_HP_028(Hero_power):
    # Toki
    def use_power(self):
        self.owner.bob.board.drain_all_minion()
        self.owner.bob.board.fill_minion_temporal()


class TB_BaconShop_HP_038(Hero_power):
    # Mukla
    nb_strike = 2

    @repeat_effect
    def use_power(self, sequence: Sequence):
        self.owner.hand.create_card_in(random.choice([53215, 65230]))

    def turn_off(self, sequence: Sequence):
        if not self.is_enabled:
            for entity in self.game.entities.filter(type=Type.HERO).exclude(self):
                entity.hand.create_card_in(53215)


class TB_BaconShop_HP_042(Hero_power):
    # Daryl
    nb_strike = 3

    @repeat_effect
    def sell_off(self, sequence: Sequence):
        self.buff(
            self.enchantment_dbfId,
            self.controller.opponent.board.cards.choice())


class TB_BaconShop_HP_061(Hero_power):
    # Aile de mort
    def summon_on(self, sequence: Sequence):
        #TODO gestion début de TURN/FIGHT
        self.buff(self.enchantment_dbfId, sequence.source)

    def fight_on(self, sequence: Sequence):
        # bonus non cumulable ?
        for minion in self.board.cards:
            self.buff(self.enchantment_dbfId, minion)
        for minion in self.board.opponent.cards:
            self.buff(self.enchantment_dbfId, minion)
    turn_on= fight_on


class TB_BaconShop_HP_086(Hero_power):
    # Al'Akir
    def fight_on(self, sequence: Sequence):
        if self.board.cards:
            self.buff(self.enchantment_dbfId, self.board.cards[0])


class TB_BaconShop_HP_069(Hero_power):
    # Illidan
    #TODO: non fonctionnel
    def fight_on(self, sequence: Sequence):
        if self.board.cards:
            self.buff(self.enchantment_dbfId, self.board.cards[0])
            if self.board.size >= 2:
                self.buff(self.enchantment_dbfId, self.board.cards[-1])


class TB_BaconShop_HP_068(Hero_power):
    # Maiev
    #TODO: non fonctionnel
    # If a minion in Bob's Tavern is made Dormant due to Maiev Shadowsong's Imprison and her hand is full by the time the Dormant ends, the minion will die in Bob's Tavern and trigger its Deathrattle, causing every minion in the tavern to react.
    def user_power_start(self, sequence: Sequence):
        minion = self.choose_one_of_them(self.board.opponent)
        if minion:
            sequence.add_target(minion)
        else:
            sequence.is_valid = False

    def use_power(self, sequence: Sequence):
        self.buff(self.enchantment_dbfId, sequence.target)


class TB_BaconShop_HP_024(Hero_power):
    # Roi-liche
    def use_power_start(self, sequence: Sequence):
        minion = self.choose_one_of_them(self.board)
        if minion:
            self.quest_value = minion
        else:
            sequence.is_valid = False

    def fight_on(self, sequence: Sequence):
        if self.quest_value in self.board.cards:
            self.buff(self.enchantment_dbfId, self.quest_value)


class BG20_HERO_103p(Hero_power):
    # Nécrorateur
    nb_strike = 2

    @repeat_effect
    def levelup_off(self, sequence: Sequence):
        self.owner.hand.create_card_in(CardName.BLOOD_GEM)


class BG20_HERO_102p(Hero_power):
    # Saurcroc
    def use_power(self):
        self.temp_counter = 1

    def buy_off(self, sequence: Sequence):
        if self.temp_counter == 1:
            self.temp_counter = 0
            self.buff(self.enchantment_dbfId,
                sequence.source,
                attack=self.nb_turn+1)


class TB_BaconShop_HP_037a(Hero_power):
    # Cirène
    def use_power(self):
        for minion in self.board.cards.one_minion_by_race():
            self.buff(self.enchantment_dbfId, minion)


class BG20_HERO_201p(Hero_power):
    # Vol'jin 1
    # un dragon qui augmente son attaque grâce à ce pouvoir est buff par le contrebandier (pas l'autre)
    def use_power_start(self, sequence: Sequence):
        minion1 = self.choose_one_of_them(
            self.board.cards + self.board.opponent.cards)
        if minion1:
            self.buff(self.enchantment_dbfId, minion1)
            sequence.target = minion1
        else:
            sequence.is_valid = False

    def use_power(self, sequence: Sequence):
        self.change(71644, quest_value=sequence.target)


class BG20_HERO_201p2(BG20_HERO_201p):
    # Vol'jin 2
    # pouvoir utilisable sur la même cible ? > non
    # le pouvoir est reset à la fin du tour si celui-ci n'est pas utilisé
    # le pouvoir est reset si le minion1 est vendu
    # ou si plus généralement quitte le board ? > aura ? > que se passe-t-il si le minion est dévoré ?
    def use_power_start(self, sequence: Sequence):
        minions = (self.board.cards + self.board.opponent.cards).exclude(self.quest_value)
        minion2 = self.choose_one_of_them(minions)
        if minion2:
            self.temp_counter = minion2
        else:
            sequence.is_valid = False

    def use_power(self, sequence: Sequence):
        minion1 = self.quest_value
        minion2 = self.temp_counter

        if minion2 and minion1:
            self.buff(self.enchantment_dbfId, 
                minion2,
                attack=minion1.attack, 
                max_health=minion1.health)

            self.buff(self.enchantment_dbfId,
                minion1,
                attack=minion2.attack,
                max_health=minion2.health)

    def sell_off(self, sequence: Sequence):
        if sequence.source is self.quest_value:
            self.turn_off(sequence)

    def turn_off(self, sequence: Sequence):
        self.change(71464)


class BG20_HERO_101p(Hero_power):
    # Xyrella
    def use_power_start(self, sequence: Sequence):
        minion = self.choose_one_of_them(self.board.opponent.cards)
        if minion:
            self.temp_counter = minion
        else:
            sequence.is_valid = False

    def use_power(self, sequence: Sequence):
        self.owner.hand.append(self.temp_counter)
        self.buff(self.enchantment_dbfId, self.temp_counter)


class TB_BaconShop_HP_106(Hero_power):
    # Tickatus
    pass


class TB_BaconShop_HP_057(Hero_power):
    # Sir Finley
    pass


class TB_BaconShop_HP_075(Hero_power):
    # Double-crochet
    # découverte par le pouvoir, une carte peut se redécouvrir
    pass


class TB_BaconShop_HP_035(Hero_power):
    # Le Recousu
    pass


class TB_BaconShop_HP_103(Hero_power):
    # Y'Sharrj
    def use_power(self, sequence: Sequence):
        self.temp_counter = 1

    def fight_on(self, sequence: Sequence):
        # TODO: carte retirée de la main de Bob ?
        if self.temp_counter:
            card = self.game.hand.cards_of_tier_max(
                    tier_max=self.owner.level,
                    tier_min=self.owner.level).choice()
            minion = self.board.create_card_in(card.dbfId)
            if minion in self.board.cards:
                self.owner.hand.append(card)


class TB_BaconShop_HP_065t2(Hero_power):
    # Aranna II
    #TODO: set 7 au lieu de add 7, mais fonctionnel car cas particulier
    card_by_roll_mod = FIELD_SIZE


class TB_BaconShop_HP_022(Hero_power):
    # Carniflore
    pass

class TB_BaconShop_HP_056(Hero_power):
    # Fongimancien
    pass

class TB_BaconShop_HP_084(Hero_power):
    # Jandice
    pass

class TB_BaconShop_HP_080(Hero_power):
    # Chaton
    pass

class TB_BaconShop_HP_052(Hero_power):
    # Malygos
    pass

class TB_BaconShop_HP_046(Hero_power):
    # Reno Jackson
    pass

class TB_BaconShop_HP_081(Hero_power):
    # Seigneur Barov
    pass


class TB_BaconShop_HP_101(Hero_power):
    # Silas
    # Considéré que la probabilité d'apparition d'un ticket est de 1/3
    # Cette valeur fait suite à un retour d'expérience non à une valeur officielle
    def summon_on(self, sequence: Sequence):
        if sequence.source.controller is self.controller.bob and random.randint(0, 2) == 0:
            self.buff(self.enchantment_dbfId, sequence.source)

    def buy_off(self, sequence: Sequence):
        for entity in sequence.source.entities:
            if entity.dbfId == self.enchantment_dbfId:
                self.quest_value += 1
                entity.remove()
                break

        if self.quest_value % 3 == 0:
            self.owner.hand.create_card_in(64484, quest_value=self.owner.level)


class TB_BaconShop_HP_077(Hero_power):
    # Tess
    pass

class TB_BaconShop_HP_102(Hero_power):
    # Zephris
    pass

class BG20_HERO_280p(Hero_power):
    # Kurtrus I
    pass

class BG20_HERO_280p2(Hero_power):
    # Kurtrus II
    pass

class BG20_HERO_280p2e2(Hero_power):
    # Kurtrus III
    pass

class BG20_HERO_242p(Hero_power):
    # Guff Totem-Runique
    pass

class BG20_HERO_301p(Hero_power):
    # Mutanus le Dévoreur
    pass

class Inconnu(Hero_power):
    pass

class Taverne(Hero_power):
    pass
