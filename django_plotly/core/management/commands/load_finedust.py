import csv
from datetime import date
from itertools import islice
from typing import Any
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import FINEDUST


class Command(BaseCommand):
    help = 'Load data from finedust file'
    
    def handle(self, *args, **options):
        datafile = settings.BASE_DIR / 'data' / 'finedust_plotly.csv'
        
        with open(datafile, 'r', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(islice(csvfile, 0, None))
            
            for row in reader:
                year = int(row['연도'])
                FINEDUST.objects.get_or_create(date=year, weighted_average=row['전국인구가중평균'])
                