from typing import List

VERSION = '20.4.2'
BATTLE_SIZE = 7
NB_PLAYER = 8
HAND_SIZE = 10
SECRET_SIZE = 5
NB_PRESENT_TYPE = 5
MAX_TURN = 44

MAX_GOLD = 10
LEVEL_MAX = 6
BOB_MINION_COST = 1
DEFAULT_MINION_COST = 3

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
LEVEL_UP_COST = [0, 6, 7, 8, 9, 10, 10]
GOLD_BY_TURN = [0, 3, 4, 5, 6, 7, 8, 9, 10]
NB_CARD_BY_LEVEL = [0, 3, 4, 4, 5, 5, 6]
NB_CARD_BY_LEVEL_ARANNA = BATTLE_SIZE

class Type(int):
    NONE = 0x0
    BEAST = 0x1
    DEMON = 0x2
    DRAGON = 0x4
    ELEMENTAL = 0x8
    MECH = 0x10
    MURLOC = 0x20
    PIRATE = 0x40
    QUILBOAR = 0x80
    ALL = 0xFF

    DEFAULT = NONE

    @classmethod
    def battleground_type(cls) -> List[int]:
        return [
            cls.BEAST, cls.DEMON, cls.DRAGON, cls.ELEMENTAL,
            cls.MECH, cls.MURLOC, cls.PIRATE, cls.QUILBOAR,
            ]

    @property
    def name(self) -> str:
        return TYPE_NAME.get(self, 'Inconnu')

    #def __getattribute__(self, name: str):
    #    if name.isupper():
    #        return self & getattr(Type, name)
    #    return getattr(self, name)

TYPE_NAME = {
    Type.NONE: "Neutre",
    Type.BEAST: "Bête",
    Type.DEMON: "Démon",
    Type.DRAGON: "Dragon",
    Type.ELEMENTAL: "Elémentaire",
    Type.MECH: "Méca",
    Type.MURLOC: "Murloc",
    Type.PIRATE: "Pirate",
    Type.QUILBOAR: "Huran",
    Type.ALL: "Tout"}

class State(int):
    NONE = 0x0
    TAUNT = 0x1
    DIVINE_SHIELD = 0x2
    REBORN = 0x4
    POISONOUS = 0x8
    WINDFURY = 0x10
    MEGA_WINDFURY = 0x20 # inexistant dans enums.py
    MODULAR = 0x40
    FREEZE = 0x80 # il n'existe pas de durée variable pour le gel
    ATTACK_IMMEDIATLY = 0x100
    CLEAVE = 0x200
    ATTACK_WEAK = 0x400
    DORMANT = 0x800
    STEALTH = 0x1000
    IS_POISONED = 0x2000
    FRENZY = 0x4000 # Frénésie
    IMMUNE = 0x8000
    SECRET = 0x10000
    ALL = 0xFFFFF

            # vol de vie, silence, ne peut pas attaquer
    ALAKIR = TAUNT | DIVINE_SHIELD | WINDFURY
    STILL_BOB = FREEZE | DORMANT
    NOT_TARGETABLE = DORMANT
    DEFAULT = NONE

STATE_NAME = {
    State.NONE: 'Aucun',
    State.TAUNT: 'Provocation',
    State.DIVINE_SHIELD: 'Bouclier divin',
    State.REBORN: 'Réincarnation',
    State.POISONOUS: 'Toxicité',
    State.WINDFURY: 'Furie des vents',
    State.MEGA_WINDFURY: 'Méga Furie des vents',
    State.MODULAR: 'Magnétisme',
    State.FREEZE: 'Gelé',
    State.ATTACK_IMMEDIATLY: 'Attaque immédiatement',
    State.CLEAVE: 'Cleave',
    State.ATTACK_WEAK: 'Attaque le plus faible', 
    State.DORMANT: 'Endormi',
    State.STEALTH: 'Furtivité',
    State.IS_POISONED: 'Empoisonné',
    State.FRENZY: 'Frénésie',
    State.IMMUNE: 'Insensible',
    State.SECRET: 'Secret',
    }

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

    KILLER_ALLY = 0x10000 # unused

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
        BEGIN_TURN: 'begin_turn',
        INVOC: 'invoc',
        END_TURN: 'end_turn',
        FIRST_STRIKE: 'first_strike',
        SELL: 'sell',
        BUY: 'buy',
        LEVELUP: 'levelup',
        ROLL: 'roll',
        PLAY: 'play',
        CREATION: 'creation',
        INVOC: 'invoc',
        BATTLECRY: 'battlecry',
        DEATHRATTLE: 'deathrattle',
        OVERKILL: 'overkill',
        DIE: 'die',
        ATK_ALLY: 'atk_ally',
        DEFEND_ALLY: 'defend_ally',
        KILLER_ALLY: 'killer_ally', # unused
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

class General(int):
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

