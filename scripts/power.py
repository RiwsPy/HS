from entity import Hero_power
import random
from enums import BOARD_SIZE, Race, Type, CardName, AKAZAM_SECRETS, LEVEL_MAX
from utils import repeat_effect
from sequence import Sequence


class use_power_on_my_minion(Hero_power):
    def use_power_start(self, sequence: Sequence):
        minion = self.board.cards.choice(
            self.owner,
            pr=f"Hero power : choisissez une cible :")
        if minion:
            sequence.add_target(minion)
        else:
            sequence.is_valid = False


class TB_BaconShop_HP_049(Hero_power):
    # Baz'hial
    def use_power(self, sequence: Sequence):
        self.owner.health -= 2
        self.hand.create_card_in(CardName.COIN)


class TB_BaconShop_HP_044(Hero_power):
    # AFK
    def turn_on(self, sequence: Sequence):
        if self.nb_turn < 3:
            self.owner.gold = 0
        elif self.nb_turn == 3:
            self.hand.create_card_in(59604, quest_value=3)
            self.hand.create_card_in(59604, quest_value=3)


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
            card = self.owner.bob.local_hand.random_choice()
            g_card = self.create_card(card.battlegroundsPremiumDbfId)
            g_card.append(card)
            card_remain = 2
            for entity in self.game.hand.cards_of_tier_max(card.level, card.level):
                if entity.dbfId == card.dbfId:
                    card_remain -= 1
                    g_card.append(entity)
                    if card_remain <= 0:
                        break
            self.hand.append(g_card)
        return True


class TB_BaconShop_HP_054(Hero_power):
    # Millhouse
    # + utilisation de l'enchantment 60406
    pass


class TB_BaconShop_HP_076(Hero_power):
    # Capitaine céleste Kragg
    def use_power(self, sequence: Sequence):
        self.owner.gold += self.nb_turn


class TB_BaconShop_HP_010(use_power_on_my_minion):
    # Georges
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
            self.board.cards.random_choice()
        )


class TB_BaconShop_HP_085(use_power_on_my_minion):
    # Rakanishu
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
        minion = self.controller.bob.board.cards.random_choice()
        if minion:
            self.hand.append(minion)
            self.buff(self.enchantment_dbfId, minion)


class TB_BaconShop_HP_041(Hero_power):
    # Le roi des Rats

    race_to_power_dbfId = {
        Race('BEAST').hex: 59839,
        Race('MECHANICAL').hex: 59853,
        Race('MURLOC').hex: 59852,
        Race('DEMON').hex: 59854,
        Race('DRAGON').hex: 60922,
        Race('PIRATE').hex: 62277,
        Race('ELEMENTAL').hex: 64220,
        Race('QUILBOAR').hex: 71081,
    }
    def turn_on(self, sequence: Sequence):
        types = Race.battleground_race()
        random.shuffle(types)
        for typ in types:
            if typ & self.game.type_present and self.synergy.hex != typ:
                self.change(self.race_to_power_dbfId[typ])
                break

    def buy_off(self, sequence: Sequence):
        if sequence.source.type & self.synergy.hex and sequence.is_ally(self):
            self.buff(self.enchantment_dbfId, sequence.source)
TB_BaconShop_HP_041a= TB_BaconShop_HP_041
TB_BaconShop_HP_041b= TB_BaconShop_HP_041
TB_BaconShop_HP_041c= TB_BaconShop_HP_041
TB_BaconShop_HP_041d= TB_BaconShop_HP_041
TB_BaconShop_HP_041f= TB_BaconShop_HP_041
TB_BaconShop_HP_041g= TB_BaconShop_HP_041
TB_BaconShop_HP_041h= TB_BaconShop_HP_041
TB_BaconShop_HP_041i= TB_BaconShop_HP_041


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

        choice = available_secret[:3].choice(self.controller, "Découverte d'un secret")
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


class TB_BaconShop_HP_001(use_power_on_my_minion):
    # Edwin
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
        if self.temp_counter == 1 and not sequence.is_ally(self):
            self.temp_counter = 0
            self.hand.append(
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
            self.controller.bob.local_hand.filter(race='DRAGON').random_choice()
        )
    roll_off = turn_on


