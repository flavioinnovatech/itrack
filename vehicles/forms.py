# -*- coding: utf-8 -*-
from itrack.vehicles.models import Vehicle
from itrack.equipments.models import Equipment
from django.forms import *


TYPE_CHOICE = (
            ('Carro','Carro'),
            (u'Caminhão', u'Caminhão'),
            (u'Portátil',u'Portátil'),
            (u'Moto',u'Moto'),
            )
            
class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        exclude=['equipment','system','last_alert_date','erased']
    type = ChoiceField(choices=TYPE_CHOICE,label=u'Tipo')
    
    
class SwapForm(Form):
    equipment = ModelChoiceField(Equipment.objects.all())
