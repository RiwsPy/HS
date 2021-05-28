#{'name': }
default_value = {
    'a': 0,
    'h': 0,
    'method': 'no_effect',
    'name': '',
    'duration': -1,
    'key_number': '0',
    'is_premium': False,
    'owner': None,
    'origin': None,
    'type':'enchantment'}

class Enchantment():
    def __init__(self, info) -> None:
        for key, value in {**default_value, **info}.items():
            setattr(self, key, value)

    def __repr__(self):
        if self.method == 'add_stat':
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
        self.owner.health += self.h
        self.owner.max_health += self.h

    def set_stat(self, a=0, h=0):
        self.owner.attack = a
        self.owner.health = h
        self.owner.max_health = h

    def add_state(self, s):
        self.owner.state |= s

    def dec_duration(self):
        self.duration -= 1
        if not self.duration:
            self.remove()

    def remove(self):
        pass