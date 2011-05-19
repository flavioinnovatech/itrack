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
            
    password = forms.CharField(widget=forms.PasswordInput(render_value=True),max_length=100)
    
class UserTailForm(forms.ModelForm):
    telephone = forms.CharField(max_length=20, label = "Telefone")
    cellphone = forms.CharField(max_length=20, label = "Celular")
    address = forms.CharField(max_length=200, label = "Endereço")
    city = forms.CharField(max_length=50, label= "Cidade")

class UserCompleteForm(UserForm,UserTailForm):
    pass
