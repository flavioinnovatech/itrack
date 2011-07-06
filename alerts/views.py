# -*- coding:utf8 -*-
from django.db.models import Q
from django.contrib.auth.models import User
from itrack.system.models import System
from itrack.system.views import findChild,isChild
from itrack.equipments.models import Equipment,CustomFieldName
from itrack.alerts.models import Alert
from itrack.alerts.forms import AlertForm
from itrack.equipments.models import Equipment
from itrack.vehicles.models import Vehicle
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect,HttpResponseForbidden
from itrack.geofence.models import Geofence
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
import pprint

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='alerta').count() != 0)
def index(request):

  system_id = request.session['system']

  equipments = Equipment.objects.filter(system = system_id)

  rendered_list = ""
  for item in equipments:
    vehicles = Vehicle.objects.filter(equipment=item.id)

    for v in vehicles:
      alerts = Alert.objects.filter(vehicle=v.id)
      for v in alerts:
        rendered_list+=u"<tr style='width:5%;'><td style='width:25%;'>"+v.name+" </td><td style='width:18%'>"+item.name+"</td><td style='width:25%'>"+str(v.time_start)+"</td><td style='width:20%'>"+str(v.time_end)+"</td><td style='width:120px; padding-left:5px;'><a class='table-button' href=\"/alerts/edit/"+str(v.id)+"/\">Editar</a>  <a class='table-button'  href=\"/alerts/delete/"+str(v.id)+"/\">Apagar</a></td></tr>"


  return render_to_response("alerts/templates/index.html",locals(),context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='alerta').count() != 0)    
def create(request,offset):
    
    if request.method == 'POST':
        form = AlertForm(request.POST)
        
        if form.is_valid():           
            
            system_id = request.session['system']
            a = form.save(commit=False)
            a.system_id = system_id
            a.save()
            
            for dest in form.data.getlist('destinataries'):
              a.destinataries.add(dest)
              
            for vehi in form.data.getlist('vehicle'):
              a.vehicle.add(vehi)
            
            a.save()
            
            try:
              for g in form.data.getlist('geofence'):
                geofence = Geofence.objects.get(pk=g)
                a.geofence = geofence
            except:
              pass
      
            a.save()        
            
            return HttpResponseRedirect("/alerts/create/finish")
        else:
            system_id = int(offset)
            adm_id = System.objects.get(pk=int(system_id)).administrator.id
            e_set = Equipment.objects.filter(system = system_id)
            v_set = []
            for e in e_set:
                try:
                    v_set.append(Vehicle.objects.get(equipment=e.id).id)
                except:
                    print "Veículo não encontrado."
            
            form.fields["vehicle"].queryset = Vehicle.objects.filter(id__in=v_set)
            form.fields["vehicle"].label = "Veículo"
            form.fields["trigger"].queryset = CustomFieldName.objects.filter((Q(custom_field__type = 'Input')|Q(custom_field__type = 'LinearInput')) & Q(system = int(offset)) & Q(custom_field__availablefields__system = int(offset))).distinct()

            form.fields["trigger"].empty_label = "(selecione o trigger)"
            if form.fields["vehicle"].queryset:
                vehicles_exist = True
            else:
                vehicles_exist = False
            
            form.fields['destinataries'].queryset=User.objects.filter(Q(system=int(system_id)) | Q(pk=adm_id) )
            
            return render_to_response("alerts/templates/create.html",locals(),context_instance=RequestContext(request),)
        
    else:
        system_id = int(offset)

        form = AlertForm()
        adm_id = System.objects.get(pk=int(system_id)).administrator.id
        
        e_set = Equipment.objects.filter(system = system_id)
        v_set = []
        for e in e_set:
            try:
                v_set.append(Vehicle.objects.get(equipment=e.id).id)
            except:
                print "Veículo não encontrado."
        
        
        form.fields["vehicle"].queryset = Vehicle.objects.filter(id__in=v_set)
        form.fields["vehicle"].label = "Veículo"
        form.fields["trigger"].queryset = CustomFieldName.objects.filter((Q(custom_field__type = 'Input')|Q(custom_field__type = 'LinearInput')) & Q(system = int(offset)) & Q(custom_field__availablefields__system = int(offset))).distinct()
        

        form.fields["trigger"].empty_label = "(selecione o trigger)"
        if form.fields["vehicle"].queryset:
            vehicles_exist = True
        else:
            vehicles_exist = False
        
        form.fields['destinataries'].queryset=User.objects.filter(Q(system=int(system_id)) | Q(pk=adm_id) )
        
        return render_to_response("alerts/templates/create.html",locals(),context_instance=RequestContext(request))

 
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='alerta').count() != 0) 
def create_finish(request):
    return render_to_response("alerts/templates/create_finish.html",locals())
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='alerta').count() != 0)        
def edit(request,offset):
    #get the alert object
    v = Alert.objects.get(pk=int(offset))
    
    #populates the form with the object, and if it's a post, fill with the new information
    if request.method == 'POST':    
        form = AlertForm(request.POST,instance=v)
    else:
        form = AlertForm(instance=v)
    
    system_id = request.session['system'] 
    
    #if the form validates, saves the new information
    if form.is_valid():
        v = form.save(commit=False)
        v.destinataries.clear()
        for u in form.data.getlist("destinataries"):
            print u
            v.destinataries.add(u)
        v.system_id = system_id
        v.save()
        return HttpResponseRedirect("/alerts/edit/finish")

    #execute this steps if the form does not validate
    #find the equipments to get their vehicles
    e_set = Equipment.objects.filter(system = system_id)
    v_set = []
    for e in e_set:
        try:
            v_set.append(Vehicle.objects.get(equipment=e.id).id)
        except:
            print "Veículo não encontrado."
    
    #put the vehicles in the queryset        
    form.fields["vehicle"].queryset = Vehicle.objects.filter(id__in=v_set)
    form.fields["vehicle"].label = "Veículo"
    
    #get the inputs that are allowed to this system
    form.fields["trigger"].queryset = CustomFieldName.objects.filter((Q(custom_field__type = 'Input')|Q(custom_field__type = 'LinearInput')) & Q(system = system_id) & Q(custom_field__availablefields__system = system_id)).distinct()
    form.fields["trigger"].empty_label = "(selecione o trigger)"
    
    if form.fields["vehicle"].queryset:
        vehicles_exist = True
    else:
        vehicles_exist = False

    # fill the destinataries select with the users of the system
    adm_id = System.objects.get(pk=system_id).administrator.id
    form.fields['destinataries'].queryset=User.objects.filter(Q(system=system_id) | Q(pk=adm_id) )
    
    return render_to_response("alerts/templates/edit.html",locals(),context_instance=RequestContext(request),)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='alerta').count() != 0)    
def edit_finish(request):
    return render_to_response("alerts/templates/edit_finish.html",locals())

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='alerta').count() != 0)  
def delete(request,offset):
  a = Alert.objects.get(pk=int(offset))
  if request.method == 'POST':
    
    a.delete()
    
    return HttpResponseRedirect("/alerts/delete/finish")
    
  else:
      return render_to_response("alerts/templates/delete.html",locals(),context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='alerta').count() != 0)    
def delete_finish(request):
    return render_to_response("alerts/templates/delete_finish.html",locals())


        
