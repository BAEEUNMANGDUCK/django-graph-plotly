import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import STATION_LOCATION


class Command(BaseCommand):
    help = "Load data from Staion file"
    
    
    def handle(self, *args, **options):
        data_file = settings.BASE_DIR / 'data' / 'station_coordinate.csv'    
        keys = ('Name', 'decimalLatitude','decimalLongitude')
        
        
        records = []
        with open(data_file, 'r', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append({k: row[k] for k in keys})
                
                
        for record in records:
            STATION_LOCATION.objects.get_or_create(
                station_name=record['Name'],
                latitude=record['decimalLatitude'],
                longitude=record['decimalLongitude']
            )