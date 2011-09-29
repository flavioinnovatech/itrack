# -*- coding:utf8 -*-

from django.db import models
from itrack.system.models import System

class CustomField(models.Model):
   system = models.ManyToManyField(System)
   name = models.CharField(max_length=200)
   type = models.CharField(max_length=50)
   table = models.IntegerField()
   tag = models.CharField(max_length=50)
   tag.default='tag'
   def __unicode__(self):
      return self.name
      
class CustomFieldName(models.Model):
    system = models.ForeignKey(System, verbose_name="Sistema")
    custom_field = models.ForeignKey(CustomField, verbose_name = "Campo")
    name = models.CharField(max_length=50, verbose_name = "Nome")
    def __unicode__(self):
      return self.name

class EquipmentType(models.Model):
    custom_field = models.ManyToManyField(CustomField)
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=40, verbose_name = "Fabricante", default="Quanta")
    product_id = models.IntegerField(default=41)
    def __unicode__(self):
        return self.name

class AvailableFields(models.Model):
    custom_fields = models.ManyToManyField(CustomField,verbose_name="Campos")

    equip_type = models.ForeignKey(EquipmentType, verbose_name = "Modelo")
    system = models.ForeignKey(System, verbose_name="Sistema")
    def __unicode__(self):
        return self.system.name+' | '+self.equip_type.name
    
class Equipment(models.Model):
   name = models.CharField(max_length=200)
   system = models.ManyToManyField(System, verbose_name="Sistema")
   serial = models.CharField(max_length=50, default='000017E8',null=True,unique= True)
   type = models.ForeignKey(EquipmentType)
   available = models.BooleanField()
   lasttrack_data = models.IntegerField(default=-1,null=False,editable=False)
   lasttrack_update = models.IntegerField(default=-1,null=False,editable=False)
   
   def __unicode__(self):
      return self.serial
      

class Tracking(models.Model):
    msgtype = models.CharField(max_length=20)
    equipment = models.ForeignKey(Equipment)
    eventdate = models.DateTimeField()
    def __unicode__(self):
        return str(self.eventdate)
    
class TrackingData(models.Model):
    tracking = models.ForeignKey(Tracking)
    type = models.ForeignKey(CustomField)
    value = models.CharField(max_length=100)    
    def __unicode__(self):
        return str(self.tracking.eventdate)+" : "+self.type.type +' | ' + self.type.tag
        
class SystemPerms(models.Model):
  
  system = models.ForeignKey(System)
  system.null = True
  
  google_map = models.BooleanField(verbose_name = 'Google - Mapa')
  google_geofence = models.BooleanField(verbose_name = "Google - Geofence")
  maplink_map = models.BooleanField(verbose_name = 'Maplink - Mapa')
  multspectral_map = models.BooleanField(verbose_name = 'Multispectral - Mapa')
  multspectral_geofence = models.BooleanField(verbose_name = 'Multispectral - Geofence')
  can_sms =models.BooleanField(verbose_name = 'Pode enviar SMS')
  
  