class TB_BaconShop_HP_048(Hero_power):
    # Brann
    def buy_on(self, sequence: Sequence):
        if self.is_enabled and sequence.source.BATTLECRY:
            self.quest_value += 1
            if self.quest_value % 5 == 0:
                self.hand.create_card_in(2949)
                self.dec_remain_use()


class TB_BaconShop_HP_028(Hero_power):
    # Toki
    # TODO: à simplifier
    def use_power(self):
        bob = self.owner.bob
        bob.board.drain_all_minion()
        self.board.fill_minion(
            nb_card_to_play = self.owner.nb_card_by_refresh - 1)

        lvl = min(LEVEL_MAX, self.owner.level+1)
        entity = bob.hand.cards_of_tier_max(tier_max=lvl, tier_min=lvl).random_choice()
        if entity:
            entity.owner = self.controller
            self.game.hand.remove(entity)
            entity.summon()

class TB_BaconShop_HP_038(Hero_power):
    # Mukla
    nb_strike = 2

    @repeat_effect
    def use_power(self, sequence: Sequence):
        self.hand.create_card_in(random.choice([53215, 65230]))

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
            self.controller.opponent.board.cards.random_choice())


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
    # TODO: If a minion in Bob's Tavern is made Dormant due to Maiev Shadowsong's Imprison and her hand is full by the time the Dormant ends, the minion will die in Bob's Tavern and trigger its Deathrattle, causing every minion in the tavern to react.
    def user_power_start(self, sequence: Sequence):
        minion = self.board.opponent.cards.choice(self.controller)
        if minion:
            sequence.add_target(minion)
        else:
            sequence.is_valid = False

    def use_power(self, sequence: Sequence):
        self.buff(self.enchantment_dbfId, sequence.target)


class TB_BaconShop_HP_024(use_power_on_my_minion):
    # Roi-liche
    def use_power_start(self, sequence: Sequence):
        minion = self.board.cards.exclude(REBORN=True).choice(
            self.owner,
            pr=f"Hero power : choisissez une cible :")
        if minion:
            sequence.add_target(minion)
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
        self.hand.create_card_in(CardName.BLOOD_GEM)


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
        minion1 = self.controller.field.cards.choice(self.controller)
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
        minion2 = self.controller.field.cards.exclude(self.quest_value).choice(self.controller)
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
        minion = self.board.opponent.cards.choice(self.controller)
        if minion:
            self.temp_counter = minion
        else:
            sequence.is_valid = False

    def use_power(self, sequence: Sequence):
        self.hand.append(self.temp_counter)
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
                    tier_min=self.owner.level).random_choice()
            minion = self.board.create_card_in(card.dbfId)
            if minion in self.board.cards:
                self.hand.append(card)


class TB_BaconShop_HP_065t2(Hero_power):
    # Aranna II
    #TODO: set 7 au lieu de add 7, mais fonctionnel car cas particulier
    card_by_roll_mod = BOARD_SIZE


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
    def use_power_start(self, sequence: Sequence):
        minion = self.owner.field.cards.choice(
            self.owner,
            pr=f"Hero power : choisissez une cible :")
        if minion:
            sequence.add_target(minion)
        else:
            sequence.is_valid = False

    def use_power(self, sequence):
        self.temp_counter += 1
        new_minion = self.game.hand.cards.filter_maxmin_level(
            level_max=sequence.target.level,
            level_min=sequence.target.level).\
                exclude(dbfId=sequence.target.dbfId).random_choice()
        sequence.target.replace(new_minion)
        if self.temp_counter >= 2:
            self.disable()
    

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
        if self.game.current_sequence == 'TURN' and\
                not sequence.is_ally(self) and\
                random.randint(0, 2) == 0:
            self.buff(self.enchantment_dbfId, sequence.source)

    @property
    def quest_value(self) -> int:
        return self._quest_value

    @quest_value.setter
    def quest_value(self, value) -> None:
        self._quest_value = value
        if self._quest_value % 3 == 0 and self._quest_value > 0:
            self.hand.create_card_in(64484, quest_value=self.owner.level)


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
