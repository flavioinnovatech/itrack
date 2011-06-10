# -*- coding:utf8 -*-

from django.shortcuts import render_to_response
from itrack.system.models import System,Settings
from itrack.equipments.models import CustomField,Equipment,Tracking,TrackingData,EquipmentType
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import simplejson
from django.http import HttpResponse
from django.utils.encoding import smart_str

@login_required
def index(request):
  settings = Settings.objects.get(system=request.session["system"])
  if settings.map_google:
    map_google = 1
  if settings.map_maplink:
    map_maplink = 1
  if settings.map_multspectral:
    map_multispectral = 1
      
  return render_to_response("rastreamento/templates/rastreamento.html",locals())

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

  data = []
  for i in equips:
    tracking = Tracking.objects.filter(equipment=i).order_by('eventdate').reverse()[0]
    trackingData = TrackingData.objects.filter(tracking=tracking.id)
    for j in trackingData:
      type = CustomField.objects.get(pk=j.type_id)
      data.append({"type":smart_str(type, encoding='utf-8', strings_only=False, errors='strict'),"value":j.value})
  
  json = simplejson.dumps(data)
  print json
  return HttpResponse(json, mimetype='application/json')
  
  
# geofence test
def geofence(request):
  return render_to_response("templates/geofence.html",locals())
  
def systems(request,offset):

