from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api_battlegrounds.permissions import IsAdminAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from card.models import Card, Race, Rarity
from .serializers import CardDetailsSerializer, MinionSerializer, RepopSerializer,\
    CardListSerializer, RaceSerializer, RaritySerializer


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
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


class AdminRaceViewSet(ModelViewSet):
    serializer_class= RaceSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Race.objects.all()


class RarityAPIView(ReadOnlyModelViewSet):
    serializer_class= RaritySerializer

    def get_queryset(self):
        return Rarity.objects.all()


class AdminRarityAPIView(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class= RaritySerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Rarity.objects.all()
