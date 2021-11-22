from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
 
from card.models import Card
from .serializers import CardSerializer
 
class CardAPIView(APIView):
    def get(self, *args, **kwargs):
        cards = Card.objects.all()
        if self.request.GET.get('dbfId'):
            cards = cards.filter(dbfId=int(self.request.GET['dbfId']))
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
