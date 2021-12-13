from django.core.management.base import BaseCommand

from card.models import Card, Race, Rarity
from json import load
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    help = 'Initialize project for local development'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        Card.objects.all().delete()
        with open(os.path.join(BASE_DIR, "db/HStat.json"), 'r') as file:
            data = load(file)

        race_objects = Race.objects.all()
        rarity_objects = Rarity.objects.all()
        for card in data:
            card['race'] = race_objects.get(name=card.get('race', 'NONE'))
            card['rarity'] = rarity_objects.get(name=card.get('rarity', 'INVALID'))

            Card.objects.create(**card)

        self.stdout.write(self.style.SUCCESS("All Done !"))
