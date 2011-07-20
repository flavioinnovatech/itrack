# -*- coding: utf-8 -*-
from django.forms import *
from django.db.models import Q
from django.contrib.admin.widgets import *

from itrack.equipments.models import CustomFieldName
from itrack.system.models import System
from itrack.vehicles.models import Vehicle
from itrack.geofence.models import Geofence


VEHICLE_CHOICES = (("license_plate","Placa"),("date","Data"),("type","Tipo de veículo"),("address","Endereço"),("system","Sistema"),("color","Cor"),("year","Ano"),("model","Modelo"),("manufacturer","Fabricante"),("chassi","Chassi"))

class PathForm(Form):
    vehicle = ModelChoiceField(Vehicle.objects.all(),label=u"Veículo",widget=Select(attrs={'style':'width: 178px;position:relative;height:25px;'}))
    period_start = DateTimeField(widget=DateTimeInput(attrs={'class':'datepicker','style':'width: 175px;position:relative;'}),label=u"Data inicial")
    period_end = DateTimeField(widget=DateTimeInput(attrs={'class':'datepicker','style':'width: 175px;position:relative;'}),label=u"Data final")
    geofence = ModelChoiceField(Geofence.objects.all(),label=u'Cerca eletrônica',widget=Select(attrs={'style':'width: 178px;position:relative;height:25px;'}))
    
    
    
    def __init__(self, system, *args, **kwargs):
        super(PathForm, self).__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(system=system)
        self.fields['geofence'].queryset = Geofence.objects.filter(system=system)
