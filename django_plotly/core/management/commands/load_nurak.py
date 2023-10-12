import csv
from datetime import date
from itertools import islice
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import NURAK


class Command(BaseCommand):
    help = 'Load data from finedust file'
    
    def handle(self, *args, **options):
        datafile = settings.BASE_DIR / 'data' / 'nurak.csv'
        
        with open(datafile, 'r', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(islice(csvfile, 0, None))
            
            for row in reader:
                NURAK.objects.get_or_create(name=row['Name'], addr=row['Address'])
                