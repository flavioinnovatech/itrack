# -*- coding: utf-8 -*-

from django.forms import *
from django.http import HttpResponseRedirect
from django.contrib.admin.widgets import *
from itrack.system.models import System,Settings
from django.contrib.formtools.wizard import FormWizard
from itrack.accounts.forms import UserCompleteForm, UserForm, UserProfileForm


class SystemForm(ModelForm):
    class Meta:
        model = System
        exclude = ('parent','users','administrator','available_fields')

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
                print field,":",value
        
        print request.FILES
        
        form_usr = UserForm(form_data)
        form_profile = UserProfileForm(form_data)
        form_sys = SystemForm(form_data)
        form_sett = SettingsForm(form_data,request.FILES)
        
        if form_usr.is_valid():
            new_user = form_usr.save(commit=False)
            new_user.set_password(form_data["password"])
            new_user.save()
            
            
        if form_profile.is_valid():
            new_profile = form_profile.save(commit=False)
            new_profile.profile_id = new_user.id
            new_profile.save()

        sys_id = request.session["system"] 
        system = System.objects.get(pk=sys_id) 
        

        new_user.groups.add(1)
        
        if form_sys.is_valid():
            new_sys = form_sys.save(commit=False)
            new_sys.parent_id = system.id
            new_sys.administrator_id = new_user.id

            new_sys.save()
            form_sys.save_m2m()

        if form_sett.is_valid():
            new_setting = form_sett.save(commit=False)
            new_setting.system_id = new_sys.id
            new_setting.title = new_sys.name
            new_setting.save()
    

        return HttpResponseRedirect('/system/create/finish/')
