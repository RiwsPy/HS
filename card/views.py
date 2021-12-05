from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
 
from card.models import Card, Race
from .serializers import CardDetailsSerializer, MinionSerializer, RepopSerializer,\
    CardListSerializer, RaceSerializer


class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()


class CardAPIView(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = CardListSerializer
    detail_serializer_class = CardDetailsSerializer

    def get_queryset(self):
        cards = Card.objects.all()
        if self.request.GET.get('dbfId'):
            cards = cards.filter(dbfId=int(self.request.GET['dbfId']))
        return cards


class TypeAPIView(ReadOnlyModelViewSet):
    serializer_class = MinionSerializer
 
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()

    def get_queryset(self):
        return Card.objects.filter(type="MINION")


class RepopAPIView(ReadOnlyModelViewSet):
    serializer_class = RepopSerializer
    def get_queryset(self):
        return Card.objects.filter(type="MINION").exclude(repopDbfId=None)


class RaceAPIView(ReadOnlyModelViewSet):
    serializer_class= RaceSerializer
    def get_queryset(self):
        return Race.objects.all()
