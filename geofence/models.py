# -*- coding: utf-8 -*-
from django.db import models
from itrack.system.models import System
from itrack.equipments.models import Equipment
from itrack.alerts.models import Alert
# Create your models here.

class Geofence(models.Model):
    system = models.ForeignKey(System, verbose_name = "Sistema")
    alert = models.ForeignKey(Alert, verbose_name = "Alerta",null = True)
    types = (
            ('C', 'Círculo'),
            ('P', 'Polígono'),
            ('R', 'Rota')
        )
    type = models.CharField(max_length=1, choices=types)
    type.default = 'C'
    def __unicode__(self):
        return str(self.alert.name)
    
class GeoEntity(models.Model):
    geofence = models.ForeignKey(Geofence, verbose_name = "Cerca Eletrônica", null = True)
    lat = models.FloatField()
    lng = models.FloatField()
    radius = models.FloatField()
    seq = models.IntegerField(null = True)
    def __unicode__(self):
        return str(self.lat)+','+str(self.lng)


