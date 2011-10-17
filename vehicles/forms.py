# -*- coding: utf-8 -*-
from itrack.vehicles.models import Vehicle
from itrack.equipments.models import Equipment
from django.forms import *


TYPE_CHOICE = (
            (u'Carro','Carro'),
            (u'Caminhão', u'Caminhão'),
            (u'Portátil',u'Portátil'),
            (u'Moto',u'Moto'),
            )
            
class VehicleForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(VehicleForm,self).__init__(*args,**kwargs)
        self.fields['chassi'].required = False
        self.fields['color'].required = False
        self.fields['order'].required = False
        self.fields['year'].required = False
        self.fields['model'].required = False
        self.fields['manufacturer'].required = False
    
    class Meta:
        model = Vehicle
        exclude=['equipment','system','last_alert_date','erased']
    type = ChoiceField(choices=TYPE_CHOICE,label=u'Tipo',required=False)
    
    
class SwapForm(Form):
    equipment = ModelChoiceField(Equipment.objects.all())
