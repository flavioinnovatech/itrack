# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, TextInput
from itrack.accounts.models import UserProfile
from django.contrib.auth.models import User

class UserProfileForm(ModelForm):
	    class Meta:
	        model = UserProfile
	        exclude = ('profile')

class UserForm(ModelForm):
    class Meta:
            model = User

            exclude = ('is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined','groups','user_permissions')
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(render_value=True),max_length=100,label='Senha')
    
class UserTailForm(forms.ModelForm):
    telephone = forms.CharField(max_length=20, label = "Telefone",required=False)
    cellphone = forms.CharField(max_length=20, label = "Celular")
    address = forms.CharField(max_length=200, label = "Endereço",required=False)
    city = forms.CharField(max_length=50, label= "Cidade",required=False)
    alert = forms.BooleanField(label = 'Visualizar alertas',required=False)
    command = forms.BooleanField(label = 'Visualizar comandos',required=False)

class UserCompleteForm(UserForm,UserTailForm):
    pass

class UserCompleteFormAdmin(UserForm,UserTailForm):
    def __init__(self, *args, **kwargs):
        super(UserCompleteFormAdmin, self).__init__(*args, **kwargs)
        self.fields['alert'].widget = forms.HiddenInput()
        self.fields['command'].widget = forms.HiddenInput()
