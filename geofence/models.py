# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from itrack.system.models import System
from itrack.equipments.models import Equipment
# from itrack.alerts.models import Alert

class Geofence(models.Model):
    name = models.CharField(max_length=200,verbose_name = 'Nome da cerca eletrônica',blank=True)
    system = models.ForeignKey(System, verbose_name = "Sistema")
    # alert = models.ForeignKey(Alert, verbose_name = "Alerta",null = True)
    types = (
            ('C', 'Círculo'),
            ('P', 'Polígono'),
            ('R', 'Rota')
        )
    type = models.CharField(max_length=1, choices=types)
    polygon = models.MultiPolygonField(null = True)
    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.name)



'''    
class GeoEntity(models.Model):
    geofence = models.ForeignKey(Geofence, verbose_name = "Cerca Eletrônica", null = True)
    lat = models.FloatField()
    lng = models.FloatField()
    radius = models.FloatField()
    seq = models.IntegerField(null = True)
    def __unicode__(self):
        return str(self.lat)+','+str(self.lng)

'''
