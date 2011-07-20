# -*- coding: utf-8 -*-

from django.forms import *
from django.db.models import Q
from django.contrib.admin.widgets import *
from itrack.equipments.models import CustomField, Equipment, EquipmentType, AvailableFields, CustomFieldName
from itrack.system.models import System
from django.contrib.formtools.wizard import FormWizard
from django.http import HttpResponseRedirect
from itrack.equipments.widgets import ColoredFilteredSelectMultiple
from itrack.system.tools import findDirectChild, findChild

class AvailableFieldsForm(Form):
    equip_type  = CharField(max_length=40,widget = TextInput(attrs={'readonly':True}), label="Modelo")
    custom_fields = ModelMultipleChoiceField(CustomFieldName.objects.all(),widget= ColoredFilteredSelectMultiple("Campos",False,attrs={'rows':'30'}))
    custom_fields.required = False
    
class EquipmentsForm(Form):

    #fields
    equipments = MultipleChoiceField(widget= FilteredSelectMultiple("Equipamentos",False,attrs={'rows':'30'}))
    equipments.required = False
    
    #initialization
    def __init__(self,current_system, system, *args, **kwargs):
        super(EquipmentsForm, self).__init__(*args, **kwargs)

        #searching the brothers of the system: the not_systems list is here to guarantee that only one subsystem
        #can have an equipment of the parent's equip list.
        childs = findChild(current_system)
        parent = System.objects.get(pk=system).parent

        not_systems =  findDirectChild(parent.id)
        
        not_systems.remove(system)
        if not_systems is None:
            not_systems = []
        
        #mounting the list of possible choices    
        queryset = Equipment.objects.filter(system=parent).exclude(system__in=not_systems).order_by('type').values_list('id','serial','type__name')
        initial = Equipment.objects.filter(system=system).values_list('id', flat=True)
        
        queryset = map(lambda x: (x[0],x[1]+' : '+x[2]), queryset)
        #initial = map(lambda x: (x[0],x[1]+' : '+x[2]), initial)
        
        self.fields["equipments"].choices = queryset
        self.fields["equipments"].initial = initial
        
        #cosmetic things
        self.fields["equipments"].label = ""
        
class CustomNameForm(Form):
    name = CharField(max_length=40,widget = TextInput())
    id = CharField(max_length=40,widget = HiddenInput(),required=True)
    

