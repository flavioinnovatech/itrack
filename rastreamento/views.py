# -*- coding:utf8 -*-

from django.shortcuts import render_to_response
from itrack.system.models import System,Settings
from itrack.equipments.models import CustomField,Equipment,Tracking,TrackingData,EquipmentType,CustomFieldName
from itrack.rastreamento.forms import ConfigForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.context import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.utils.encoding import smart_str
from itrack.vehicles.models import Vehicle
import pprint


@login_required
def index(request):
  settings = Settings.objects.get(system=request.session["system"])
  if settings.map_google:
    map_google = 1
  if settings.map_maplink:
    map_maplink = 1
  if settings.map_multspectral:
    map_multispectral = 1
  
  form = ConfigForm()
  form.fields["custom_names"].queryset = CustomFieldName.objects.filter(system = request.session["system"]).filter(custom_field__availablefields__system = request.session["system"]).distinct()
  form.fields["vehicles"].queryset = Vehicle.objects.filter(equipment__system = request.session["system"])
  form.fields["custom_names"].initial = CustomFieldName.objects.filter(custom_field__system = request.session["system"])
  form.fields["vehicles"].initial = Vehicle.objects.filter(system = request.session["system"])
  return render_to_response("rastreamento/templates/rastreamento.html",locals(),context_instance=RequestContext(request),)

#TO-DO: needs permission here
def loadCustomFields(request):
  system = request.session["system"]
  equips = Equipment.objects.filter(system=system)

  customFields = []
  
  for i in equips:
    equiptype = EquipmentType.objects.filter(name=i.type)
    for k in equiptype:
      customfields = CustomField.objects.filter(equipmenttype=k)
      for j in customfields:
          customFields.append(j.name)
  
  json = simplejson.dumps(customFields)
  return HttpResponse(json, mimetype='application/json')
  
def loadData(request):
  system = request.session["system"]
  equips = Equipment.objects.filter(system=system)
  v_set = []
  
  for e in equips:
    try:
        v_set.append(Vehicle.objects.get(equipment=e.id).id)
    except:
        print "Veículo não encontrado."
        
  vehicles = Vehicle.objects.filter(id__in=v_set).filter(system=system)


  #data needs vehicle identification here
  data = {}
  for i in vehicles:
    info = {}
    info["hora"] = {}
    info["veiculo"] = {}
    info["info"] = {}
    tracking = Tracking.objects.filter(equipment=i.equipment.id).order_by('eventdate').reverse()[0]
    trackingData = TrackingData.objects.filter(tracking=tracking.id)
    info["hora"]["eventdate"] = smart_str(tracking.eventdate, encoding='utf-8', strings_only=False, errors='strict')
    info["veiculo"]["chassi"] = i.chassi
    info["veiculo"]["license plate"] = i.license_plate
    info["veiculo"]["color"] = i.color
    info["veiculo"]["year"] = i.year
    info["veiculo"]["model"] = i.model
    info["veiculo"]["manufacturer"] = i.manufacturer
    info["veiculo"]["type"] = i.type
    for j in trackingData:
      try:
        cfn = CustomFieldName.objects.filter(system=system).get(custom_field=j.type)
        if cfn.custom_field in CustomField.objects.filter(system=system):
            info["info"][smart_str(cfn.name, encoding='utf-8', strings_only=False, errors='strict')] = j.value
      except:
        pass
            
    data[tracking.equipment.serial] =  info
       
    print data 

  json = simplejson.dumps(data)

  return HttpResponse(json, mimetype='application/json')
  
  
# geofence test
def geofence(request):
  return render_to_response("templates/geofence.html",locals())

def xhr_test(request):
    
    if request.method == "POST":
        #form = ConfigForm(request.POST)
        #if form.is_valid():
        #    for field in form.cleaned_data:
        #        print field
        
        v_set = Vehicle.objects.filter(system = request.session["system"])
        for v in v_set:
            v.system.remove(request.session["system"])
        
        cf_set = CustomField.objects.filter(system = request.session["system"])
        for cf in cf_set:
            cf.system.remove(request.session["system"])
        
        try:
            vehicles = request.POST.getlist(u"vehicles[]")
            for vehicle in vehicles:
                v = Vehicle.objects.get(pk=int(vehicle))
                v.system.add(request.session["system"])
        except:
            pass
        try:
            custom_names = request.POST.getlist(u"custom_names[]")
            for name in custom_names:
                cf = CustomFieldName.objects.get(pk=int(name)).custom_field
                cf.system.add(int(request.session["system"]))
        except:
            pass
            

        
    else:
        form = ConfigForm()
        return render_to_response("rastreamento/templates/form.html",locals(),context_instance=RequestContext(request),) 

    return render_to_response("rastreamento/templates/form.html",locals(),context_instance=RequestContext(request),)    
    

