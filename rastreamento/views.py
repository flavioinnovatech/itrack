# -*- coding:utf8 -*-

from django.shortcuts import render_to_response
from itrack.system.models import System,Settings
from itrack.equipments.models import CustomField,Equipment,Tracking,TrackingData,EquipmentType
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
        
  vehicles = Vehicle.objects.filter(id__in=v_set)


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
      info["info"][smart_str(j.type.name, encoding='utf-8', strings_only=False, errors='strict')] = j.value
    data[tracking.equipment.serial] =  info

  pp = pprint.PrettyPrinter(indent=4)
  pp.pprint(data)

  json = simplejson.dumps(data)

  return HttpResponse(json, mimetype='application/json')
  
  
# geofence test
def geofence(request):
  return render_to_response("templates/geofence.html",locals())

def xhr_test(request):
    
    if request.method == "POST":
        pass
    else:
        form = ConfigForm()
        return render_to_response("rastreamento/templates/form.html",locals(),context_instance=RequestContext(request),) 
    print form.__dict__
    return render_to_response("rastreamento/templates/form.html",locals(),context_instance=RequestContext(request),)    
    

