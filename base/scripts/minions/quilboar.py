from base.entity import Minion
from base.enums import CardName
from base.scripts.base import *
from base.utils import repeat_effect
from base.sequence import Sequence


class BG21_037(Minion):
    # Fendeur de gemmes
    nb_strike = 1

    @repeat_effect
    def loss_shield_off(self, sequence: Sequence):
        if sequence.is_ally(self):
            self.controller.draw(CardName.BLOOD_GEM)


class BG21_037_G(BG21_037):
    # Fendeur de gemmes premium
    # TODO: une fois doré, les gemmes sont dorées également (même effet, juste visuel ?)
    nb_strike = 2

class BG20_101(Minion):
    # Chauffard huran
    nb_strike = 1

    @repeat_effect
    def frenzy(self, sequence: Sequence):
        self.controller.draw(CardName.BLOOD_GEM)


class BG20_101_G(BG20_101):
    # Chauffard huran premium
    nb_strike = 2


class BG20_102(Minion):
    # Défense robuste
    def enhance_off(self, sequence: Sequence):
        if sequence.target is self and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT:
            self.buff(self)
BG20_102_G= BG20_102 # Défense robuste premium


class BG20_103(Minion):
    # Brute dos-hirsute
    bonus_value = 3

    def enhance_on(self, sequence: Sequence):
        if sequence.target is self and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT and\
                self.TRIGGER_VISUAL:
            sequence.source.attack += self.bonus_value
            sequence.source.max_health += self.bonus_value
            self.TRIGGER_VISUAL = False


class BG20_103_G(BG20_103):
    # Brute dos-hirsute premium
    bonus_value = 6


class BG20_105(Minion):
    # Mande-épines
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.controller.draw(CardName.BLOOD_GEM)
    deathrattle = battlecry


class BG20_105_G(BG20_105):
    # Mande-épines premium
    nb_strike = 2


class BG20_202(Minion):
    # Nécrolyte
    def play_start(self, sequence: Sequence):
        super().play_start(sequence)
        if sequence.is_valid:
            sequence.add_target(
                self.controller.board.cards.choice(self.controller)
            )

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.buff(sequence.target)
        self.buff(sequence.target)
        for neighbour in sequence.target.adjacent_neighbors():
            change = False
            for enchantment in neighbour.entities[::-1]:
                if enchantment.dbfId == CardName.BLOOD_GEM_ENCHANTMENT:
                    enchantment.apply(sequence.target)
                    change = True
            if change:
                neighbour.calc_stat_from_scratch()
        sequence.target.calc_stat_from_scratch()
BG20_202_G= BG20_202 # Nécrolyte premium


class BG20_201(Minion):
    # Porte-bannière huran
    nb_strike = 1

    @repeat_effect
    def turn_off(self, sequence: Sequence):
        for neighbour in self.adjacent_neighbors().filter(race='QUILBOAR'):
            self.buff(neighbour)


class BG20_201_G(BG20_201):
    # Porte-bannière huran premium
    nb_strike = 2


class BG20_104(Minion):
    # Cogneur
    def combat_end(self, sequence: Sequence):
        self.controller.draw(CardName.BLOOD_GEM)
BG20_104_G= BG20_104 # Cogneur premium


class BG20_207(Minion):
    # Duo dynamique
    def enhance_off(self, sequence: Sequence):
        target = sequence.target
        if self.controller is target.controller and\
                target.race.QUILBOAR and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT and\
                self is not sequence.target:
            self.buff(self)
BG20_207_G= BG20_207 # Duo dynamique premium


class BG20_106(Minion):
    bonus_value = 2
    # Tremble-terre
    def enhance_off(self, sequence: Sequence):
        if sequence.target is self and\
                sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT:
            for minion in self.my_zone.cards.exlude(self):
                self.buff(minion, attack=self.bonus_value)


class BG20_106_G(BG20_106):
    # Tremble-terre premium
    bonus_value = 4


class BG20_204(Minion):
    # Chevalier dos-hirsute
    def frenzy(self, sequence: Sequence):
        self.DIVINE_SHIELD = True
BG20_204_G= BG20_204 # Chevalier dos-hirsute premium


class BG20_302(Minion):
    # Aggem malépine
    def enhance_off(self, sequence: Sequence):
        if sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT and\
                self is sequence.target:
            for minion in self.my_zone.cards.one_minion_by_race():
                self.buff(minion)
BG20_302_G= BG20_302 # Aggem malépine premium


class BG20_205(Minion):
    # Agamaggan
    bonus_value = 1
    def enhance_on(self, sequence: Sequence):
        if sequence.source.dbfId == CardName.BLOOD_GEM_ENCHANTMENT and\
                sequence.is_ally(self):
            sequence.source.attack += self.bonus_value
            sequence.source.max_health += self.bonus_value

class BG20_205_G(Minion):
    # Agamaggan premium
    bonus_value = 2


class BG20_303(Minion):
    # Charlga
    nb_strike = 1

    @repeat_effect
    def turn_off(self):
        for minion in self.my_zone.cards:
            self.buff(minion)


class BG20_303_G(BG20_303):
    # Charlga premium
    nb_strike = 2


class BG20_206(Minion):
    # Capitaine Plate-Défense
    #TODO: sequence + optimisation
    mod_quest_value = 4
    def unknown(self, sequence: Sequence):
        for _ in range(sequence.gold_spend):
            self.quest_value += 1
            if self.quest_value % self.mod_quest_value == 0:
                self.controller.draw(CardName.BLOOD_GEM)


class BG20_206_G(BG20_206):
    # Capitaine Plate-Défense premium
    nb_strike = 2

    @repeat_effect
    def unknown(self, sequence: Sequence):
        for _ in range(sequence.gold_spend):
            self.quest_value += 1
            if self.quest_value % self.mod_quest_value == 0:
                self.controller.draw(CardName.BLOOD_GEM)
                self.controller.draw(CardName.BLOOD_GEM)


class BG20_203(Minion):
    # Prophète du sanglier
    def play_off(self, sequence: Sequence):
        if sequence.source.race.QUILBOAR and\
                sequence.is_ally(self) and\
                self.TRIGGER_VISUAL:
            self.controller.draw(CardName.BLOOD_GEM)
            self.TRIGGER_VISUAL = False


class BG20_203_G(BG20_203):
    # Prophète du sanglier premium
    def play_off(self, sequence: Sequence):
        if sequence.source.race.QUILBOAR and\
                sequence.is_ally(self) and\
                self.TRIGGER_VISUAL:
            self.controller.draw(CardName.BLOOD_GEM)
            self.controller.draw(CardName.BLOOD_GEM)
            self.TRIGGER_VISUAL = False


class BG20_301(Minion):
    # Bronze couenne
    nb_strike = 2

    @repeat_effect
    def sell_end(self, sequence: Sequence):
        self.controller.draw(CardName.BLOOD_GEM)


class BG20_301_G(BG20_301):
    # Bronze couenne premium
    nb_strike = 4


class BG20_100(Minion):
    # Géomancien de Tranchebauge
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.controller.draw(CardName.BLOOD_GEM)


class BG20_100_G(BG20_100):
    # Géomancien de Tranchebauge premium
    nb_strike = 2

