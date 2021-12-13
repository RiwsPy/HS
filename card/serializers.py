from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from card.models import Card, Race, Rarity
 
class CardDetailsSerializer(ModelSerializer):
 
    class Meta:
        model = Card
        #fields= ['is_playable', '__all__']
        exclude= ['date_updated', 'howToEarn', 'howToEarnGolden']

 
class CardListSerializer(ModelSerializer):

    class Meta:
        model = Card
        exclude= [
            'howToEarn',
            'howToEarnGolden',
            'set',
            'artist',
            'faction',
            'hideCost',
            'hideStats',
            'collectionText',
            'date_created',
            'date_updated',
            'battlegroundsDarkmoonPrizeTurn',
            'spellSchool',
            'elite',
            'rarity',
            'collectible',
            'text',
            'flavor',
            'targetingArrowText',
            'phase',
            'levelup_cost_mod',
            'roll_cost',
            'minion_cost',
            'duration',
            'avenge_counter',
            'remain_use',
            'referencedTags',
            'cardClass',
            ]

class MinionSerializer(ModelSerializer):
    class Meta:
        model = Card
        exclude = [
            'powerDbfId',
            'max_health',
            'hero_script',
            'battlegroundsHero',
            'remain_use',
            'duration',
            'battlegroundsDarkmoonPrizeTurn',
            'minion_cost',
            'roll_cost',
            'levelup_cost_mod',
            'phase',
        ]

# Serializer test
class RepopSerializer(ModelSerializer):
    repopDbfId = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = ['dbfId', 'name', 'repopDbfId']

    def get_repopDbfId(self, instance):
        queryset = Card.objects.get(dbfId=instance.repopDbfId)
        serializer = MinionSerializer(queryset)
        return serializer.data


class RaceSerializer(ModelSerializer):
    cards = serializers.SerializerMethodField()
    class Meta:
        model = Race
        fields = [
            'name',
            'cards',
            'is_active']

    def get_cards(self, instance):
        queryset = Card.objects.filter(race=instance.name)
        serializer = CardListSerializer(queryset, many=True)
        return serializer.data

    # validate_XXX, où XXX est le nom de l'attribut
    def validate_name(self, value:str):
        value = value.upper()
        if Race.objects.filter(name=value).exists():
            raise serializers.ValidationError(f'Race {value} already exists')
        return value

    def validate(self, data):
        if data['is_active'] is False:
            raise serializers.ValidationError('is_active must be True')
        return data


class RaritySerializer(ModelSerializer):
    class Meta:
        model = Rarity
        fields = '__all__'

    def validate_name(self, value):
        value = value.upper()
        if Rarity.objects.filter(name=value).exists():
            raise serializers.ValidationError(f'Rarity {value} already exists')
        return value
