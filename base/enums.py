from typing import List

VERSION = '21.8'
BOARD_SIZE = 7
NB_PLAYER = 8
HAND_SIZE = 10
SECRET_SIZE = 5
NB_PRESENT_TYPE = 5
MAX_TURN = 44

MAX_GOLD = 10
LEVEL_MAX = 6
BOB_MINION_COST = 1
DEFAULT_MINION_COST = 3

dbfId_attr = {
    'enchantmentDbfId',
    'repopDbfId',
    'battlegroundsPremiumDbfId',
    'battlegroundsNormalDbfId',
    'powerDbfId',
}


class CardName:
    COIN = 58596
    BLOOD_GEM = 70136
    BLOOD_GEM_ENCHANTMENT = 72191
    KHADGAR = 52502
    KHADGAR_P = 58380
    BOB = 57110
    ICE_BLOCK = 58512
    TRIPLE_REWARD = 59604

    DEFAULT_HERO = 56298
    DEFAULT_GAME = -12
    DEFAULT_HAND = -13
    DEFAULT_BOARD = -14
    DEFAULT_BOB_BOARD = -15
    DEFAULT_PLAYER = -16
    DEFAULT_SECRET_BOARD = -17
    DEFAULT_GRAVEYARD = -18
    DEFAULT_FIELD = -19

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
NB_CARD_BY_LEVEL_ARANNA = BOARD_SIZE

class Race(str):
    data = {
        "NONE": 'Neutre',
        "BEAST": 'Bête',
        "DEMON": 'Démon',
        "DRAGON": 'Dragon',
        "ELEMENTAL": 'Élémentaire',
        "MECHANICAL": 'Méca',
        "MURLOC": 'Murloc',
        "PIRATE": 'Pirate',
        "QUILBOAR": 'Huran',
        "ALL": 'Tout'}
    data['DEFAULT'] = data['NONE']

    @classmethod
    def battleground_race_name(cls) -> List[str]:
        return list(cls.data.keys())[1:-2]

    @property
    def name(self) -> str:
        return self.__class__.data[self]

    def __getattr__(self, race) -> bool:
        if race.isupper():
            return self == race
        raise AttributeError

    def __eq__(self, value) -> bool:
        return str(self) == str(value) or str(self) == 'ALL'

    def __ne__(self, value) -> bool:
        return not self == value

    def __hash__(self) -> int:
        return super().__hash__()

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
    'CANT_BE_DESTROYED',

    'IS_POISONED',
    'MEGA_WINDFURY',
    'CLEAVE',
    'DORMANT',
]


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

    def __new__(cls, value):
        if isinstance(value, str):
            return super().__new__(cls, getattr(cls, value))
        return super().__new__(cls, value)

    @property
    def can_be_add_in_hand(self):
        return self in (self.__class__.SPELL, self.__class__.MINION)

    @property
    def can_be_add_in_board(self):
        return self == self.__class__.MINION

    def __getattr__(self, attr):
        if isinstance(attr, int):
            return attr
        raise AttributeError


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
