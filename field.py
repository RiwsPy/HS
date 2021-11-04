from entity import Entity

class Field(Entity):
    default_attr = {}

    def __init__(self, dbfId, **kwargs):
        self.p1 = None
        self.p2 = None
        super().__init__(dbfId, **kwargs)
        self.append(self.p1)
        self.append(self.p2)
        self.p1.field = self
        self.p2.field = self
        self.combat = None

    def fight_off(self, sequence):
        #TODO: détermination du prochain adversaire ?
        if self.combat:
            for fighter in self.entities:
                fighter.field = None

            if self.combat.winner:
                loser = self.combat.loser.owner
                loser.health -= self.combat.damage

        self.combat = None
