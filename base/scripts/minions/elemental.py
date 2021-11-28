from base.entity import Minion
from base.enums import CardName
from base.scripts.base import *
import random
from base.utils import repeat_effect
from base.sequence import Sequence


BGS_119= Minion # Cyclone crépitant
TB_BaconUps_159= Minion # Cyclone crépitant premium


class BG21_021(battlecry_select_one_minion_and_buff_it):
    # Enfumeur
    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.buff(
            sequence.target,
            attack=self.bonus_value,
            max_health=self.bonus_value
        )

    @property
    def bonus_value(self) -> int:
        return self.controller.level


class BG21_021_G(BG21_021):
    # Enfumeur premium
    @property
    def bonus_value(self) -> int:
        return super().bonus_value*2


class BG21_020(Minion):
    # Rejeton de Lumière éclatant
    bonus_value = 1
    #TODO: activer le bonus
    def avenge(self, sequence: Sequence):
        self.buff(
            self.controller,
            bonus_value=self.bonus_value)


class BG21_020_G(BG21_020):
    # Rejeton de Lumière éclatant premium
    bonus_value = 2


class BG21_040(Minion):
    # Âme en peine recycleuse
    bonus_value = 1
    def play_off(self, sequence: Sequence):
        if sequence.is_ally(self) and sequence.source.race.ELEMENTAL:
            self.buff(
                self.controller,
                remain_use=self.bonus_value)


class BG21_040_G(BG21_040):
    # Âme en peine recycleuse premium
    bonus_value = 2


class BG21_036(Minion):
    # Maître des réalités
    def enhance_on(self, sequence: Sequence):
        if sequence.source.my_zone is self.my_zone and\
                sequence.source.race.ELEMENTAL and\
                (getattr(sequence.source, 'attack', 0) > 0 or\
                getattr(sequence.source, 'max_health', 0) > 0):
            sequence(self.buff, self.enchantmentDbfId, self)
BG21_036= BG21_036 # Maître des réalités premium


class BGS_126(Minion):
    # Elémentaire du feu de brousse
    nb_target = 1
    def combat_end(self, sequence: Sequence):
        damage_left = -sequence.target.health
        if damage_left > 0:
            for new_target in \
                    sequence.target.adjacent_neighbors().shuffle()[:self.nb_target]:
                self.damage(new_target, damage_left)


class TB_BaconUps_166(BGS_126):
    # Elémentaire du feu de brousse premium
    nb_target = 2


class BGS_121(deathrattle_repop):
    # Gentil djinn
    nb_repop = 1
    @repeat_effect
    def deathrattle(self, sequence: Sequence):
        super().deathrattle(sequence)
        for repop in sequence._repops:
            # les cartes sont-elles retirées de la main de bob ?
            self.controller.draw(repop.dbfId)

    @property
    def repopDbfId(self) -> int:
        """
        donne-t-il un elem au hasard de la taverne ou une carte elem choisie au
        hasard parmi toutes les possibilités ?
        maj 18.6 : summon que des serviteurs d'un niveau inférieur ou égal à celui de la taverne
        TODO: Gentle Djinni firstly summons an elemental, and only then puts a copy of it in hand. Therefore, if Djinni's deathrattle triggers more than once, but there is not enough space on board to summon another minion, the player will not receive a second and subsequent copy of elemental.
        : le gain ne se fait que si le repop à lieu
        """
        return random.choice(self.controller.deck.filter(race='ELEMENTAL').exclude(self.dbfId)).dbfId

class TB_BaconUps_165(BGS_121):
    # Gentil djinn premium
    nb_repop = 2


class BGS_122(Minion):
    # Elementaire de stase
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        minion_dbfId = self.discover(
            self.controller.deck.filter(race='ELEMENTAL'),
            nb=1)
        try:
            minion_id = self.controller.bob.board.create_card_in(minion_dbfId)
        except BoardAppendError:
            pass
        else:
            minion_id.FREEZE = True


