# -*- coding:utf8 -*-

from django.db import models
from itrack.equipments.models import  Equipment, CustomFieldName
from itrack.geofence.models import Geofence
from django.contrib.auth.models import User
from itrack.system.models import System
from itrack.vehicles.models import Vehicle


class Alert(models.Model):
    name = models.CharField(max_length=200,verbose_name = 'Nome do monitoramento')
    vehicle = models.ManyToManyField(Vehicle,verbose_name = 'Veículo')
    system = models.ForeignKey(System)
    destinataries = models.ManyToManyField(User,verbose_name='Notificados')
    time_start = models.DateTimeField(u'início do monitoramento')
    time_end = models.DateTimeField('fim do monitoramento')
    receive_email = models.BooleanField(verbose_name = 'Receber alerta por email')
    receive_sms = models.BooleanField(verbose_name = 'Receber alerta por SMS')
    receive_popup = models.BooleanField(verbose_name = 'Exibir popups na tela do usuário logado')
    trigger = models.ForeignKey(CustomFieldName,verbose_name="Evento",null=True)
    
    state = models.BooleanField(verbose_name = 'Alertar quando', choices=((True,"Ligado"),(False,"Desligado"),))
    geofence = models.ForeignKey(Geofence, verbose_name = "Cerca Eletrônica",null = True,blank = True)
    linear_limit = models.DecimalField(max_digits=8, decimal_places=0,verbose_name = 'Limite')
    linear_limit.null = True
    linear_limit.blank = True
    active = models.BooleanField(verbose_name = 'Ativo')

    def __unicode__(self):
        return self.name
        
class Popup(models.Model):
    alert = models.ForeignKey(Alert)
    user = models.ForeignKey(User)
    #system = models.ForeignKey(System)
    vehicle = models.ForeignKey(Vehicle)
    date = models.DateTimeField(null = True)
    def __unicode__(self):
        return str(self.alert)+" : "+str(self.vehicle)
