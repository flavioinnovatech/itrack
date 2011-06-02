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
            new_setting  = change_css(new_setting)              
            new_setting.save()


        return HttpResponseRedirect('/system/finish/')



def change_css(new_setting):
          new_setting.css = ' #topContainer .centerContainer{ background: url(/media/'+new_setting.logo.name+') no-repeat;}'
          new_setting.css = new_setting.css + ' body {background-color:#'+new_setting.color_site_background+';}'

          #Menu
          new_setting.css = new_setting.css + ' #nav {background: '+new_setting.color_menu_gradient_final+'; filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=#'+new_setting.color_menu_gradient_inicial+', endColorstr=#'+new_setting.color_menu_gradient_final+');}'
          new_setting.css = new_setting.css + ' #nav {background: -moz-linear-gradient(top,  #'+new_setting.color_menu_gradient_inicial+',  #'+new_setting.color_menu_gradient_final+');}'
          new_setting.css = new_setting.css + '#nav {background: -webkit-gradient(linear, left top, left bottom, from(#'+new_setting.color_menu_gradient_inicial+'), to(#'+new_setting.color_menu_gradient_final+'));}'
          new_setting.css = new_setting.css + "#nav .current a, #nav li:hover > a {background-color: #"+new_setting.color_menu_gradient_final_hover+";}"
          new_setting.css = new_setting.css + '#nav .current a, #nav li:hover > a {filter:  progid:DXImageTransform.Microsoft.gradient(startColorstr=#'+new_setting.color_menu_gradient_inicial_hover+', endColorstr=#'+new_setting.color_menu_gradient_final_hover+');}'
          new_setting.css = new_setting.css + '#nav .current a, #nav li:hover > a {background: -moz-linear-gradient(top,  #'+new_setting.color_menu_gradient_inicial_hover+',  #'+new_setting.color_menu_gradient_final_hover+');}'
          new_setting.css = new_setting.css + '#nav .current a, #nav li:hover > a {background: -webkit-gradient(linear, left top, left bottom, from(#'+new_setting.color_menu_gradient_inicial_hover+'), to(#'+new_setting.color_menu_gradient_final_hover+'));}'
          new_setting.css = new_setting.css + '#nav a {color: #'+new_setting.color_menu_font+';}'
          new_setting.css = new_setting.css + '#nav a:hover {color: #'+new_setting.color_menu_font_hover+';}'

          #Submenu
          new_setting.css = new_setting.css + '#nav ul{background-color:#'+new_setting.color_submenu_gradient_final+';}'
          new_setting.css = new_setting.css + ' #nav ul{filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=#'+new_setting.color_submenu_gradient_inicial+', endColorstr=#'+new_setting.color_submenu_gradient_final+');}'
          new_setting.css = new_setting.css + ' #nav ul {background: -moz-linear-gradient(top,  #'+new_setting.color_submenu_gradient_inicial+',  #'+new_setting.color_submenu_gradient_final+');}'
          new_setting.css = new_setting.css + '#nav ul{background: -webkit-gradient(linear, left top, left bottom, from(#'+new_setting.color_submenu_gradient_inicial+'), to(#'+new_setting.color_submenu_gradient_final+'));}'
          new_setting.css = new_setting.css + '#nav ul a:hover {background-color: #'+new_setting.color_submenu_hover+' !important; color:#'+new_setting.color_submenu_font_hover+' !important;}'
          
          # Login Status
          new_setting.css = new_setting.css + '#loginstatus {background-color:#'+new_setting.color_submenu_gradient_final+';}'
          new_setting.css = new_setting.css + '#loginstatus{progid:DXImageTransform.Microsoft.gradient(startColorstr=#'+new_setting.color_submenu_gradient_inicial+', endColorstr=#'+new_setting.color_submenu_gradient_final+');}'
          new_setting.css = new_setting.css + ' #loginstatus {background: -moz-linear-gradient(top,  #'+new_setting.color_submenu_gradient_inicial+',  #'+new_setting.color_submenu_gradient_final+');}'
          new_setting.css = new_setting.css + '#loginstatus{background: -webkit-gradient(linear, left top, left bottom, from(#'+new_setting.color_submenu_gradient_inicial+'), to(#'+new_setting.color_submenu_gradient_final+'));}'
          
          # Botoes
          new_setting.css = new_setting.css + '#actions a {background-color:#'+new_setting.color_submenu_gradient_final+';}'
          new_setting.css = new_setting.css + '#loginstatus{progid:DXImageTransform.Microsoft.gradient(startColorstr=#'+new_setting.color_submenu_gradient_inicial+', endColorstr=#'+new_setting.color_submenu_gradient_final+');}'
          new_setting.css = new_setting.css + ' #actions a {background: -moz-linear-gradient(top,  #'+new_setting.color_submenu_gradient_inicial+',  #'+new_setting.color_submenu_gradient_final+');}'
          new_setting.css = new_setting.css + '#actions a{background: -webkit-gradient(linear, left top, left bottom, from(#'+new_setting.color_submenu_gradient_inicial+'), to(#'+new_setting.color_submenu_gradient_final+'));}'
          
          return new_setting
