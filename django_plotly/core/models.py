from django.db import models

# Create your models here.
class FINEDUST(models.Model):
    date = models.IntegerField()
    weighted_average = models.FloatField()
    
    
    class Meta:
        ordering = ('date',)
        


class CITY_FINEDUST(models.Model):
    date = models.IntegerField()
    seoul = models.FloatField()
    busan = models.FloatField()
    daegu = models.FloatField()
    incheon = models.FloatField()
    gwangju = models.FloatField()
    daejeon = models.FloatField()
    ulsan = models.FloatField()
    sejong = models.FloatField()
    gyeonggi = models.FloatField()
    gangwon = models.FloatField()
    chungbuk = models.FloatField()
    chungnam = models.FloatField()
    jeonbuk = models.FloatField()
    jeonnam = models.FloatField()
    gyeongbuk = models.FloatField()
    gyeongnam = models.FloatField()
    jeju = models.FloatField()
    
    class Meta:
        ordering = ('date',)
        
        

class NUM_NEWS(models.Model):
    date = models.IntegerField()
    num_news = models.IntegerField()
    
    class Meta:
        ordering = ('date',)        
        


class STATION_LOCATION(models.Model):
    station_name = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.station_name
    




class STATION_LOCATION2(models.Model):
    station_name = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.station_name
    


class NURAK(models.Model):
    name = models.CharField(max_length=250)
    addr = models.CharField(max_length=250)
    
    class Meta:
        ordering = ('name',)