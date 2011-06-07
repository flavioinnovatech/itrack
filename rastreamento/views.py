from django.shortcuts import render_to_response
from itrack.system.models import System,Settings
from itrack.equipments.models import CustomField,Equipment,Tracking,TrackingData,EquipmentType
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def index(request):
  settings = Settings.objects.get(system=request.session["system"])
  if settings.map_google:
    map_google = 1
  if settings.map_maplink:
    map_maplink = 1
  if settings.map_multspectral:
    map_multispectral = 1
    
  system = request.session["system"]
  equips = Equipment.objects.filter(system=system)

  for item in equips:
    equiptype = EquipmentType.objects.filter(name=item.type)
    print equiptype
    
  return render_to_response("rastreamento/templates/rastreamento.html",locals())
  
# geofence test
def geofence(request):
  return render_to_response("templates/geofence.html",locals())
  
def systems(request,offset):

