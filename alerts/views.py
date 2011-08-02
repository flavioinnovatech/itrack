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

def systemAlertDetails(sysid):
    lines = []
    system = System.objects.get(pk=sysid)
    alerts = Alert.objects.filter(system=system)
    if system.parent == None:
        childof = None
    else:
        childof = system.parent.id
    lines.append({  'id':system.id,
                    'childof':childof,
                    'sysname':system.name,
                })
    for alert in alerts:
        lines.append({  'id':alert.id,
                        'childof':system.id,
                        'alertname':alert.name,
                        'vehicle': alert.vehicle.all(),
                        'timestart':alert.time_start,
                        'timeend':alert.time_end,
                    })
    
    if alerts: 
        return lines    
    else: 
        return []

def mountAlertTree(list_of_childs,parent):
    table = []
    
    if type(list_of_childs).__name__ == 'list':
        if(len(list_of_childs) > 0):
            prev = list_of_childs[0]
            if type(prev).__name__ != 'list':
                lines = systemAlertDetails(prev)
                for line in lines:
                    table.append(line)
            else:
                pass
                
            for el in list_of_childs[1:]:
                
                if type(el).__name__ == 'list':
                    lines = mountAlertTree(el,prev)
                else:
                    lines = mountAlertTree(el,parent)
                
                for line in lines:
                    table.append(line)
                    
                prev = el
    
        return table
           
    else:
        return systemAlertDetails(list_of_childs)
    

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

  childs = findChild(system_id)
  alert_tree = mountAlertTree([system_id,childs],system_id)
  
  return render_to_response("alerts/templates/index.html",locals(),context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='alerta').count() != 0)    
def create(request,offset):
    
    if request.method == 'POST':
        form = AlertForm(int(offset),request.POST)
        
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
            if form.fields["vehicle"].queryset:
                vehicles_exist = True
            else:
                vehicles_exist = False
            
            return render_to_response("alerts/templates/create.html",locals(),context_instance=RequestContext(request),)
        
    else:
        form = AlertForm(int(offset))
        
        if form.fields["vehicle"].queryset:
            vehicles_exist = True
        else:
            vehicles_exist = False
        
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
    system_id = int(request.session['system']) 
    
    #populates the form with the object, and if it's a post, fill with the new information
    if request.method == 'POST':    
        form = AlertForm(system_id,request.POST,instance=v)
    else:
        form = AlertForm(system_id,instance=v)
    #if the form validates, saves the new information
    if form.is_valid():
        v = form.save(commit=False)
        v.destinataries.clear()
        print v.state
        for u in form.data.getlist("destinataries"):
            v.destinataries.add(u)
        v.system_id = system_id
        v.save()
        return HttpResponseRedirect("/alerts/edit/finish")
    
    
    if form.fields["vehicle"].queryset:
        vehicles_exist = True
    else:
        vehicles_exist = False

    
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
    
  


        
