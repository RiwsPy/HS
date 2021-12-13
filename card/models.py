from django.db import models, transaction
from django.contrib.postgres.fields import ArrayField
from base.enums import CARD_NB_COPY, state_list, Race as Race_enums, Type, dbfId_attr
from typing import Any

class Race(models.Model):
    name= models.CharField(max_length=30, primary_key=True)
    is_active= models.BooleanField(default=True)

    @transaction.atomic
    # permet de ne pas update les cartes si la sauvegarde sur le type n'a pas fonctionné
    def disable(self):
        if self.is_active is False:
            return
        self.is_active = False
        self.save()
        #self.products.update()


class Rarity(models.Model):
    name= models.CharField(max_length=30, unique=True)


class Card(models.Model):
    RACE = [
        ('ALL', 'ALL'),
        ('NONE', 'NONE'),
        ('BEAST', 'BEAST'),
        ('DEMON', 'DEMON'),
        ('MECHANICAL', 'MECHANICAL'),
        ('MURLOC', 'MURLOC'),
        ('DRAGON', 'DRAGON'),
        ('PIRATE', 'PIRATE'),
        ('ELEMENTAL', 'ELEMENTAL'),
        ('QUILBOAR', 'QUILBOAR'),
    ]

    dbfId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    id = models.CharField(max_length=255, default="no_method")
    techLevel= models.PositiveSmallIntegerField(default=0)
    attack = models.PositiveSmallIntegerField(null=True)
    health = models.PositiveSmallIntegerField(null=True)
    max_health = models.PositiveSmallIntegerField(null=True)

    battlegroundsPremiumDbfId= models.IntegerField(null=True)
    battlegroundsNormalDbfId= models.IntegerField(null=True)
    powerDbfId= models.IntegerField(null=True)
    repopDbfId= models.IntegerField(null=True)
    enchantmentDbfId= models.IntegerField(null=True)

    cardClass= models.CharField(max_length=50, default="NEUTRAL")
    cost= models.IntegerField(default=0)
    # JSONField ??
    mechanics= ArrayField(
            models.CharField(max_length=50, null=True),
            default=list
        )
    referencedTags= ArrayField(
            models.CharField(max_length=50, null=True),
            default=list
        )
    race= models.ForeignKey(Race, on_delete=models.PROTECT)
    #synergy= models.ForeignKey(Race, on_delete=models.PROTECT)
    #race= models.CharField(max_length=30, default='DEFAULT', choices=RACE)
    synergy = models.CharField(max_length=30, default='NONE', choices=RACE)
    type = models.CharField(max_length=30, default="DEFAULT")

    hero_script = models.CharField(max_length=255, null=True)

    battlegroundsHero= models.BooleanField(default=False)
    remain_use= models.PositiveSmallIntegerField(null=True)
    avenge_counter= models.PositiveSmallIntegerField(null=True)
    duration= models.IntegerField(null=True)
    battlegroundsDarkmoonPrizeTurn= models.PositiveSmallIntegerField(null=True)
    minion_cost= models.PositiveSmallIntegerField(null=True)
    roll_cost= models.PositiveSmallIntegerField(default=0)
    levelup_cost_mod= models.PositiveSmallIntegerField(default=0)
    phase= models.CharField(max_length=30, null=True)

    spellSchool= models.CharField(max_length=30, default='')
    elite= models.BooleanField(default=False)
    rarity= models.ForeignKey(Rarity, on_delete=models.PROTECT, default='INVALID')
    #rarity= models.CharField(max_length=30, default='DEFAULT')
    collectible= models.BooleanField(default=False)
    set= models.CharField(max_length=30)
    artist= models.CharField(max_length=255, default='')
    text= models.CharField(max_length=255*16, default='')
    flavor= models.CharField(max_length=255*16, default='')
    targetingArrowText= models.CharField(max_length=255, default='')
    howToEarn= models.CharField(max_length=255, default='')
    howToEarnGolden= models.CharField(max_length=255, default='')
    faction= models.CharField(max_length=30, default='')
    hideStats= models.BooleanField(default=False)
    hideCost= models.BooleanField(default=False)
    collectionText= models.CharField(max_length=255, default='')

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    value = 2


    def __str__(self) -> str:
        return self.name

    @property
    def is_playable(self) -> bool:
        return self.type == Type.MINION and self.techLevel or\
            self.type == Type.HERO and self.battlegroundsHero

    @property
    def nb_copy(self) -> int:
        return CARD_NB_COPY[self.techLevel]

    @property
    def level(self) -> int:
        if self.type == Type.MINION and self.techLevel == 0:
            if self.battlegroundsNormalDbfId:
                return self.__class__.objects.get(pk=self.battlegroundsNormalDbfId).level
            return 1
        return self.techLevel

    def __getattr__(self, attr: str) -> Any:
        if attr in state_list:
            return attr in self.mechanics
        if attr in dbfId_attr:
            return self.__class__.objects.get(pk=getattr(self, attr))
        raise AttributeError

    """
    @property
    def RACE(self):
        return Race_enums(self.race)

    @property
    def SYNERGY(self):
        return Race_enums(self.synergy)

    @property
    def TYPE(self):
        return Type(self.type)
    """
