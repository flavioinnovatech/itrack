# -*- coding:utf8 -*-

from django.db import models
from itrack.equipments.models import Equipment
# Create your models here.

class Vehicle(models.Model):
    equipment = models.ForeignKey(Equipment, verbose_name= "Equipamento")
    chassi = models.CharField(max_length=30)
    license_plate = models.CharField(max_length=10, verbose_name="Placa")
    color = models.CharField(max_length=20, verbose_name = "Cor")
    year = models.CharField(max_length=30,verbose_name= "Ano")
    model = models.CharField(max_length=30,verbose_name= "Modelo")
    manufacturer = models.CharField(max_length=30,verbose_name= "Marca")
    type = models.CharField(max_length=30, verbose_name = "Tipo de Veículo")
    def __unicode__(self):
        return self.license_plate