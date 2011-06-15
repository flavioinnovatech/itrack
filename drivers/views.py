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


def index(request,offset):
    #checks if system can alter the vehicle's drivers
    try:
        if request.session['system'] in map(lambda x: x['id'],Vehicle.objects.get(pk=int(offset)).system.values()):
            drivers = Driver.objects.filter(vehicle = int(offset))
            rendered_list = {}
            for d in drivers:
                rendered_list[d.id] = { 'identification':d.identification,
                                        'name':d.name,
                                        'telephone1':d.telephone1,
                                        'telephone2':d.telephone2,
                                        'vehicle':d.vehicle,
                                        'photo':d.photo,
                                        'address':d.address
                                      }
        
            return render_to_response("drivers/templates/index.html",locals(),context_instance=RequestContext(request))
        else:
            return HttpResponseForbidden(u"O seu sistema não pode alterar o veículo solicitado.")
    except ObjectDoesNotExist:
        return HttpResponseNotFound("O veículo solicitado não existe.")     

def profile(request,offset):
    #checks if system can alter the vehicle's drivers
    if request.session['system'] in map(lambda x: x['id'],Driver.objects.get(pk=int(offset)).vehicle.system.values()):
        
        driver = Driver.objects.get(pk=int(offset))
        
        return render_to_response("drivers/templates/profile.html",locals(),context_instance=RequestContext(request))
    
    
    else:
        return HttpResponseForbidden(u"O seu sistema não pode visualizar motoristas deste veículo.")

def create(request,offset):
    #checks if system can alter the vehicle's drivers
    try:
        if request.session['system'] in map(lambda x: x['id'],Vehicle.objects.get(pk=int(offset)).system.values()):
            if request.method == "POST":
                form = DriverForm(request.POST,request.FILES)
            else:                
                form = DriverForm()
                
            if form.is_valid():
                driver = form.save(commit = False)
                driver.vehicle = Vehicle.objects.get(pk=int(offset))
                driver.save()
                return HttpResponseRedirect("/drivers/create/finish")

            return render_to_response("drivers/templates/create.html",locals(),context_instance=RequestContext(request))
        else:
            return HttpResponseForbidden(u"O seu sistema não pode criar motoristas para este veículo.")
    except ObjectDoesNotExist:
        return HttpResponseNotFound("O veículo solicitado não existe.") 
        
        
def create_finish(request):
    return HttpResponse("Create_finish")
    
def edit(request,offset):
    #checks if system can alter the driver vehicle
    try:
        if request.session['system'] in map(lambda x: x['id'],Driver.objects.get(pk=int(offset)).vehicle.system.values()):
            
            d = Driver.objects.get(pk=int(offset))
            
            if request.method == "POST":
                form = DriverForm(request.POST,request.FILES, instance=d)
            else:
                form = DriverForm(instance=d)
                
            if form.is_valid():
                driver = form.save(commit = False)
                driver.vehicle = Vehicle.objects.get(pk=int(offset))
                driver.save()
                return HttpResponseRedirect("/drivers/edit/finish")
    
            return render_to_response("drivers/templates/create.html",locals(),context_instance=RequestContext(request))
        else:
            return HttpResponseForbidden(u"O seu sistema não pode editar motoristas para este veículo.")
    except ObjectDoesNotExist:
        return HttpResponseNotFound("O veículo solicitado não existe.") 
        
def edit_finish(request):
    return HttpResponse("Edit_finish")
    
def delete(request,offset):
    #checks if system can alter the vehicle's drivers
    try:
        if request.session['system'] in map(lambda x: x['id'],Driver.objects.get(pk=int(offset)).vehicle.system.values()):
            
            d = Driver.objects.get(pk=int(offset))
            
            if request.method == "POST":
                d.delete()
                return HttpResponseRedirect("/drivers/delete/finish")
    
            return render_to_response("drivers/templates/delete.html",locals(),context_instance=RequestContext(request))
        else:
            return HttpResponseForbidden(u"O seu sistema não pode apagar motoristas para este veículo.")
    except ObjectDoesNotExist:
        return HttpResponseNotFound("O veículo solicitado não existe.") 
        
def delete_finish(request):
    return HttpResponse("Delete_finish")