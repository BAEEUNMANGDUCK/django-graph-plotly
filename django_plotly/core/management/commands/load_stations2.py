import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import STATION_LOCATION2


class Command(BaseCommand):
    help = "Load data from Staion file"
    
    
    def handle(self, *args, **options):
        data_file = settings.BASE_DIR / 'data' / 'station_plotly.csv'    
        keys = ('Name', 'decimalLatitude','decimalLongitude')
        
        
        records = []
        with open(data_file, 'r', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    records.append({k: row[k] for k in keys})
                except Exception:
                    pass
                
                if records[-1]['decimalLatitude'] == "":
                    records.pop()
                
                
        for record in records:
            STATION_LOCATION2.objects.get_or_create(
                station_name=record['Name'],
                latitude=record['decimalLatitude'],
                longitude=record['decimalLongitude']
            )