from yaml import load
import script_power
import constants
import script_hero
import script_hero_arene

with open('bdd_power.yaml', 'r') as file:
    global BDD_POWER
    BDD_POWER = load(file)

class Power:
    def __init__(self, id, owner):
        info = BDD_POWER.get(id)
        if not info:
            print(f"{self.__class__.__name__} : Unknown power {id}")
            return None

        self.id = id
        self.owner = owner
        self.name = ''
        self.cost = 0
        self.type = 0
        self.remain_use = -1
        self.script = ''
        self.hero_script = 'Default_script'
        self.minion_cost = 3
        self.roll_cost = 1
        self.lst_bob_cost = constants.LEVEL_UP_COST
        self.quest_value = 0
        self.secret_limitation = []

        self.is_disabled = False # une utilisation / tour
        for key, value in info.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'Power ({self.id}): {self.name}'

    @property
    def next_roll_cost(self):
        if self.owner.nb_free_roll > 0:
            return 0
        return self.roll_cost

    def dec_remain_use(self):
        self.remain_use -= 1

    def dec_power_cost(self):
        self.cost = max(0, self.cost - 1)

    def reset_power(self):
        self.is_disabled = False

    def active_manual(self): # effet actif
        if not self.remain_use:
            print("Pouvoir déjà utilisé.")
            return None
        if type(self.owner.opponent) is not type(self.owner.bob):
            print("Pouvoir inutilisable en combat.")
            return None
        if self.is_disabled:
            print("Pouvoir déjà utilisé ce tour-ci.")
            return None
        if self.owner.gold < self.cost:
            print("Utilisation du pouvoir impossible : pas assez d'or !")
            return None

        if self.script:
            result = getattr(script_power, self.script)(self.owner, constants.EVENT_USE_POWER)
            if result is not False:
                self.is_disabled = True
                self.owner.gold -= self.cost
                self.remain_use -= 1
            return result
        return None

    def active(self, *arg): # activation automatique (pouvoir passif)
        if self.script:
            return getattr(script_power, self.script, getattr(script_power, 'no_power'))(self.owner, *arg)

        print("Utilisation du pouvoir impossible !")
        return None

    def active_script(self, recursive):
        if self.hero_script:
            getattr(script_hero, self.hero_script, getattr(script_hero, 'Default_script'))(self.owner, recursive=recursive)

    def active_script_arene(self, *arg):
        if self.hero_script:
            getattr(script_hero_arene, self.hero_script, getattr(script_hero_arene, 'Default_script'))(self.owner, *arg)
