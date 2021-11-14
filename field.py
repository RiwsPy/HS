from entity import Entity
from utils import Card_list

class Field(Entity):
    default_attr = {}

    def __init__(self, *args, **kwargs):
        self.p1 = None
        self.p2 = None
        super().__init__(*args, **kwargs)
        self.append(self.p1)
        self.append(self.p2)
        self.p1.field = self
        self.p2.field = self
        self.combat = None

    @property
    def cards(self) -> Card_list:
        return Card_list(*(self.p1.board.cards + self.p2.board.cards))

    def fight_off(self, sequence):
        #TODO: détermination du prochain adversaire ?
        if self.combat:
            for fighter in self.entities:
                fighter.field = None

            if self.combat.winner:
                loser = self.combat.loser.owner
                loser.health -= self.combat.damage

        self.combat = None