class TB_BaconUps_161(BGS_122):
    # Elementaire de stase premium
    nb_strike = 2


class BGS_123(Minion):
    # Tempête de la taverne
    nb_strike = 1

    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.controller.draw(
            self.discover(
                self.controller.deck.filter(race='ELEMENTAL'),
                nb=1)
        )


class TB_BaconUps_162(BGS_123):
    # Tempête de la taverne premium
    nb_strike = 2


class BGS_116(Minion):
    # Anomalie actualisante
    bonus_value = 1
    @repeat_effect
    def battlecry(self, sequence: Sequence):
        self.buff(
            self.controller,
            remain_use=self.bonus_value)


class TB_BaconUps_167(BGS_116):
    # Anomalie actualisante premium
    bonus_value = 2


class BGS_127(Minion):
    # Roche en fusion
    def play_off(self, sequence: Sequence):
        if sequence.source.race.ELEMENTAL and sequence.is_ally(self):
            self.buff(self)
TB_Baconups_202= BGS_127 # Roche en fusion premium


class BGS_120(Minion):
    # Elémentaire de fête
    nb_strike = 1

    @repeat_effect
    def play_off(self, sequence: Sequence):
        if sequence.source.race.ELEMENTAL and sequence.is_ally(self):
            self.buff(
                self.my_zone.cards.filter(race='ELEMENTAL').exclude(self).random_choice()
            )


class TB_BaconUps_160(Minion):
    # Elémentaire de fête premium
    nb_strike = 2


class BGS_100(Minion):
    # Mini Rag
    nb_strike = 1

    @repeat_effect
    def play_off(self, sequence: Sequence):
        if sequence.source.race.ELEMENTAL:
            self.buff(
                self.my_zone.cards.random_choice(),
                attack=sequence.source.level,
                max_health=sequence.source.level)


class TB_BaconUps_200(BGS_100):
    # Mini Rag premium
    nb_strike = 2


class BGS_115(Minion):
    # Élémenplus
    nb_strike = 1

    @repeat_effect
    def sell_end(self, sequence: Sequence):
        self.controller.draw(64040)


class TB_BaconUps_156(Minion):
    # Élémenplus premium
    nb_strike = 2

BGS_115t= Minion # Goutte d'eau


class BGS_105(Minion):
    # Chambellan Executus
    bonus_value = 1

    @repeat_effect
    def turn_off(self, sequence: Sequence):
        self.buff(
            self.my_zone[0],
            attack=self.bonus_value,
            max_health=self.bonus_value)

    @property
    def nb_strike(self) -> int:
        return self.controller.played_cards[self.nb_turn].filter(type='MINION', race='ELEMENTAL')+1

class TB_BaconUps_207(BGS_105):
    # Chambellan Executus premium
    bonus_value = 2

class BGS_104(Minion):
    # Nomi
    #TODO: à compléter, n'affecte pas les serviteurs déjà présents dans la taverne
    bonus_value = 1
    def play_off(self, sequence: Sequence):
        # s'active après le battlecry de l'élémentaire de stase
        if sequence.is_ally(self) and sequence.source.race.ELEMENTAL:
            self.buff(
                self.controller,
                bonus_value=self.bonus_value
            )


class TB_BaconUps_201(BGS_104):
    # Nomi premium
    bonus_value = 2


class BGS_124(Minion):
    # Lieutenant Garr
    def play_off(self, sequence: Sequence):
        if self is not sequence.source and sequence.source.race.ELEMENTAL:
            for _ in self.my_zone.cards.filter(race='ELEMENTAL'):
                self.buff(self)
TB_BaconUps_163= BGS_124 # Lieutenant Garr premium

BGS_128= battlecry_select_all_and_buff_them # Assistant arcanique
TB_Baconups_203= BGS_128 # Assistant arcanique premium
