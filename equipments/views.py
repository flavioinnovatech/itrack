# -*- coding: utf-8 -*-
from django.forms import *
from django.contrib.admin.widgets import *
from itrack.equipments.models import Equipment,AvailableFields,CustomField,EquipmentType
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from itrack.system.models import System, Settings
from django.contrib.auth.models import User
from itrack.accounts.models import UserProfile

from django.forms import ModelForm, TextInput
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from itrack.equipments.forms import AvailableFieldsForm,EquipmentsForm
from http403project.http import Http403
from django.db.models import Q,Count

from itrack.system.views import findChild, isChild



#creates the list of childs for the system with id = 'parent', for the direct childs of the system
def findDirectChild(parent):
        u=[]
        for x in System.objects.filter(parent__id=parent):
            u.append(x.id)
        return u
        
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
          rendered_list+=u"<tr style='width:5%;' id=\"node-"+str(x)+"\" "+ childof +u"><td style='width:50%;'>"+System.objects.get(pk=x).name+u" </td><td style='text-align:center;'><a class='table-button' href=\"/equipment/permissions/"+str(x)+u"/\">Permissões</a>  <a class='table-button' href=\"/equipment/associations/"+str(x)+u"/\">Equipamentos</a></td></tr>\n"

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
def permissions(request,offset):
 #raise an Http 403 error in case the system is not parent of the 'offset' system
    childs = findChild(request.session['system'])
    parent = System.objects.get(pk=int(offset)).parent
    if (isChild(int(offset), childs)):
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
                                av.custom_fields.add(cf)
                            av.save()
                        except KeyError:
                            pass
                        
                        
                        
                return HttpResponseRedirect("/equipment/finish/")
        else:
            
            formset = AvailableFieldsFormset()
            for form,equip in zip(formset,equip_types):
                form.fields["custom_fields"].queryset = CustomField.objects.filter(Q(availablefields__system = parent) & Q(availablefields__equip_type = equip)).order_by('type')
            
                
                form.fields["custom_fields"].initial = CustomField.objects.filter(Q(availablefields__system = int(offset)) & Q(availablefields__equip_type = equip))
       
                
                form.fields["custom_fields"].label = ""
                form.fields["equip_type"].initial = EquipmentType.objects.get(pk=equip.id).name
                if not form.fields["custom_fields"].queryset:
                    print "aqui!"
                    form.fields["custom_fields"].widget = HiddenInput()
                    form.fields["equip_type"].widget = HiddenInput()
                    

            return render_to_response("equipments/templates/permissions.html",locals(),context_instance=RequestContext(request)) 
    else:
        raise Http403(u'Você não tem permissão para editar este sistema.')
    
def finish(request):
    return render_to_response('equipments/templates/finish.html',locals())

def assoc_finish(request):
    return render_to_response('equipments/templates/assoc_finish.html',locals())
    
def associations(request,offset):
 #raise an Http 403 error in case the system is not parent of the 'offset' system
    childs = findChild(request.session['system'])
    parent = System.objects.get(pk=int(offset)).parent
    if (isChild(int(offset),childs)):
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
                
                return HttpResponseRedirect("/equipment/associations/finish/")
        else:
            form = EquipmentsForm()
            form.fields["equipments"].label = ""
            form.fields["equipments"].initial = Equipment.objects.filter(system=int(offset))

            form.fields["equipments"].queryset = Equipment.objects.filter(system=parent).order_by('type')
            return render_to_response("equipments/templates/associations.html",locals(),context_instance=RequestContext(request))
    else:
        raise Http403(u'Você não tem permissão para editar este sistema.')
    
#def set_names(request,offset):
    
    
