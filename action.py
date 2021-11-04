# self: entity.Entity
def damage_resolve(self, *targets):
    for target in targets:
        if not target.is_alive and target in target.owner.entities:
            target.die(killer=self)

def attack(sequence):
    for target in sequence.targets.filter(is_alive=True):
        sequence.source.damage(target, sequence.source.attack, overkill=True)
        target.damage(target, target.attack, overkill=False)
