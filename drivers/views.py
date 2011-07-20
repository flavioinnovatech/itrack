# -*- coding: utf-8 -*-

# Create your views here.

# core http handling libs
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from django.template.context import Context,RequestContext
from django.shortcuts import render_to_response

# auth and decorators
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test

#models
from itrack.system.models import System
from itrack.vehicles.models import Vehicle
from itrack.drivers.models import Driver
from django.core.exceptions import ObjectDoesNotExist

#forms
from itrack.drivers.forms import DriverForm, DriverReallocForm


def index(request):

    try:
        
      display_list = []
      
      drivers = Driver.objects.filter(system = request.session['system'])
      
      for d in drivers:
        
        v_array = []
        for v in d.vehicle.all():
          v_array.append(v.license_plate)
          
        v_string = ', '.join(v_array)
                  
        display_list.append({
                    'id':d.id,
                    'name': d.name,
                    'identification': d.identification,
                    'telephone1': d.telephone1,
                    'telephone2': d.telephone2,
                    'photo': d.photo,
                    'vehicle': v_string,
                    'address': d.address,

        })
             
      return render_to_response("drivers/templates/index.html",locals(),context_instance=RequestContext(request))
      
    except ObjectDoesNotExist:
        return HttpResponseNotFound("O veículo solicitado não existe.")     

def profile(request,offset):
    #checks if system can alter the vehicle's drivers
    if request.session['system'] in map(lambda x: x['id'],Driver.objects.get(pk=int(offset)).vehicle.system.values()):
        
        driver = Driver.objects.get(pk=int(offset))
        
        return render_to_response("drivers/templates/profile.html",locals(),context_instance=RequestContext(request))
    
    
    else:
        return HttpResponseForbidden(u"O seu sistema não pode visualizar motoristas deste veículo.")

def create(request):
    #checks if system can alter the vehicle's drivers
    try:
        # if request.session['system'] in map(lambda x: x['id'],Vehicle.objects.get(pk=int(offset)).system.values()):
            if request.method == "POST":
                form = DriverForm(request.POST,request.FILES)
            else:                
                form = DriverForm()
                
            if form.is_valid():
                driver = form.save(commit = False)
                system = System.objects.get(pk=request.session['system'])
                driver.system = system
                driver.save()

                vehicles = form.cleaned_data['vehicle']
                for v in vehicles:
                    driver.vehicle.add(v)
                driver.save()
                return HttpResponseRedirect("/drivers/create/finish")

            return render_to_response("drivers/templates/create.html",locals(),context_instance=RequestContext(request))
        # else:
            # return HttpResponseForbidden(u"O seu sistema não pode criar motoristas para este veículo.")
    except ObjectDoesNotExist:
        return HttpResponseNotFound("O veículo solicitado não existe.") 
        
        
def create_finish(request):
    return render_to_response("drivers/templates/create_finish.html",locals())
    
def edit(request,offset):
    #checks if system can alter the driver vehicle
    try:
        # if request.session['system'] in map(lambda x: x['id'],Driver.objects.get(pk=int(offset)).vehicle.system.values()):
            
            d = Driver.objects.get(pk=int(offset))
            
            if request.method == "POST":
                form = DriverForm(request.POST,request.FILES, instance=d)
            else:
                form = DriverForm(instance=d)
                
            if form.is_valid():
                driver = form.save(commit = False)
                system = System.objects.get(pk=request.session['system'])
                driver.system = system
                driver.save()
                
                vehicles = form.cleaned_data['vehicle']
                for v in vehicles:
                    driver.vehicle.add(v)
                driver.save()
                return HttpResponseRedirect("/drivers/edit/finish")
    
            return render_to_response("drivers/templates/create.html",locals(),context_instance=RequestContext(request))
        # else:
            # ret urn HttpResponseForbidden(u"O seu sistema não pode editar motoristas para este veículo.")
    except ObjectDoesNotExist:
        return HttpResponseNotFound("O veículo solicitado não existe.") 
        
def edit_finish(request):
    return render_to_response("drivers/templates/edit_finish.html",locals())
    
def delete(request,offset):
    #checks if system can alter the vehicle's drivers
    try:
        # if request.session['system'] in map(lambda x: x['id'],Driver.objects.get(pk=int(offset)).vehicle.system.values()):
            
            d = Driver.objects.get(pk=int(offset))
            
            if request.method == "POST":
                d.delete()
                return HttpResponseRedirect("/drivers/delete/finish")
    
            return render_to_response("drivers/templates/delete.html",locals(),context_instance=RequestContext(request))
        # else:
            # return HttpResponseForbidden(u"O seu sistema não pode apagar motoristas para este veículo.")
    except ObjectDoesNotExist:
        return HttpResponseNotFound("O veículo solicitado não existe.") 
        
def delete_finish(request):
    return render_to_response("drivers/templates/delete_finish.html",locals())
