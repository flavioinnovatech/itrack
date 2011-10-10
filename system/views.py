# -*- coding: utf-8 -*-
from django.forms import *
from django.contrib.admin.widgets import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.system.models import System, Settings
from django.contrib.auth.models import User
from itrack.accounts.models import UserProfile
from itrack.equipments.models import Equipment,CustomFieldName
from django.forms import ModelForm, TextInput
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.template.context import RequestContext
from itrack.system.forms import SystemForm, SettingsForm, SystemWizard, change_css
from itrack.accounts.forms import UserCompleteFormAdmin
from itrack.equipments.forms import AvailableFieldsForm,EquipmentsForm,CustomNameForm
from django.db.models import Q
from itrack.system.tools import systemDepth

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

#renders the HTML to edit childs
#Deprecated see v2 below
def render_system_html(childs,rendered_list=""):
    if childs == []: 
        return ""
    rendered_list+="<ul class=\"childs\">"
    for x in childs:
        if  type(x).__name__ == "list":
        #if its a list, execute recursively inside it
            rendered_list+= render_system_html(x)
        else:
        #if its a number, mount the url for the system
            rendered_list+="<li>"+System.objects.get(pk=x).name+" <a class='table-button' href=\"/system/edit/"+str(x)+"/\">Editar</a>  <a class='table-button' href=\"/system/delete/"+str(x)+"/\">Apagar</a></li>\n"
    
    rendered_list+="</ul>"
    return rendered_list
    
def render_system_html2(childs,father="",rendered_list=""):
  if childs == []: 
    return ""
  
  if father != "":
    childof = " class='child-of-node-"+str(father)+"' "
  else:
    childof = ""
  
  for x in childs:
      if  type(x).__name__ == "list":
      #if its a list, execute recursively inside it
          parentIndex = childs.index(x) - 1
          father = System.objects.get(pk=childs[parentIndex]).id
          rendered_list+= render_system_html2(x,father)
      else:
      #if its a number, mount the url for the system
          # rendered_list+=System.objects.get(pk=x).name
          rendered_list+="<tr style='width:5%;' id=\"node-"+str(x)+"\" "+ childof +"><td style='width:50%;'>"+System.objects.get(pk=x).name+" </td><td style='text-align:center;'><a class='table-button' href=\"/system/edit/"+str(x)+"/\">Editar</a>  <a class='table-button' href=\"/system/delete/"+str(x)+"/\">Apagar</a></td></tr>"

  return rendered_list    

#serializes the recursive list from findChild
def serializeChild(childs,ser_list=[]):
    if childs == []: 
        return []
    for x in childs:
        if  type(x).__name__ == "list":
        #if its a list, execute recursively inside it
            serializeChild(x,ser_list)
        else:
        #if its a number, append it
            ser_list.append(x)           
    return ser_list

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def index(request):
    parent = []
    system = System.objects.get(administrator__username=request.user.username)
    
    parent = system.id
    vector = []
    if parent != []:
        childs = findChild(parent)
        vector.append(parent)
        vector.append(childs)
        
        vector_html = render_system_html2(childs)
    
    #controls the depth: systems that are deeper than 4 levels cannot create more subsystems
    if systemDepth(system) >= 4:
        can_create = 0
    else:
        can_create = 1
    
    return render_to_response("system/templates/home.html",locals())

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def create(request):
        system = request.session["system"]

        if systemDepth(System.objects.get(administrator__username=request.user.username)) >= 4:
            return HttpResponseForbidden(u"Você não tem permissão para criar um subsistema.")
        class ModifiedSettingsForm(SettingsForm):
            pass
                
        sysadm = User.objects.get(pk=request.user.id)
        settings_parent = Settings.objects.get(system=system)
        
        
        
        wiz = SystemWizard([UserCompleteFormAdmin,SystemForm,ModifiedSettingsForm])
        return wiz(context=RequestContext(request), request=request, extra_context=locals())

    
def finish(request):
    return render_to_response('system/templates/create_finish.html',locals())
    
def editfinish(request):
    return render_to_response('system/templates/edit_finish.html',locals())
	
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def edit(request,offset):
    #raise an Http 403 error in case the system is not parent of the 'offset' system
    childs = findChild(request.session['system'])
    if isChild(int(offset),childs) or int(offset) == request.session['system']:
        if request.method == 'POST':
            #process the edit form
            print request.POST.__dict__
            system = System.objects.get(pk=int(offset))
            settings = Settings.objects.get(system__id=int(offset))
            
            form_sett = SettingsForm(request.POST,request.FILES,instance=settings)
            form_sys = SystemForm(request.POST,instance=system)       
            
            if form_sys.is_valid() and form_sett.is_valid():
                new_sys = form_sys.save()
                new_setting = form_sett.save(commit=False)
                new_setting.save()
                new_setting  = change_css(new_setting)              
                new_setting.save()
                
                if request.session['system'] == System.objects.get(pk=int(offset)).id:
                    request.session['css'] = new_setting.css
                message =  "Sistema editado com sucesso."    
                return HttpResponseRedirect("/system/edit/finish/")

            else:
              return render_to_response("system/templates/edit.html",locals(),context_instance=RequestContext(request),)
            
        else:
            #display the edit form
        
            system = System.objects.get(pk=int(offset))
            settings = Settings.objects.get(system__id=int(offset))
            system_parent = system.parent_id
            system_admin = system.administrator_id
            
            form_sys = SystemForm(instance = system)
            form_sett = SettingsForm(instance = settings)
            
            
            if request.session["system"] == int(offset)  and system_parent != None:
                #if the system being edited is the admin own system, disable the equipment field, unless he is the root admin
                #del form_sys.fields["equipments"]
                    
                if system_parent == None:
                    system_parent = system.id
                    system_admin = system.administrator.id

                #form_sys.fields["equipments"].queryset = Equipment.objects.filter(system = system_parent)
                
            sysname = system.name
            wiz = SystemWizard([UserCompleteFormAdmin,SystemForm(instance = system),SettingsForm(instance = settings)])
            #return wiz(context=RequestContext(request), request=request, extra_context=locals())
            return render_to_response("system/templates/edit.html",locals(),context_instance=RequestContext(request),)
        
    else:
        return HttpResponseForbidden(u"Você não tem permissão para alterar este sistema.")

def deletefinish(request):
    return render_to_response("system/templates/delete_finish.html",locals())

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def delete(request,offset):
#raise an Http 403 error in case the system is not parent of the 'offset' system
    childs = findChild(request.session["system"])
    if isChild(int(offset),childs):
        if request.method == 'POST':
            ids = serializeChild(findChild(int(offset)),[])
            childs = System.objects.filter(pk__in=ids)
            print childs
            for sys in childs:
                user_list = User.objects.filter(system=sys.id)
                print user_list
                for usr in user_list:
                    UserProfile.objects.get(profile=usr).delete()
                    usr.delete()
                sys.administrator.delete()

            sys = System.objects.get(pk=int(offset))
            sys.administrator.delete()
            #sys.delete()
                
            return HttpResponseRedirect("/system/delete/finish")
        else:
            
            ids = serializeChild(findChild(int(offset)),[])
            childs = System.objects.filter(pk__in=ids)
            main_system = System.objects.get(pk=int(offset)).name
            return render_to_response("system/templates/delete.html",locals(),context_instance=RequestContext(request))
    
            
    else:
        return HttpResponseForbidden(u'Você não tem permissão para apagar este sistema.')

@login_required
def sys_not_created(request):
    if request.method == 'POST':
        request.session["system_being_created"] = False
    return HttpResponse(u'False')
