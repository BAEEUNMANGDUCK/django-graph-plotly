import csv
from itertools import islice

from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import CITY_FINEDUST


class Command(BaseCommand):
    help = 'Load data from finedust file'
    
    def handle(self, *args, **options):
        datafile = settings.BASE_DIR / 'data' / 'finedust_plotly.csv'
        
        with open(datafile, 'r', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(islice(csvfile, 0, None))
            
            for row in reader:
                year = int(row['연도'])
                sejong=row['세종']
                if sejong == '-':
                    sejong = float(0)
                CITY_FINEDUST.objects.get_or_create(date=year,
                                               seoul=row['서울'],
                                               busan=row['부산'],
                                               daegu=row['대구'],
                                               incheon=row['인천'],
                                               gwangju=row['광주'],
                                               daejeon=row['대전'],
                                               ulsan=row['울산'],
                                               sejong=sejong,
                                               gyeonggi=row['경기'],
                                               gangwon=row['강원'],
                                               chungbuk=row['충북'],
                                               chungnam=row['충남'],
                                               jeonbuk=row['전북'],
                                               jeonnam=row['전남'],
                                               gyeongbuk=row['경북'],
                                               gyeongnam=row['경남'],
                                               jeju=row['제주'],
                                               )
                