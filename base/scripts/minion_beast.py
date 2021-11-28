from base.entity import Minion
from base.enums import CardName
import random
from .base import *
from base.utils import repeat_effect
from base.sequence import Sequence


class TRL_232(Minion):        
    # Navrecorne cuiracier
    def overkill(self, sequence: Sequence):
        self.invoc(sequence, self.repopDbfId)
TB_BaconUps_051= TRL_232 # Navrecorne cuiracier premium

