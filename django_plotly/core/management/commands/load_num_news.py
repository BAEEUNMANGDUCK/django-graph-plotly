import csv
from datetime import date
from itertools import islice
from typing import Any
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import NUM_NEWS


class Command(BaseCommand):
    help = 'Load data from finedust file'
    
    def handle(self, *args, **options):
        datafile = settings.BASE_DIR / 'data' / 'num_news_finedust.csv'
        
        with open(datafile, 'r', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(islice(csvfile, 0, None))
            
            for row in reader:
                year = int(row['연도'])
                NUM_NEWS.objects.get_or_create(date=year, num_news=row['뉴스개수'])
                