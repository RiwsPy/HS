# self: entity.Entity
def damage_resolve(self, *targets):
    for target in targets:
        if not target.is_alive and target in target.owner.entities:
            target.die(killer=self)

def attack(sequence):
    target = sequence.target
    if sequence.target.is_alive:
        sequence.source.damage(target, sequence.source.attack, overkill=True)
        target.damage(sequence.source, target.attack, overkill=False)
