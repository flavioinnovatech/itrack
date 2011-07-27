from django.db import models

# Create your models here.

class CachedGeocode(models.Model):
    
    lat = models.FloatField()
    lng = models.FloatField()
    
    full_address = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    administrative_area = models.CharField(max_length=50)    
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.lat)+" , "+str(self.lng)
        
        
