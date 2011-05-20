from django.db import models
from itrack.system.models import System

class CustomField(models.Model):
   name = models.CharField(max_length=200)
   type = models.CharField(max_length=50)
   table = models.IntegerField()
   def __unicode__(self):
      return self.name

class CustomFieldData(models.Model):
   customfield = models.ForeignKey(CustomField)
   name = models.CharField(max_length=200)
   value = models.BigIntegerField()
   type = models.CharField(max_length=50)
   def __unicode__(self):
      return self.name

class EquipmentType(models.Model):
    custom_field = models.ManyToManyField(CustomField)
    name = models.CharField(max_length=200)
    system = models.ManyToManyField(System, verbose_name="Sistema")
    def __unicode__(self):
        return self.name

class AvaliableFields(models.Model):
    custom_fields = models.ManyToManyField(CustomField)
    equip_type = models.ForeignKey(EquipmentType)
    system = models.ForeignKey(System, verbose_name="Sistema")
    def __unicode__(self):
        return self.system.name
    
class Equipment(models.Model):
   name = models.CharField(max_length=200)
   fields = models.ManyToManyField(CustomField)
   type = models.ForeignKey(EquipmentType)
   available = models.BooleanField()
   def __unicode__(self):
      return self.name

   

