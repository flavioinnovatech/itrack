from django.db import models

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from itrack.equipments.models import Equipment

class System(Site):
    class Meta:
        permissions = (("can_create", "Pode criar subsistemas"),)

    users = models.ManyToManyField(User)
    administrator = models.ForeignKey(User,related_name='usuarios')
    parent = models.ForeignKey('self')
    equipments = models.ManyToManyField(Equipment)


    parent.null = True
    parent.blank = True
    def __unicode__(self):
        return self.name
      

class Settings(models.Model):
    
    system = models.ForeignKey(System)
    system.default = 1
    
    title = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='static/img/')
    
    color_site_background = models.CharField(max_length=50)
    color_table_background = models.CharField(max_length=50)
    
    color_menu_gradient_final = models.CharField(max_length=50) 
    color_menu_gradient_inicial = models.CharField(max_length=50)
    color_menu_gradient_final_hover = models.CharField(max_length=50)
    color_menu_gradient_inicial_hover = models.CharField(max_length=50)
    
    color_submenu_gradient_final = models.CharField(max_length=50) 
    color_submenu_gradient_inicial = models.CharField(max_length=50)
    color_submenu_hover = models.CharField(max_length=50)
    
    color_menu_font = models.CharField(max_length=50) 
    color_menu_font_hover = models.CharField(max_length=50)
    color_submenu_font = models.CharField(max_length=50)
    color_submenu_font_hover = models.CharField(max_length=50)
    
    color_table_line_hover = models.CharField(max_length=50)
    color_table_line_font_hover = models.CharField(max_length=50)
    color_table_header = models.CharField(max_length=50)
    color_site_font = models.CharField(max_length=50)
    color_link = models.CharField(max_length=50)

    color_site_background.default = "#e0e0e0"
    color_table_background.default = "#ffffff"
    
    color_menu_gradient_final.default = "#7a7a7a"
    color_menu_gradient_inicial.default = "#a9a9a9"
    color_menu_gradient_final_hover.default = "#a1a1a1"
    color_menu_gradient_inicial_hover.default = "#ebebeb"
    
    color_submenu_gradient_final.default = "#cfcfcf"
    color_submenu_gradient_inicial.default = "#ffffff"
    color_submenu_hover.default = "#a0a0a0"
    
    color_menu_font.default = "#e7e5e5"
    color_menu_font_hover.default = "#444444"
    color_submenu_font.default = "#444444"
    color_submenu_font_hover.default = "#e7e5e5"
    
    color_table_line_hover.default = "#dadada"
    color_table_line_font_hover.default = "#212121"
    color_table_header.default = "#cccccc"
    color_site_font.default = "#000000"
    color_link.default = "#333333"
    
    css = models.TextField()
    css.default = "body {background-color:#E0E0E0}"
    
    map_google = models.BooleanField()
    map_multspectral = models.BooleanField()
    map_maplink = models.BooleanField()
    
    def __unicode__(self):
        return self.title    
