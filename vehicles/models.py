# -*- coding:utf8 -*-

from django.db import models
from itrack.equipments.models import Equipment
from itrack.system.models import System
# Create your models here.

class Vehicle(models.Model):
    system = models.ManyToManyField(System,null=True)
    equipment = models.ForeignKey(Equipment, verbose_name= "Equipamento",blank=True,null=True,unique=True)
    chassi = models.CharField(max_length=30,null=True)
    license_plate = models.CharField(max_length=10, verbose_name="Placa",unique=True)
    order = models.CharField(max_length=6, verbose_name='Ordem',default='')
    color = models.CharField(max_length=20, verbose_name = "Cor",null=True)
    year = models.CharField(max_length=30,verbose_name= "Ano",null=True)
    model = models.CharField(max_length=30,verbose_name= "Modelo",null=True)
    manufacturer = models.CharField(max_length=30,verbose_name= "Marca",null=True)
    type = models.CharField(max_length=30, verbose_name = "Tipo de Veículo")
    last_alert_date = models.DateTimeField(u'Último alerta enviado',null=True)
    threshold_time = models.FloatField(u'Tempo mínimo entre o envio de alertas (em minutos)',default=5)
    erased = models.BooleanField(default=False)
    def __unicode__(self):
        if self.order != '':
            return self.license_plate + ' - ' + self.order
        else:
            return self.license_plate
