# -*- coding: utf-8 -*-
from django.db import models
from itrack.system.models import System
from itrack.equipments.models import Equipment
from itrack.vehicles.models import Vehicle
# Create your models here.

class Geofence(models.Model):
    system = models.ForeignKey(System, verbose_name = "Sistema")
    equipments = models.ManyToManyField(Equipment, verbose_name = "Equipamentos")
    

class GeoEntity(models.Model):
    geofence = models.ForeignKey(Geofence, verbose_name = "Cerca Eletrônica")
    lat = models.FloatField()
    lng = models.FloatField()
    radius = models.FloatField()
    


