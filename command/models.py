# -*- coding: utf8 -*-

from django.db import models
from itrack.equipments.models import  Equipment
from django.contrib.auth.models import User
from itrack.system.models import System

TYPE_CHOICES = (("Desativar Panico","Desativar Panico"),("Bloquear veiculo","Bloquear veiculo"),("Desbloquear Veiculo","Desbloquear Veiculo"),)
STATE_CHOICES = (("Enviado para o servidor","Enviado para o servidor"),("Aguardando envio para o equipamento","Aguardando envio para o equipamento"),("Transmitindo para o equipamento","Transmitindo para o equipamento"),("Comando executado","Comando executado"))

# Create your models here.
class Command(models.Model):
    equipment = models.ForeignKey(Equipment,verbose_name="Equipamento")
    system = models.ForeignKey(System)
    type = models.CharField(max_length=50, choices = TYPE_CHOICES,verbose_name="Comando")
    state = models.CharField(max_length=50, choices = STATE_CHOICES)
    time_sent = models.DateTimeField('data enviada',blank=True,null=True)
    time_received = models.DateTimeField('data recebida',blank=True,null=True)
    time_executed = models.DateTimeField('data executada',blank=True,null=True)
    def __unicode__(self):
        return self.equipment.name
