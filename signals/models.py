from django.db import models
from infotrack.equipments.models import  Equipment
from django.contrib.auth.models import User
from infotrack.system.models import System

class Alert(models.Model):
    name = models.CharField(max_length=200)
    equipment = models.ForeignKey(Equipment)
    system = models.ForeignKey(System)
    destinataries = models.ManyToManyField(User)
    time_start = models.DateTimeField('inicio do monitoramento')
    time_end = models.DateTimeField('fim do monitoramento')
    receive_email = models.BooleanField()
    receive_sms = models.BooleanField()
    def __unicode__(self):
        return self.name
    
class Command(models.Model):
    equipment = models.ForeignKey(Equipment)
    system = models.ForeignKey(System)
    type = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    time_sent = models.DateTimeField('data enviada')
    time_received = models.DateTimeField('data recebida')
    time_executed = models.DateTimeField('data executada')
    def __unicode__(self):
        return self.equipment.name
    


