from rest_framework.serializers import ModelSerializer
 
from card.models import Card
 
class CardSerializer(ModelSerializer):
 
    class Meta:
        model = Card
        #fields= ['is_playable', '__all__']
        exclude= ['date_updated']
