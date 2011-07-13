# -*- coding: utf-8 -*-

from django.forms import *
from django.db.models import Q
from django.contrib.admin.widgets import *

from itrack.equipments.models import CustomFieldName
from itrack.system.models import System
from itrack.vehicles.models import Vehicle


VEHICLE_CHOICES = (("license_plate","Placa"),("date","Data"),("type","Tipo de veículo"),("address","Endereço"),("system","Sistema"),("color","Cor"),("year","Ano"),("model","Modelo"),("manufacturer","Fabricante"),("chassi","Chassi"))

class ReportForm(Form):

    vehicle = ModelChoiceField(Vehicle.objects.all(),label=u"Veículo")
    period_start = DateTimeField(widget=DateTimeInput(attrs={'class':'datepicker'}),label=u"Data inicial")
    period_end = DateTimeField(widget=DateTimeInput(attrs={'class':'datepicker'}),label=u"Data final")
    vehicle_fields = MultipleChoiceField(choices=VEHICLE_CHOICES,required=False,widget=FilteredSelectMultiple(u"Dados do veículo",False,attrs={'rows':'30'}))
    fields = ModelMultipleChoiceField(CustomFieldName.objects.all(),widget=FilteredSelectMultiple("Campos",False,attrs={'rows':'30'}),required=False)
    
    
    def __init__(self, system, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(system=system)
        self.fields['fields'].queryset = CustomFieldName.objects.filter(system=system).filter(custom_field__availablefields__system= system).distinct()
        
        #
