# -*- coding: utf8 -*-
from itrack.command.models import Command
from django.forms import *

class CommandForm(ModelForm):
    class Meta:
        model = Command
        exclude = ['time_sent','time_executed','time_received','system','state']
        widgets = {
            'action': RadioSelect()
        }
    #activate = ChoiceField(choices = (("ON","Ativar"),("OFF","Desativar"),),widget=RadioSelect(),label=u"Ação")
        
