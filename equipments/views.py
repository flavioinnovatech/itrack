# -*- coding: utf-8 -*-
from django.forms import *
from django.contrib.admin.widgets import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.system.models import System, Settings
from django.contrib.auth.models import User
from itrack.accounts.models import UserProfile
from itrack.equipments.models import Equipment
from django.forms import ModelForm, TextInput
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from itrack.system.forms import SystemForm, SettingsForm, UserCompleteForm, SystemWizard
from http403project.http import Http403
from django.db.models import Q



#creates the list of childs for the system with id = 'parent', for the direct childs of the system
def findDirectChild(parent):
        u=[]
        for x in System.objects.filter(parent__id=parent):
            u.append(x.id)
        return u
        
#renders the HTML to edit childs
def render_equipment_html(childs,rendered_list=""):
    if childs == []: 
        return ""
    rendered_list+="<ul class=\"childs\">"
    for x in childs:
        if  type(x).__name__ == "list":
        #if its a list, execute recursively inside it
            rendered_list+= render_system_html(x)
        else:
        #if its a number, mount the url for the equipment
            rendered_list+="<li><a href=\"/equipment/associations/"+str(x)+"/\">"+System.objects.get(pk=x).name+"</a></li>\n"
    
    rendered_list+="</ul>"
    return rendered_list

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def index(request):
    parent = []
    system = request.session["system"]
    
    childs = findDirectChild(system)

        
    vector_html = render_equipment_html(childs)
        
    return render_to_response("equipments/templates/home.html",locals())
