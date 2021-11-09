from entity import Enchantment

buff_attr_add = {
    'attack', # : int
    'max_health', # : int
    'health', # int
    #'mechanics', # list
}

class add_stat(Enchantment):
    def apply(self):
        target = self.owner
        for attr in buff_attr_add & set(dir(self)) & set(dir(target)):
            target[attr] += self[attr]
        for mechanic in self.mechanics:
            setattr(target, mechanic, True)

BGS_066e= add_stat # Or raflé
TB_BaconUps_130e= add_stat # Or raflé
GVG_076a= add_stat # Pistons
TB_BaconUps_094e= add_stat # Pistons
BGS_033e1= add_stat # Bien nourri
TB_BaconUps_104e= add_stat # Bien nourri
BGS_004e= add_stat # Colère tissée
TB_BaconUps_079e= add_stat # Colère tissée
EX1_509e= add_stat # Blarghghl
TB_BaconUps_011e= add_stat # Blarghghl
BGS_081e= add_stat # Du butin !
TB_BaconUps_143e= add_stat # Du butin !
BGS_124e= add_stat # Garrdien
TB_BaconUps_163e= add_stat # Garrdien
AT_121e= add_stat # Ego énorme
TB_BaconUps_037e= add_stat # Ego énorme
BGS_075e= add_stat # Atteint de la rage
TB_BaconUps_125e= add_stat # Atteint de la rage
BGS_127e= add_stat # Bouclier de lave
TB_Baconups_202e= add_stat # Bouclier de lave
BGS_010e= add_stat # Monstrueux
ICC_807e= add_stat # Dure-écaille
TB_BaconUps_072e= add_stat # Dure-écaille
BGS_036e= add_stat # Soif de dragon
TB_BaconUps_106e= add_stat # Soif de dragon
BGS_202e= add_stat # Échos du Vide
TB_BaconUps_258e= add_stat # Échos du Vide
BGS_112e= add_stat # Illusion du héraut
TB_BaconUps_303e= add_stat # Illusion du héraut
BGS_111e= add_stat # Y’Shaarj !
TB_BaconUps_301e= add_stat # Y’Shaarj !!!
BGS_110e= add_stat # Gros bras !
TB_BaconUps_302e= add_stat # Bras mastoc !
BGS_201e= add_stat # Sacrifice rituel
TB_BaconUps_257e= add_stat # Sacrifice rituel
BGS_047e= add_stat # Yaharr !
TB_BaconUps_134e= add_stat # Yaharr !
BGS_056e= add_stat # Grondement
TB_BaconUps_139e= add_stat # Grondement
ULD_217e= add_stat # Microbandelettes
TB_BaconUps_250e= add_stat # Microbandelettes
BGS_105e= add_stat # Égide du seigneur du feu
ICC_029e= add_stat # Écailles de dragon
TB_BaconUps_120e= add_stat # Écailles de dragon
BGS_009e= add_stat # Béni
TB_BaconUps_082e= add_stat # Béni
BGS_037e= add_stat # Dilatation du temps
TB_BaconUps_107e= add_stat # Dilatation du temps
ICC_858e= add_stat # Lumière faiblissante
TB_BaconUps_047e= add_stat # Lumière faiblissante
BGS_067e= add_stat # Divinité
TB_BaconUps_117e= add_stat # Divinité
BGS_100e= add_stat # Mini-main de Rag
BGS_041e= add_stat # Aspect des Arcanes
TB_BaconUps_109e= add_stat # Aspect des Arcanes
BGS_120e= add_stat # Fête endiablée
BGS_204e= add_stat # Dans la démesure !
TB_BaconUps_304e= add_stat # Dans la démesure !
BGS_021e= add_stat # Saccager
TB_BaconUps_090e= add_stat # Saccager
BGS_017e= add_stat # Appel farouche
TB_BaconUps_086e= add_stat # Appel farouche
BGS_071e= add_stat # Déflect-o-bouclier
TB_BaconUps_123e= add_stat # Déflect-o-bouclier
EX1_531e= add_stat # Bien nourri
TB_BaconUps_043e= add_stat # Bien nourri
GVG_106e= add_stat # Bricolé à fond
TB_BaconUps_046e= add_stat # Bricolé à fond
BGS_035e= add_stat # Cire de dragon
TB_BaconUps_105e= add_stat # Cire de dragon
UNG_999t14e= add_stat # Puissance volcanique
UNG_999t3e= add_stat # Griffes enflammées
UNG_999t4e= add_stat # Carapace de pierre
UNG_999t6e= add_stat # Énorme
UNG_999t13e= add_stat # Crachat de poison
UNG_999t8e= add_stat # Bouclier crépitant
UNG_999t7e= add_stat # Vitesse de l’éclair
UNG_999t2e= add_stat # Spores vivantes
BGS_030e= add_stat # Bagargouillé
TB_BaconUps_100e= add_stat # Bagargouillé
EX1_093e= add_stat # Main d’Argus
TB_BaconUps_009e= add_stat # Main d’Argus
DAL_077e= add_stat # Aileron toxique
CFM_816e= add_stat # Voir grand
TB_BaconUps_074e= add_stat # Voir grand
UNG_073e= add_stat # Formation
TB_BaconUps_061e= add_stat # Formation
GVG_055e= add_stat # Ferraille tordue
TB_BaconUps_069e= add_stat # Ferraille tordue
GVG_048e= add_stat # Dents de métal
TB_BaconUps_066e= add_stat # Dents de métal
BT_010e= add_stat # Carburant gangraileron
TB_BaconUps_124e= add_stat # Carburant gangraileron
CFM_610e= add_stat # Ombres acérées
TB_BaconUps_070e= add_stat # Ombres acérées
BGS_128e= add_stat # Énergie élémentaire
TB_Baconups_203e= add_stat # Énergie élémentaire
BGS_053e= add_stat # La vie de pirate !
TB_BaconUps_138e= add_stat # La vie de pirate !
BGS_038e= add_stat # Étreinte du Crépuscule
TB_BaconUps_108e= add_stat # Étreinte du Crépuscule
EX1_103e= add_stat # Mrghlglhal
TB_BaconUps_064e= add_stat # Mrghlglhal
DS1_070o= add_stat # Présence du maître
TB_BaconUps_068e= add_stat # Présence du maître
BGS_001e= add_stat # Diablerie
TB_BaconUps_062e= add_stat # Diablerie
BGS_082e= add_stat # Petite gorgée de thé
TB_BaconUps_144e= add_stat # Petite gorgée de thé
BGS_083e= add_stat # Grosse gorgée de thé
TB_BaconUps_145e= add_stat # Grosse gorgée de thé
BOT_283e= add_stat # Énergie cinétique
TB_BaconUps_077e= add_stat # Énergie cinétique
BGS_018e= add_stat # Âme de la bête
TB_BaconUps_085e= add_stat # Âme de la bête
BGS_080e= add_stat # Mers brisées
TB_BaconUps_142e= add_stat # Mers brisées
BAR_073e= add_stat # Reforgé
TB_BaconUps_320e= add_stat # Surforgé
OG_256e= add_stat # Poisseux
TB_BaconUps_025e= add_stat # Poisseux
BGS_059e= add_stat # Âme dévorée
VAN_NEW1_027e= add_stat # Yarrr !
TB_BaconUps_136e= add_stat # Yarrr !
EX1_507e= add_stat # Mrgglaargl !
TB_BaconUps_008e= add_stat # Mrgglaargl !
EX1_185e= add_stat # Mode brise-siège
TB_BaconUps_053e= add_stat # Mode brise-siège
GVG_021e= add_stat # Étreinte de Mal’Ganis
TB_BaconUps_060e= add_stat # Étreinte de Mal’Ganis
BG21_039e= add_stat # Emprise de Kathra’natir
BG21_039_Ge= add_stat # Emprise de Kathra’natir
Yod_026e= add_stat # Sacrifice du serviteur
BG20_207e= add_stat # Faveur du Sanglier
BG20_207_Ge= add_stat # Faveur du Sanglier
BG20_302e= add_stat # Mal épineux
BG20_302_Ge= add_stat # Mal épineux
BG20_102e= add_stat # Robuste
BG20_102_Ge= add_stat # Super robuste
BGS_048e= add_stat # Tatouages pirates
TB_BaconUps_140e= add_stat # Tatouages pirates
GVG_027e= add_stat # Bien armé
TB_BaconUps_044e= add_stat # Bien armé
BGS_044e= add_stat # Protégez maman !
BG20_210e= add_stat # Force des ruines maléficiée
BG20_210_Ge= add_stat # Fureur des ruines maléficiée
BG20_106e= add_stat # Retourné
BG21_027e= add_stat # Évoluée
BG21_027_Ge= add_stat # Évoluée
BG21_006e= add_stat # Impétueux
BG21_008e= add_stat # Salin
BG21_008_Ge= add_stat # Super salin
BG21_013e= add_stat # Puissance des dragons
BG21_000e= add_stat # Bond en avant
BG21_000_Ge= add_stat # Bond en avant
BG21_021e= add_stat # Enfumé
BG21_010e= add_stat # Gonflé
BG21_010_Ge= add_stat # Super gonflé
BG21_030e= add_stat # Bourgeonnement
BG21_030_Ge= add_stat # Bourgeonnement
BG21_002e= add_stat # Bien nourri
BG21_002_Ge= add_stat # Bien nourri
BG21_024e= add_stat # Lubrifié
BG21_024_Ge= add_stat # Lubrifié
BG21_016e= add_stat # Amas de butin
BG21_016_Ge= add_stat # Amas de butin
BG21_014e= add_stat # Promotion
BG21_001e= add_stat # Claires-écailles
BG21_001e2= add_stat # Claires-écailles
BG21_003e= add_stat # Réincarnation en cours
BG21_036e= add_stat # Le Plan élémentaire
BG21_036_Ge= add_stat # Le Plan élémentaire
BG21_009e= add_stat # Entraînement du SI:septique
BG21_004e= add_stat # Rassasié
BG21_025e= add_stat # Casse Oméga
BG21_025e2= add_stat # Casse Oméga
BG21_005e= add_stat # Nourri par un gangroptère
TB_BaconShop_HP_015e= add_stat # Bricolé
TB_BaconShop_HP_039e= add_stat # Dans la boîte
TB_BaconShop_HP_066e= add_stat # Verdoyant
TB_BaconShop_HP_041e= add_stat # Rat fidèle
TB_BaconShop_HP_104e= add_stat # Générosité de C’Thun
TB_BaconShop_HP_040e= add_stat # Briqueté
TB_BaconShop_HP_085e= add_stat # Lueurs de taverne
TB_BaconShop_HP_036e2= add_stat # Breuvage démoniaque
TB_BaconShop_HP_014e= add_stat # Givré
TB_BaconShop_HP_087te= add_stat # Main de Ragnaros
TB_BaconShop_HP_001e= add_stat # Lames affûtées
TB_BaconShop_HP_107e= add_stat # Pousse-toi de là !
TB_BaconShop_HP_042e= add_stat # Chapeau
TB_BaconShop_HP_061e= add_stat # Vous brûlerez tous !
TB_BaconShop_HP_068e= add_stat # Emprisonné
TB_BaconShop_HP_068e2= add_stat # Éveillé
TB_BaconShop_HP_024e2= add_stat # Rite de réincarnation
BG20_HERO_102pe2= add_stat # Pour la Horde !
TB_BaconShop_HP_037te= add_stat # Ciré
BG20_HERO_280pe= add_stat # Préparation au combat
BG20_HERO_280p2e= add_stat # Puissance
BG20_HERO_280p3e2= add_stat # Portail fermé
BG20_HERO_242pe= add_stat # Effet bœuf de Guff
BG20_HERO_301pe= add_stat # Crachat reçu
TB_BaconShop_HP_069e= add_stat # Fidèles lieutenants
BOT_312e= add_stat # Menace répliquante
TB_BaconUps_032e= add_stat # Menace répliquante
BOT_911e= add_stat # Ennuy-o-module
TB_BaconUps_099e= add_stat # Ennuy-o-module
BG20_GEMe2= add_stat # Gemmes de sang
TRL_509te= add_stat # Banane
BGS_Treasures_000e= add_stat # Grande banane
TB_Bacon_Secrets_13e= add_stat # Esprit combatif
FP1_020e= add_stat # Vengeance
BGS_104e1= add_stat # Festin de taverne
BG21_020e= add_stat # Ébloui


