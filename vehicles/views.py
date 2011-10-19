# -*- coding:utf8 -*-

from itrack.vehicles.models import Vehicle
from itrack.vehicles.forms import VehicleForm,SwapForm
from itrack.equipments.models import Equipment
from itrack.system.models import System
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test

def systemVehicleDetails(entity_list,sysid):
    lines = []
    
    system = System.objects.get(pk=int(sysid))
    
    equipment_edit = False
    if system.parent == None:
        equipment_edit = True

    for item in entity_list:

        if type(item).__name__ == 'Equipment':
            lines.append({  
                            'equip_id':item.id,
                            'create_button':True,
                            'edit_equip': equipment_edit,
                            'serial' : item.serial,
                            'simcard' : item.simcard if item.simcard != None else ""
                        })
        else:
            lines.append({  
                            'vehicle_id':item.id,
                            'equip_id':item.equipment.id,
                            'create_button':False,
                            'edit_equip': equipment_edit,
                            'plate': str(item),  
                            'serial': item.equipment.serial,
                            'simcard': item.equipment.simcard if item.equipment.simcard != None else ""
                        })
    
    if entity_list: 
        return lines    
    else: 
        return []
        
@login_required      
def index(request):
    system = request.session['system']
    
    #
    #print vehicle_table
    
    equipments = Equipment.objects.filter(Q(system = system))
    vehicles = list(Vehicle.objects.filter(Q(equipment__system=system)&Q(erased=False)))
    equips_with_vehicle = [x.equipment for x in vehicles]
    for equipment in equipments:
        if equipment not in equips_with_vehicle:
            vehicles.append(equipment)
    
    vehicle_table = systemVehicleDetails(vehicles,system)
    s = System.objects.get(pk=int(system))
    show_simcard = (s.parent == None)
    
    return render_to_response("vehicles/templates/index.html",locals(),context_instance=RequestContext(request))


def create(request,offset):
    
    if request.method == 'POST':
        
        try:
            v = Vehicle.objects.get(Q(license_plate__iexact = request.POST["license_plate"])&Q(erased=True))
            form = VehicleForm(request.POST,instance=v)
        except ObjectDoesNotExist:
            form = VehicleForm(request.POST)
            
        if form.is_valid():
            e = Equipment.objects.get(pk=int(offset))         
            v = form.save(commit=False)
            v.equipment = e
            v.erased = False
            v.save()
            return HttpResponseRedirect("/vehicles/create/finish")
        else:
            return render_to_response("vehicles/templates/create.html",locals(),context_instance=RequestContext(request),)
        
    else:
        form = VehicleForm()
        return render_to_response("vehicles/templates/create.html",locals(),context_instance=RequestContext(request),)
        
def create_finish(request):
    return render_to_response("vehicles/templates/create_finish.html",locals())
        
def edit(request,offset):
    v = Vehicle.objects.get(pk=int(offset))
    if request.method == 'POST':    
        form = VehicleForm(request.POST,instance=v)
        if form.is_valid():
            v = form.save(commit=False)
            #v.equipment = e
            v.save()
            return HttpResponseRedirect("/vehicles/edit/finish")
        else:
            return render_to_response("vehicles/templates/edit.html",locals(),context_instance=RequestContext(request),)
        
    else:
        form = VehicleForm(instance=v)
        return render_to_response("vehicles/templates/edit.html",locals(),context_instance=RequestContext(request),)
        
def edit_finish(request):
    return render_to_response("vehicles/templates/edit_finish.html",locals())


    
def delete(request,offset):
  v = Vehicle.objects.get(pk=int(offset))
  if request.method == 'POST':
    v.erased = True
    v.equipment = None
    v.save()
    
    return HttpResponseRedirect("/vehicles/delete/finish")
    
  else:
      return render_to_response("vehicles/templates/delete.html",locals(),context_instance=RequestContext(request))
      
def delete_finish(request):
    return render_to_response("vehicles/templates/delete_finish.html",locals())


def swap_finish(request):
    return render_to_response("vehicles/templates/swap_finish.html",locals())

def swap(request,offset):
  v = Vehicle.objects.get(pk=int(offset))
  
  if request.method == 'POST':
    form = SwapForm(request.POST)
    
    print "form:",form
    if form.is_valid():
  
        e = Equipment.objects.get(pk=request.POST["equipment"])
        try:
            v2 = Vehicle.objects.get(equipment = e)
        except:
            v2 = None
            
        if v2 != None:
            e2 = Equipment.objects.get(vehicle=v)
            print e2
            print e
            print v
            print v2
            v.equipment = e
            v2.equipment = None
            v2.save()
            v.save()
            v2.equipment = e2
            v2.save()
            
            
        else:
            v.equipment = e
            v.save()
            
        return HttpResponseRedirect("/vehicles/swap/finish")
    else:
        form.fields["equipment"].queryset = Equipment.objects.filter(system=request.session["system"])
        return render_to_response("vehicles/templates/swap.html",locals(),context_instance=RequestContext(request))
  else:
    form = SwapForm()
    form.fields["equipment"].queryset = Equipment.objects.filter(system=request.session["system"])
    return render_to_response("vehicles/templates/swap.html",locals(),context_instance=RequestContext(request))
        

