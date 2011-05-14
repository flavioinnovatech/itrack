from django.forms import *
from itrack.system.models import System,Settings

class SystemForm(ModelForm):
	    class Meta:
	        model = System
	        exclude = ('parent')



class SettingsForm(ModelForm):
    class Meta:
            model = Settings
            exclude = ('title','system')
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
