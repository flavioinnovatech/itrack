from django.db import models

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from itrack.equipments.models import Equipment

class System(Site):
    class Meta:
        permissions = (("can_create", "Pode criar subsistemas"),)

    users = models.ManyToManyField(User)
    administrator = models.ForeignKey(User,related_name='usuarios')
    parent = models.ForeignKey('self')
    equipments = models.ManyToManyField(Equipment)


    parent.null = True
    parent.blank = True
    def __unicode__(self):
        return self.name
      

class Settings(models.Model):
    
    system = models.ForeignKey(System)
    system.default = 1
    
    title = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='static/img/')
    
    headerbgcolor = models.CharField(max_length=200)
    headerborder = models.CharField(max_length=200)
    headertext = models.CharField(max_length=200)
   
    contentbgcolor = models.CharField(max_length=200)
    contentborder = models.CharField(max_length=200)
    contenttext = models.CharField(max_length=200)
   
    clickbgcolor = models.CharField(max_length=200)
    clickborder = models.CharField(max_length=200)
    clicktext = models.CharField(max_length=200)
       
    map_google = models.BooleanField()
    map_multspectral = models.BooleanField()
    map_maplink = models.BooleanField()
    
    def __unicode__(self):
        return self.title    
