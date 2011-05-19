# -*- coding: utf-8 -*-

from django.forms import *
from django.http import HttpResponseRedirect
from django.contrib.admin.widgets import *
from itrack.system.models import System,Settings
from itrack.equipments.models import Equipment
from django.contrib.formtools.wizard import FormWizard
from itrack.accounts.forms import UserCompleteForm


# this class is used to solve the problem of not being able to derive multiple ModelForm classes with getting all the attrs from the
# parent classes



class SystemForm(ModelForm):
    class Meta:
        model = System
        exclude = ('parent','users','administrator')
    equipments = forms.ModelMultipleChoiceField(queryset=Equipment.objects.all(), widget=FilteredSelectMultiple("Equipamentos", is_stacked=False))
    equipments.label = "Equipamentos"
    


class SettingsForm(ModelForm):
    class Meta:
            model = Settings
            exclude = ('title','system','css')
            widgets = {
                'color_site_background' : TextInput(attrs={'class':'color'}),
                'color_table_background' : TextInput(attrs={'class':'color'}),
                'color_menu_gradient_final' : TextInput(attrs={'class':'color'}),
                'color_menu_gradient_inicial' : TextInput(attrs={'class':'color'}),
                'color_menu_gradient_final_hover' : TextInput(attrs={'class':'color'}),
                'color_menu_gradient_inicial_hover': TextInput(attrs={'class':'color'}),
                'color_submenu_gradient_final': TextInput(attrs={'class':'color'}),
                'color_submenu_gradient_inicial': TextInput(attrs={'class':'color'}),
                'color_submenu_hover': TextInput(attrs={'class':'color'}),
                'color_menu_font': TextInput(attrs={'class':'color'}),
                'color_menu_font_hover': TextInput(attrs={'class':'color'}),
                'color_submenu_font': TextInput(attrs={'class':'color'}),
                'color_submenu_font_hover': TextInput(attrs={'class':'color'}),
                'color_table_line_hover': TextInput(attrs={'class':'color'}),
                'color_table_line_font_hover': TextInput(attrs={'class':'color'}),
                'color_table_header': TextInput(attrs={'class':'color'}),
                'color_site_font': TextInput(attrs={'class':'color'}),
                'color_link': TextInput(attrs={'class':'color'}),
            }
            
class SystemWizard(FormWizard):
    def get_template(self,step):
        return 'system/templates/create_wizard.html'

    def done(self,request,form_list):
        form_data = {}
        for form in form_list:
            for field, value in form.cleaned_data.iteritems():
                form_data[field] = value
            
        print form_data
        print request.FILES
        return HttpResponseRedirect('/system/create/finish/')
