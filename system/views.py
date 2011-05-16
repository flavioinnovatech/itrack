# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.system.models import System, Settings
from django.forms import ModelForm, TextInput
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from itrack.system.forms import SystemForm, SettingsForm
from http403project.http import Http403


#creates the list of childs for the system with id = 'parent'
def findChild(parent):
    if (System.objects.filter(parent__id=parent).count() == 0):
		return []
    else:
        u=[]
        for x in System.objects.filter(parent__id=parent):
            n = x.id
            u.append(n)
            el = findChild(n)
            if el != []:
                u.append(el)
        return u

#checks if 'system' is a child of the list of childs 'list'        
def isChild(system,childs):
    is_child = False
    for sys in childs:
        if sys == system:
            #found the system in the list
            return True
        elif sys == [] and is_child == False:
            #not found the system yet
                is_child = False
        elif type(sys).__name__ == "list" and is_child == False:
            #if its a list, search recursively inside it
            is_child = isChild(system,sys)
    return is_child

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def index(request):
    parent = []
    system = System.objects.filter(administrator__username=request.user.username)
    for item in system:
        parent = item.id
    vector = []
    if parent != []:
        childs = findChild(parent)
        vector.append(parent)
        vector.append(childs)

    return render_to_response("system/templates/home.html",locals())

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def create(request):
    system = System.objects.filter(users__username__exact=request.user.username)
    
    if request.method == 'POST':
        
        
        form_sett = SettingsForm(request.POST,request.FILES)
        form_sys = SystemForm(request.POST)
        
        for selected_system in system:
            selected_system = selected_system
        
        if form_sys.is_valid():
            new_sys = form_sys.save(commit=False)
            new_sys.parent_id = selected_system.id

            new_sys.save()
            form_sys.save_m2m()
            
        if form_sett.is_valid():
            new_setting = form_sett.save(commit=False)
            new_setting.system_id = new_sys.id
            new_setting.title = new_sys.name
            new_setting.save()

            message = "Sistema criado com sucesso."
            return render_to_response('system/templates/home.html',locals())
            
        else:
            message =  "Form invalido."    
            return render_to_response('system/templates/create.html',locals(),context_instance=RequestContext(request),)


    else:
        form_sys = SystemForm()
        form_sett = SettingsForm()

        return render_to_response("system/templates/create.html",locals(),context_instance=RequestContext(request),)
		
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def edit(request,offset):
    #raise an Http 403 error in case the system is not parent of the 'offset' system
    childs = findChild(request.session['system'])
    if isChild(int(offset),childs) or int(offset) == request.session['system']:
        if request.method == 'POST':
            #process the edit form
            
            system = System.objects.get(pk=int(offset))
            settings = Settings.objects.get(system__id=int(offset))
            
            form_sett = SettingsForm(request.POST,request.FILES,instance=settings)
            form_sys = SystemForm(request.POST,instance=system)       

            print form_sys
            
            if form_sys.is_valid() and form_sett.is_valid():
                new_sys = form_sys.save()
                new_setting = form_sett.save()
                
                message =  "Sistema editado com sucesso."    
                return render_to_response('system/templates/home.html',locals(),)
            else:
                message =  "Form invalido."    
                return render_to_response('system/templates/create.html',locals(),context_instance=RequestContext(request),)
            
        else:
            #display the edit form
            system = System.objects.get(pk=int(offset))
            settings = Settings.objects.get(system__id=int(offset))

            form_sys = SystemForm(instance = system)
            form_sett = SettingsForm(instance = settings)
            
            return render_to_response("system/templates/edit.html",locals(),context_instance=RequestContext(request),)
        
    else:
        raise Http403(u'Você não tem permissão para editar este sistema.')
        


