import script_power
import constants

class Hero():
    def __init__(self, bob, key, player):
        # le pouvoir du héros doit dépendre du script non du nom du héros
        self.player = player
        self.key = key
        self.script_power = 0

        info = bob.all_hero.get(key)
        if info:
            self.name = info['name'] or "Nom par défaut"
            self.script_power = info['script_power'] or 0
