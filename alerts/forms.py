# -*- coding: utf-8 -*-

from itrack.alerts.models import Alert
from itrack.equipments.models import  Equipment
from django.contrib.admin.widgets import *
from django.contrib.auth.models import User
from itrack.system.models import System
from django.template.context import RequestContext
from django.forms import *
from itrack.vehicles.models import Vehicle

class AlertForm(ModelForm):
    class Meta:
        model = Alert
        exclude = ('system')
        widgets = {
            'time_start' : DateTimeInput(attrs={'class':'datepicker'}),
            'time_end': DateTimeInput(attrs={'class':'datepicker'}),
        }
    
    vehicle = ModelMultipleChoiceField(Vehicle.objects.all(),widget= FilteredSelectMultiple(u"Veículos",False,attrs={'rows':'30'}))
  
    destinataries = ModelMultipleChoiceField(User.objects.all(),widget= FilteredSelectMultiple(u"Notificados",False,attrs={'rows':'30'}))
