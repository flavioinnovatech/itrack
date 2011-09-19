# -*- coding: utf8 -*-

from django.db import models
from itrack.equipments.models import  Equipment, CustomFieldName
from itrack.vehicles.models import Vehicle
from django.contrib.auth.models import User
from itrack.system.models import System
from django.db.models import Max

STATE_CHOICES = ((u'0',"Enviado para o servidor"),(u'1',"Transmitindo para o equipamento"),(u'2',"Comando executado"),(u'3',"Falha no envio"))
ACTION_CHOICES = (("ON","Ativar"),("OFF","Desativar"),)

class Command(models.Model):

    equipment = models.ForeignKey(Vehicle,verbose_name=u"Veículo")
    system = models.ForeignKey(System)
    type = models.ForeignKey(CustomFieldName,verbose_name="Comando",null=True)
    state = models.CharField(max_length=50, choices = STATE_CHOICES)
    action = models.CharField(max_length=10, choices = ACTION_CHOICES,verbose_name= u"Ação",default='ON')
    time_sent = models.DateTimeField('data enviada',blank=True,null=True)
    time_received = models.DateTimeField('data recebida',blank=True,null=True)
    time_executed = models.DateTimeField('data executada',blank=True,null=True)
    sender = models.ForeignKey(User,blank=True,null=True)
    
    def __unicode__(self):
        return self.equipment.license_plate
        
class CPRSession(models.Model):
    key = models.CharField(max_length=50)
    time = models.DateTimeField('timestamp')
