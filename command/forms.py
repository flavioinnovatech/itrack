# -*- coding: utf8 -*-
from itrack.command.models import Command
from django.forms import *
from django import forms


class CommandForm(ModelForm):
    class Meta:
        model = Command
        exclude = ['time_sent','time_executed','time_received','system','state','sender']
        widgets = {
            'action': RadioSelect(attrs={'disabled':'disabled'})
        }
    
    username = CharField(label="Usuário")
    password = forms.CharField(label="Senha",widget=forms.PasswordInput(render_value=True),)

#    activate = ChoiceField(choices = (("ON","Ativar"),("OFF","Desativar"),),widget=RadioSelect(),label=u"Ação")
        

