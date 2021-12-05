from django.core.management.base import BaseCommand

from card.models import Card, Race
from base.enums import Race as Race_data
from json import load
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    help = 'Initialize project for local development'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        Card.objects.all().delete()
        Race.objects.all().delete()
        with open(os.path.join(BASE_DIR, "db/HStat.json"), 'r') as file:
            data = load(file)

        for race in Race_data.data:
            Race.objects.create(name=race)

        race_objects = Race.objects.all()
        for card in data:
            race = card.get('race', 'DEFAULT')
            card['race'] = race_objects.get(name=race)
            Card.objects.create(**card)

        self.stdout.write(self.style.SUCCESS("All Done !"))
