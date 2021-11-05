from os import X_OK
from typing import List

VERSION = '21.4'
FIELD_SIZE = 7
NB_PLAYER = 8
HAND_SIZE = 10
SECRET_SIZE = 5
NB_PRESENT_TYPE = 5
MAX_TURN = 44

MAX_GOLD = 10
LEVEL_MAX = 6
BOB_MINION_COST = 1
DEFAULT_MINION_COST = 3

class CardName:
    COIN = 58596
    BLOOD_GEM = 70136
    BLOOD_GEM_ENCHANTMENT = 72191
    KHADGAR = 52502
    KHADGAR_P = 58380
    BOB = 57110
    ICE_BLOCK = 58512

    DEFAULT_HERO = -10
    DEFAULT_GAME = -12
    DEFAULT_HAND = -13
    DEFAULT_BOARD = -14
    DEFAULT_BOB_BOARD = -15
    DEFAULT_PLAYER = -16
    DEFAULT_SECRET_BOARD = -17
    DEFAULT_GRAVEYARD = -18

    LAPIN = 60122
    LAPIN_P = 59664


class Rarity:
    INVALID = 0
    COMMON = 1
    FREE = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5
    DIAMOND = 6

    DEFAULT = FREE

CARD_NB_COPY = [0, 16, 15, 13, 11, 9, 7]
LEVELUP_COST = [0, 6, 7, 8, 9, 10, 10]
GOLD_BY_TURN = [0, 3, 4, 5, 6, 7, 8, 9, 10]
NB_CARD_BY_LEVEL = [0, 3, 4, 4, 5, 5, 6]
NB_CARD_BY_LEVEL_ARANNA = FIELD_SIZE

class Race(str):
    data = {
        "NONE": [0x0, 'Neutre'],
        "BEAST": [0x1, 'Bête'],
        "DEMON": [0x2, 'Démon'],
        "DRAGON": [0x4, 'Dragon'],
        "ELEMENTAL": [0x8, 'Élémentaire'],
        "MECHANICAL": [0x10, 'Méca'],
        "MURLOC": [0x20, 'Murloc'],
        "PIRATE": [0x40, 'Pirate'],
        "QUILBOAR": [0x80, 'Huran'],
        "ALL": [0xFF, 'Tout']}
    data['DEFAULT'] = data['NONE']

    @classmethod
    def battleground_race(cls) -> List[int]:
        return [
            0x1, 0x2, 0x4, 0x8,
            0x10, 0x20, 0x40, 0x80,
            ]

    @property
    def hex(self) -> int:
        return self.__class__.data[self][0]

    @property
    def name(self) -> str:
        return self.__class__.data[self][1]

    def __getattr__(self, race) -> int:
        if race.isupper():
            return self == race or self == 'ALL'
        raise AttributeError

    def __and__(self, value) -> int:
        if isinstance(value, int):
            return self.hex & value
        return self.hex & self.__class__.data[value][0]

    def __sub__(self, value) -> int:
        return self.hex - (self.hex & value)

state_list= [
    'BATTLECRY',
    'ENCHANTMENT_INVISIBLE',
    'TRIGGER_VISUAL',
    'CHARGE',
    'MODULAR',
    'WINDFURY',
    'AURA',
    'DEATHRATTLE',
    'REBORN',
    'DIVINE_SHIELD',
    'FRENZY',
    'FREEZE',
    'DISCOVER',
    'POISONOUS',
    'OVERKILL',
    'SECRET',
    'TAUNT',
    'IMMUNE',
    'AVENGE',

    'IS_POISONED',
    'MEGA_WINDFURY',
    'ATTACK_IMMEDIATLY',
    'CLEAVE',
    'DORMANT',
]

