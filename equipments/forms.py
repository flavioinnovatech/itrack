# -*- coding: utf-8 -*-

from django.forms import *

from django.contrib.admin.widgets import *
from itrack.equipments.models import CustomField, Equipment, EquipmentType, AvailableFields, CustomFieldName
from itrack.system.models import System
from django.contrib.formtools.wizard import FormWizard
from django.http import HttpResponseRedirect

class AvailableFieldsForm(Form):
    equip_type  = CharField(max_length=40,widget = TextInput(attrs={'readonly':True}), label="Modelo")
    custom_fields = ModelMultipleChoiceField(CustomFieldName.objects.all(),widget= FilteredSelectMultiple("Campos",False,attrs={'rows':'30'}))
    custom_fields.required = False
    
class EquipmentsForm(Form):
    equipments = ModelMultipleChoiceField(Equipment.objects.all(),widget= FilteredSelectMultiple("Equipamentos",False,attrs={'rows':'30'}))
    equipments.required = False
        
class CustomNameForm(Form):
    name = CharField(max_length=40,widget = TextInput())
    id = CharField(max_length=40,widget = HiddenInput(),required=True)
