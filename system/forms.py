# -*- coding: utf-8 -*-

from django.forms import *
from django.http import HttpResponseRedirect
from django.contrib.admin.widgets import *
from itrack.system.models import System,Settings
from django.contrib.formtools.wizard import FormWizard
from itrack.accounts.forms import UserCompleteForm, UserForm, UserProfileForm
from itrack.equipments.models import CustomFieldName,SystemPerms
from itrack.equipments.views import associations, permissions,set_names

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
                'color1' : TextInput(attrs={'class':'color'}),
                'color2' : TextInput(attrs={'class':'color'}),
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
            
class PermsForm(ModelForm):
  class Meta:
    model = SystemPerms
        
        
class SystemWizard(FormWizard):
    def get_template(self,step):
        return 'system/templates/create_wizard.html'


    def done(self,request,form_list):
        
        form_data = {}
        for form in form_list:
            for field, value in form.cleaned_data.iteritems():
                form_data[field] = value
                print field,":",value
        
        form_usr = UserForm(form_data)
        form_profile = UserProfileForm(form_data)
        form_sys = SystemForm(form_data)
        form_sett = SettingsForm(form_data,request.FILES)
        form_perms = PermsForm(form_data)
        
        if form_usr.is_valid() and form_profile.is_valid() and form_sys.is_valid() and form_sett.is_valid():
        
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

              cfn_set = CustomFieldName.objects.filter(system = system)
              for cfn in cfn_set:
                cfn2 = CustomFieldName(system = new_sys, custom_field=cfn.custom_field, name = cfn.name)
                cfn2.save()
              
              request.session.update({'system_being_created':True})
              return HttpResponseRedirect('/equipment/associations/'+str(new_sys.id))
              
          else:
            return render_to_response("system/templates/create_wizard.html",locals(),context_instance=RequestContext(request))
            



def change_css(new_setting):

          new_setting.css = '#topContainer .centerContainer{ background-image: url(/media/'+new_setting.logo.name+');}'
          new_setting.css +='body {background-color:#'+new_setting.color_site_background+';}'
          
          color1 = hex_to_rgb(new_setting.color1)
          color1 = ", ".join(map( str, color1 ))
          
          print color1
          
          new_setting.css += '.color1 {background-image: -moz-linear-gradient(rgba('+color1+', 0.2) 0%, rgba('+color1+', 1) 95%);}'

          # print new_setting.css
          
          return new_setting

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))
