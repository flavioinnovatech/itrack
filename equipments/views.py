# -*- coding: utf-8 -*-
from django.forms import *
from django.contrib.admin.widgets import *
from itrack.equipments.models import Equipment,AvailableFields,CustomField,EquipmentType, CustomFieldName
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from itrack.system.models import System, Settings
from django.contrib.auth.models import User
from itrack.accounts.models import UserProfile
from itrack.system.decorators import system_has_access

from django.forms import ModelForm, TextInput
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from itrack.equipments.forms import AvailableFieldsForm,EquipmentsForm,CustomNameForm
from http403project.http import Http403
from django.db.models import Q,Count

from itrack.system.tools import findChild, isChild, serializeChild, findDirectChild




        
#renders the HTML to edit childs
def render_equipment_html(childs,father="",rendered_list=""):
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
          rendered_list+= render_equipment_html(x,father)
      else:
      #if its a number, mount the entry for the system
          rendered_list+=u"<tr style='width:5%;' id=\"node-"+str(x)+"\" "+ childof +u"><td style='width:50%;'>"+System.objects.get(pk=x).name+u" </td><td style='text-align:center;'><a class='table-button' href=\"/equipment/permissions/"+str(x)+u"/\">Permissões</a>  <a class='table-button' href=\"/equipment/associations/"+str(x)+u"/\">Equipamentos</a><a class='table-button' href=\"/equipment/fieldnames/"+str(x)+u"/\">Campos</a></td></tr>\n"

  return rendered_list    

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def index(request):
    system = request.session["system"]
    childs = findChild(system)
    vector_html = []

    rendered_list = render_equipment_html(childs)
    
    print childs
    
    return render_to_response("equipments/templates/home.html",locals())

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
@system_has_access()
def permissions(request,offset):
 
        childs = findChild(request.session['system'])
        parent = System.objects.get(pk=int(offset)).parent
        system_name = System.objects.get(pk=int(offset))
        
        equip_types = EquipmentType.objects.all()

        AvailableFieldsFormset = formset_factory(AvailableFieldsForm, extra=len(equip_types))        
        if request.method == 'POST':
                formset = AvailableFieldsFormset(request.POST)
                
                if formset.is_valid() or not formset.is_valid():
                    for form in formset.cleaned_data:
                        try:
                            form["equip_type"] = EquipmentType.objects.get(name = form["equip_type"])
                            AvailableFields.objects.filter(Q(system=int(offset))&Q(equip_type=form["equip_type"])).delete()
                            
                            av = AvailableFields()
                            av.system = System.objects.get(pk=int(offset))
                            
                            av.equip_type = form["equip_type"]
                            av.save()
                            
                            for cf in form["custom_fields"]:
                                av.custom_fields.add(cf.custom_field)
                            av.save()
                        except KeyError:
                            pass
                    
                    if request.session["system_being_created"]:
                        return HttpResponseRedirect("/equipment/fieldnames/"+offset)
                    else:        
                        return HttpResponseRedirect("/equipment/finish/")
        else:
            
            formset = AvailableFieldsFormset()
            for form,equip in zip(formset,equip_types):
                
                form.fields["custom_fields"].queryset = CustomFieldName.objects.filter(Q(custom_field__availablefields__system = parent) & Q(custom_field__availablefields__equip_type = equip)& Q(system=int(offset)))
                
                form.fields["custom_fields"].initial = CustomFieldName.objects.filter(Q(custom_field__availablefields__system = int(offset)) & Q(custom_field__availablefields__equip_type = equip)&Q(system=int(offset)))
                
                form.fields["custom_fields"].label = ""
                form.fields["equip_type"].initial = EquipmentType.objects.get(pk=equip.id).name
                if not form.fields["custom_fields"].queryset:
                    form.fields["custom_fields"].widget = HiddenInput()
                    form.fields["equip_type"].widget = HiddenInput()
                    

            return render_to_response("equipments/templates/permissions.html",locals(),context_instance=RequestContext(request)) 
    
def finish(request):
    return render_to_response('equipments/templates/finish.html',locals())

def assoc_finish(request):
    return render_to_response('equipments/templates/assoc_finish.html',locals())
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
@system_has_access()    
def associations(request,offset):

        childs = findChild(request.session['system'])
        parent = System.objects.get(pk=int(offset)).parent
    
        system_name = System.objects.get(pk=int(offset))
        
        if request.method == 'POST':
            form = EquipmentsForm(request.POST)
            if form.is_valid():
                eqset = Equipment.objects.filter(system=int(offset))
                for eq in eqset:
                    eq.system.remove(system_name)
                
                for eq in form.cleaned_data["equipments"]:
                    eq.system.add(system_name)
                    eq.save()
                
                if request.session["system_being_created"]:
                    return HttpResponseRedirect("/equipment/permissions/"+offset)
                else:  
                    return HttpResponseRedirect("/equipment/associations/finish/")
        else:
            form = EquipmentsForm()
            form.fields["equipments"].label = ""
            form.fields["equipments"].initial = Equipment.objects.filter(system=int(offset))
            
            #searching the brothers of the system: the not_systems list is here to guarantee that only one subsystem
            #can have an equipment of the parent's equip list.
            not_systems =  findDirectChild(parent.id)
            not_systems.remove(int(offset))
            print not_systems
            if not_systems is None:
                not_systems = []
            form.fields["equipments"].queryset = Equipment.objects.filter(system=parent).exclude(system__in=not_systems).order_by('type')
            return render_to_response("equipments/templates/associations.html",locals(),context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
@system_has_access() 
def set_names(request,offset):
    system = int(offset)
    cfn_set = CustomFieldName.objects.filter(system__id=system).filter(custom_field__availablefields__system = system).distinct()
    parent = System.objects.get(pk=system).parent
    
    print cfn_set
    
    if parent == None:
        parent = system
    
    print len(cfn_set)
    cfn_parent_set = CustomFieldName.objects.filter(system = parent).filter(custom_field__availablefields__system = system).distinct()
    NameFieldsFormset = formset_factory(CustomNameForm, extra=len(cfn_set))     
    
    if request.method == 'POST':
        formset = NameFieldsFormset(request.POST)
        if formset.is_valid():
            for form in formset.cleaned_data:
                cfn = CustomFieldName.objects.get(pk=int(form["id"]))
                cfn.name = form["name"]
                cfn.save()
            
            if request.session["system_being_created"]:
                request.session["system_being_created"] = False
                return HttpResponseRedirect("/system/finish/")
            else:
                return render_to_response('equipments/templates/assoc_finish.html',locals())

        
        
    else:
        formset = NameFieldsFormset()   
    for form,cfn,pcfn in zip(formset,cfn_set,cfn_parent_set):
        if parent == system:
            form.fields["name"].label = cfn.custom_field.name
        else:
            form.fields["name"].label = pcfn.name
            
        form.fields["name"].initial = cfn.name
        form.fields["id"].initial = cfn.id

    return render_to_response("equipments/templates/fieldnames.html",locals(),context_instance=RequestContext(request))
        
    
    
