from django.db import models
from itrack.equipments.models import  Equipment
from django.contrib.auth.models import User
from itrack.system.models import System

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
