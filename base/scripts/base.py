from base.entity import Minion, Enchantment
from base.sequence import Sequence
from base.utils import repeat_effect
from base.board import BoardAppendError

class minion_without_script(Minion):
    pass

class battlecry_select_one_minion_and_buff_it(Minion):
    # buff battlecry, only minions of the same synergy can be targeted
    # TODO: gestion carnipousse ? cible au hasard ?
    requirements = {}
    def play_start(self, sequence: Sequence):
        super().play_start(sequence)
        if sequence.is_valid:
            minion = \
                self.controller.board.cards.filter(race=self.synergy).\
                    choice(self.controller)
            sequence.add_target(minion)

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.buff(self.enchantmentDbfId, sequence.target)


class deathrattle_repop(Minion):
    nb_repop = 1

    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        for _ in range(self.nb_repop):
            try:
                repop_id = self.invoc(sequence, self.repopDbfId)
            except BoardAppendError:
                pass
            else:
                sequence._repops.append(repop_id)


class hit_by_repop(Minion):
    nb_repop = 1
    def hit(self, sequence: Sequence):
        if self is sequence.target and sequence.damage_value > 0:
            deathrattle_repop.deathrattle(self, sequence)


class battlecry_select_all_and_buff_them(Minion):
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        minions = self.controller.board.cards.filter_hex(race=self.synergy).exclude(self)
        for minion in minions:
            self.buff(self.enchantmentDbfId, minion)


class aura_buff_race(Minion):
    def summon_on(self, sequence: Sequence):
        if sequence.is_ally(self) and\
                sequence.source.race == self.race:
            self.buff(self.enchantmentDbfId, sequence.source, aura=True)

    def summon_start(self, sequence: Sequence):
        super().summon_start(sequence)
        if sequence.is_valid:
            for minion in self.controller.board.cards:
                if minion.race == self.race:
                    self.buff(self.enchantmentDbfId, minion, aura=True)


class battlecry_buff_myself(Minion):
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.buff(self.enchantmentDbfId, self)


buff_attr_add = {
    'attack', # : int
    'max_health', # : int
    'health', # int
    #'mechanics', # list
}


class add_stat(Enchantment):
    def apply(self):
        for attr in buff_attr_add:
            if getattr(self, attr, None) and getattr(self.owner, attr, None):
                self.owner[attr] += self[attr]
        for mechanic in self.mechanics:
            setattr(self.owner, mechanic, True)