class BG21_040e(Enchantment):
    # L’actualisation coûte (1)_pièce de moins.
    def roll_on(self, sequence):
        sequence.cost -= 1

    def roll_off(self, sequence):
        self.remain_use -= 1
        if self.remain_use <= 0:
            self.remove()


class BGS_116e(BG21_040e):
    # Actualiser coûte 0.
    def roll_on(self, sequence):
        sequence.cost = 0


class BG20_HERO_201p2e(Enchantment):
    # Esprit échangé
    def apply(self):
        self.owner.attack = self.attack
        self.owner.max_health = self.max_health


class BG20_HERO_101pe2(Enchantment):
    # Gage de paix
    def apply(self):
        self.owner.attack = 2
        self.owner.max_health = 2


class TB_BaconShop_HP_101e(Enchantment):
    # Ticket de Sombrelune
    pass

class BG20_HERO_201p3e(Enchantment):
    # Marqué pour échange (Vol'Jin)
    pass


class BGS_045e(add_stat):
    # Souffle froid
    #TODO: bonus rétroactif ou fixe ? A tester ig avec Illidan
    @property
    def attack(self) -> int:
        return self.owner.attack

    @attack.setter
    def attack(self, value) -> None:
        self._attack = value


class TB_BaconUps_115e(add_stat):
    # Souffle froid premium
    @property
    def attack(self) -> int:
        return self.owner.attack*2

    @attack.setter
    def attack(self, value) -> None:
        self._attack = value


class BGS_104pe(Enchantment):
    # Ench. de joueur Nomi
    def summon_on(self, sequence):
        if sequence.source.controller is self.controller.bob and\
                sequence.source.race.ELEMENTAL:
            self.buff(self.enchantment_dbfId,
                attack=self.bonus_value,
                max_health=self.bonus_value)
BG21_020pe= BGS_104pe # Ench. de joueur Rejeton de Lumière éclatant


class TB_BaconShop_HP_068(add_stat):
    # Emprisonné
    def remove(self):
        super().remove()
        self.buff(self.enchantment_dbfId, self)
        self.controller.opponent.hand.append(self)



# Unofficial enchantment
IMMUNE_000= add_stat # Bloc de glace, Étreinte de Mal’Ganis, Emprise de Kathra’natir


class POISSON(Enchantment):
    # Poisson de N'Zoth
    def apply(self):
        self.owner.DEATHRATTLE = True
        setattr(self, 'deathrattle', self.deathrattle_met)

