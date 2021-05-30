import constants

#{'name': }
default_value = {
    'a': 0,
    'h': 0,
    's': 0,
    'method': 'no_effect',
    'name': '',
    'duration': -1,
    'key_number': '0',
    'is_premium': False,
    'script': {},
    'owner': None,
    'origin': None,
    'type':'enchantment'}

class Enchantment():
    def __init__(self, info) -> None:
        for key, value in {**default_value, **info}.items():
            setattr(self, key, value)

    def __repr__(self):
        if self.method in ('add_stat', 'magnetism'):
            return f'{self.name} {self.a}/{self.h}'
        return f'{self.name}'

    def apply(self):
        if self.owner:
            return getattr(self, self.method)()
        return False

    def no_effect(self, *arg):
        return False
    
    def add_stat(self):
        if self.is_premium:
            self.a *= 2
            self.h *= 2
            self.is_premium = False

        self.owner.attack += self.a
        self.owner.max_health += self.h
        self.owner.health += self.h
        self.owner.state |= self.s

    def set_stat(self): # pas de gestion du state
        self.owner.attack = self.a
        self.owner.health = self.h
        self.owner.max_health = self.h

    def magnetism(self):
        self.name = self.origin.name
        self.owner.attack += self.a
        self.owner.max_health += self.h
        self.owner.health += self.h
        self.owner.state |= self.s
        self.owner.copy_deathrattle(self.origin) # dangerous ?

    def add_script(self):
        self.script = {int(key): value
            for key, value in self.script.items()}
        self.owner.add_script(self.script)

    def dec_duration(self):
        if self.duration == 1:
            self.remove()
        elif self.duration > 1:
            self.duration -= 1

    def remove(self):
        #TODO bug si cumul d'enchantment DORMANT, tous les effets s'activent simultanément
        # bloqué car impossible d'enchanter un minion DORMANT ?
        self.owner.enchantment.remove(self)
        if self.key_number == '314': # endormi
            self.remove_state(constants.STATE_DORMANT)
            self.active_script_type(constants.EVENT_WAKE_UP)
