# -*- coding:utf8 -*-

from django.db import models
from itrack.equipments.models import  Equipment
from django.contrib.auth.models import User
from itrack.system.models import System
from itrack.vehicles.models import Vehicle


class Alert(models.Model):
    name = models.CharField(max_length=200,verbose_name = 'Nome do monitoramento')
    vehicle = models.ManyToManyField(Vehicle,verbose_name = 'Veículo')
    system = models.ForeignKey(System)
    destinataries = models.ManyToManyField(User,verbose_name='Notificados')
    time_start = models.DateTimeField('inicio do monitoramento')
    time_end = models.DateTimeField('fim do monitoramento')
    receive_email = models.BooleanField(verbose_name = 'Receber alerta por email')
    receive_sms = models.BooleanField(verbose_name = 'Receber alerta por SMS')
    TRIGGER_CHOICES = (
            (u'0', u'Alerta de pânico'),
            (u'1', u'Veículo for ligado'),
            (u'2', u'Limite de Velocidade'),
            (u'3', u'Cerca eletrônica')
    )
    trigger = models.CharField(max_length=200, choices=TRIGGER_CHOICES)
    trigger.default = "0"
    velocity_limit = models.DecimalField(max_digits=4, decimal_places=0,verbose_name = 'Limite de Velocidade (km/h)')
    velocity_limit.null = True
    velocity_limit.blank = True
    velocity_limit.null = True
    velocity_limit.blank = True
    def __unicode__(self):
        return self.name
