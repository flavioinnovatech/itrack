from django.db import models
from itrack.equipments.models import  Equipment
from django.contrib.auth.models import User
from itrack.system.models import System

# Create your models here.
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