# obsolete
class Event(int):
    NONE = 0x0
    BEGIN_TURN = 0x1 # début de tour chez bob
    END_TURN = 0x2 # temps écoulé chez bob
    FIRST_STRIKE = 0x4 # début du combat
    SELL = 0x8 # le joueur vend une carte
    BUY = 0x10 # le joueur achète une carte
    LEVELUP = 0x20 # le joueur levelup
    ROLL = 0x40 # roll manuel
    PLAY = 0x80 # une carte est jouée
    CREATION = 0x100 # début de partie

    INVOC = 0x200 # invocation alliée (chef de meute, mande-flots murloc...)
    BATTLECRY = 0x400 # cri de guerre
    DEATHRATTLE = 0x800 # râle d'agonie
    OVERKILL = 0x1000 # brutalité

    DIE = 0x2000 # un allié meure (charognard, poisson)
    ATK_ALLY = 0x4000 # un allié attaque
    DEFEND_ALLY = 0x8000 # un allié est attaqué

    AFTER_PLAY = 0x10000

    BOB_PLAY = 0x20000 # Millificent, Nomi ?
    ADD_ENCHANTMENT_ON = 0x40000 # Aggem, tremble-terre...
    HIT_BY = 0x80000 # Chef du gang des diablotins, Rover de sécurité, Maman des diablotins
    WAKE_UP = 0x100000 # Maeiv
    AFTER_ATK_MYSELF = 0x200000 # Ara monstrueux, Cogneur

    PLAY_AURA = 0x400000 # Capitaine des mers du sud, Mal Ganis
    LOSS_HP = 0x800000 # Guetteur flottant, plus utilisé
    LOSS_SHIELD = 0x1000000 # Massacreur drakonide, Bolvar

    USE_POWER = 0x2000000
    AFTER_ATK_BY = 0x4000000 # Yo-oh
    DIE_PLAYER = 0x8000000 # Bloc de glace, Biggleworth

    KILL_MYSELF = 0x10000000 # Nat Pagle, unused (EVENT_KILLER_ALLY)

    END_FIGHT = 0x20000000

    ALL = 0xFFFFFFFF
    DEFAULT = NONE

    method_str = {
        BEGIN_TURN: 'turn_on',
        END_TURN: 'end_turn',
        FIRST_STRIKE: 'first_strike',
        SELL: 'sell',
        BUY: 'buy',
        LEVELUP: 'levelup',
        ROLL: 'roll',
        PLAY: 'play',
        CREATION: 'creation',
        INVOC: 'summon',
        BATTLECRY: 'battlecry',
        DEATHRATTLE: 'deathrattle',
        OVERKILL: 'overkill',
        DIE: 'kill',
        ATK_ALLY: 'atk_ally',
        DEFEND_ALLY: 'defend_ally',
        AFTER_PLAY: 'after_play',
        BOB_PLAY: 'bob_play',
        ADD_ENCHANTMENT_ON: 'add_enchantment_on',
        HIT_BY: 'hit_by',
        WAKE_UP:'wake_up',
        AFTER_ATK_MYSELF: 'after_atk_myself',
        PLAY_AURA: 'play_aura',
        LOSS_HP: 'loss_hp',
        LOSS_SHIELD: 'loss_shield',
        USE_POWER: 'use_power',
        AFTER_ATK_BY: 'after_atk_by',
        DIE_PLAYER: 'die_player',
        KILL_MYSELF: 'kill_myself',
        END_FIGHT: 'end_fight',
    }

    @property
    def method(self):
        return self.method_str[self]

class Type(int):
    NONE = 0
    GAME = 1
    PLAYER = 2
    BOB = 3
    HERO = 4
    HERO_POWER = 5
    ZONE = 6

    MINION = 7
    SPELL = 8
    ENCHANTMENT = 9

    DEFAULT = NONE

    @property
    def can_be_add_in_hand(self):
        return self in (self.__class__.SPELL, self.__class__.MINION)

    @property
    def can_be_add_in_board(self):
        return self == self.__class__.MINION


class Zone(int):
    NONE = 0
    PLAY = 1
    DECK = 2
    HAND = 3
    GRAVEYARD = 4
    REMOVEDFROMGAME = 5
    SETASIDE = 6
    SECRET = 7
    DEFAULT = NONE

ADAPT_ENCHANTMENT = [41692, 41068, 41069, 41071, 41210, 41073, 41072, 41693]

AKAZAM_SECRETS = [58505, 58509, 58507, 58500, 58499, 58512, 58502, 70114]
