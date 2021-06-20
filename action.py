from constants import Event, State, General, Zone
import random

# self: entity.Entity
def damage_resolve(self, *targets):
    for target in targets:
        if target.general == General.MINION and not target.is_alive:
            if target.my_zone.zone_type == Zone.PLAY:
                target.die(self)
            else:
                print(f'{target} die in zone {target.my_zone.zone_type}')
        elif target.general == General.HERO and not target.is_alive:
            target.die()

def damage_fight(self, target, nb=None, overkill=False):
    if target.general == General.ZONE:
        targets = target.cards.exclude(is_alive=False)
        if targets:
            target = random.choice(targets)
        else:
            return

    if nb is None:
        nb = self.attack

    if nb <= 0 or target.state & State.IMMUNE:
        return

    if target.state & State.DIVINE_SHIELD:
        self.append_action(target.remove_attr, state=State.DIVINE_SHIELD)
        return

    target.health -= nb
    target.active_local_event(Event.HIT_BY)
    if self.state & State.POISONOUS:
        target.state |= State.IS_POISONED

    if overkill and target.health < 0:
        self.active_local_event(Event.OVERKILL, target=target)
    self.append_action(damage_resolve, self, *target.owner.entities)

def attack(self, target):
    # pre-attack
    if self is not target:
        self.active_global_event(Event.ATK_ALLY, self.controller, attacker=self)
        self.active_global_event(Event.DEFEND_ALLY, target.controller, defenser=target)

    # damage
    self.append_action(damage_fight, self, target, overkill=True)
    self.append_action(damage_fight, target, self, order=0, overkill=False)
    if self.state & State.CLEAVE:
        for minion in target.adjacent_neighbors():
            self.append_action(damage_fight, self, minion, order=0, overkill=False)

    # after attack
    self.active_local_event(Event.AFTER_ATK_MYSELF)
