# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

from itrack.vehicles.models import Vehicle

class Driver(models.Model):
    name = models.CharField(max_length=100,verbose_name="Nome")
    vehicle = models.ForeignKey(Vehicle, verbose_name=u"Veículo")
    identification = models.IntegerField(verbose_name=u"Matrícula")
    address = models.CharField(max_length=200, verbose_name=u"Endereço")
    telephone1 = models.CharField(max_length=20,verbose_name=u"Telefone 1")
    telephone2 = models.CharField(max_length=20,verbose_name=u"Telefone 2")
    photo = models.ImageField(upload_to='img/',verbose_name="Foto")
    photo.default="img/nophoto.jpg"
    
    def __unicode__(self):
        return self.name
