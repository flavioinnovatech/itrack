from django.db import models

# Create your models here.

class CachedGeocode(models.Model):
    
    lat = models.FloatField()
    lng = models.FloatField()
    
    full_address = models.CharField(max_length=100,null=True,blank=True)
    number = models.CharField(max_length=20,null=True,blank=True)
    street = models.CharField(max_length=50,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    administrative_area = models.CharField(max_length=50,null=True,blank=True)    
    country = models.CharField(max_length=50,null=True,blank=True)
    postal_code = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=20, null=True,blank=True)

    def __unicode__(self):
        return str(self.lat)+" , "+str(self.lng)
        
        
