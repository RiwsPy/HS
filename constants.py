BATTLE_SIZE = 7
NB_PLAYER = 8
HAND_SIZE = 10
SECRET_SIZE = 5
MAX_GOLD = 10
LEVEL_MAX = 6
BOB_MINION_COST = 1

CARD_NB_COPY = [0, 16, 15, 13, 11, 9, 7]
LEVEL_UP_COST = [0, 6, 7, 8, 9, 10, 10]
LEVEL_UP_COST_MILLHOUSE = [0, 7, 8, 9, 10, 11, 11]
GOLD_BY_TURN = [0, 3, 4, 5, 6, 7, 8, 9, 10]
NB_CARD_BY_LEVEL = [0, 3, 4, 4, 5, 5, 6]
NB_CARD_BY_LEVEL_ARANNA = [0, 7, 7, 7, 7, 7, 7]

TYPE_NAME = {0x0: "Neutre", 0x1:"Bête", 0x2:"Démon", 0x4:"Dragon", 0x8:"Elémentaire",
    0x10:"Méca", 0x20:"Murloc", 0x40:"Pirate", 0x80:"Huran"}
TYPE_NONE = 0x0
TYPE_BEAST = 0x1
TYPE_DEMON = 0x2
TYPE_DRAGON = 0x4
TYPE_ELEMENTAL = 0x8
TYPE_MECH = 0x10
TYPE_MURLOC = 0x20
TYPE_PIRATE = 0x40
TYPE_QUILBOAR = 0x80
TYPE_ALL = 0xFF

STATE_NAME = {0: 'Aucun', 1: 'Provocation', 2: 'Bouclier divin', 4: 'Réincarnation',
    8: 'Toxicité', 0x10: 'Furie des vents', 0x20: 'Méga Furie des vents',
    0x40: 'Magnétisme', 0x80: 'Gelé', 0x100: 'Attaque immédiatement', 0x200: 'Cleave',
    0x400: 'Attaque le plus faible', 0x800: 'Endormi', 0x1000: 'Furtivité',
    0x2000: 'Empoisonné'}

STATE_NONE = 0x0
STATE_TAUNT = 0x1
STATE_DIVINE_SHIELD = 0x2
STATE_REBORN = 0x4
STATE_POISONOUS = 0x8
STATE_WINDFURY = 0x10
STATE_ALAKIR = 0x13
STATE_MEGA_WINDFURY = 0x20
STATE_MAGNETIC = 0x40
STATE_FREEZE = 0x80
STATE_ATTACK_IMMEDIATLY = 0x100
STATE_CLEAVE = 0x200
STATE_ATTACK_WEAK = 0x400
STATE_DORMANT = 0x800
STATE_STILL_BOB = 0x880
STATE_STEALTH = 0x1000
STATE_IS_POISONED = 0x2000
STATE_FRENZY = 0x4000 # Frénésie
STATE_ALL = 0xFFFF
        # vol de vie, silence, ne peut pas attaquer

EVENT_NONE = 0x0
EVENT_BEGIN_TURN = 0x1 # début de tour chez bob
EVENT_END_TURN = 0x2 # temps écoulé chez bob
EVENT_FIRST_STRIKE = 0x4 # ou begin turn, début du combat
EVENT_SELL = 0x8 # le joueur vend une carte
EVENT_BUY = 0x10 # le joueur achète une carte
EVENT_LEVELUP = 0x20 # le joueur levelup
EVENT_ROLL = 0x40 # roll manuel
EVENT_PLAY = 0x80 # une carte est jouée
EVENT_CREATION = 0x100 # début de partie

EVENT_INVOC = 0x200 # invocation alliée (chef de meute, mande-flots murloc...)
EVENT_BATTLECRY = 0x400 # cri de guerre
EVENT_DEATHRATTLE = 0x800 # râle d'agonie
EVENT_OVERKILL = 0x1000 # brutalité

EVENT_DIE_ALLY = 0x2000 # un allié meure (charognard, poisson)
EVENT_ATK_ALLY = 0x4000 # un allié attaque
EVENT_DEFEND_ALLY = 0x8000 # un allié est attaqué
EVENT_KILLER_ALLY = 0x10000 # un allié tue un adversaire

EVENT_BOB_PLAY = 0x20000 # Millificent, Nomi ?
EVENT_ATK_MYSELF = 0x40000 # Gardien des glyphes > unused (EVENT_ATK_ALLY)
EVENT_HIT_BY = 0x80000 # Chef du gang des diablotins, Rover de sécurité, Maman des diablotins
EVENT_DEFEND_MYSELF = 0x100000 # Ritualiste tourmenté > unused (EVENT_DEFEND_ALLY)
EVENT_AFTER_ATK_MYSELF = 0x200000 # Ara monstrueux

EVENT_PLAY_ENCHANTMENT = 0x400000 # Capitaine des mers du sud, Mal Ganis
EVENT_LOSS_HP = 0x800000 # Guetteur flottant
EVENT_LOSS_SHIELD = 0x1000000 # Massacreur drakonide, Bolvar

EVENT_USE_POWER = 0x2000000
EVENT_PERMANENT = 0x4000000 # Aile de mort ?
EVENT_DIE_PLAYER = 0x8000000 # Bloc de glace, Biggleworth

EVENT_KILL_MYSELF = 0x10000000 # Nat Pagle, unused (EVENT_KILLER_ALLY)

