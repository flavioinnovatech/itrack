# -*- coding:utf8 -*-

from django.shortcuts import render_to_response
from itrack.system.models import System,Settings
from itrack.equipments.models import CustomField,Equipment,Tracking,TrackingData,EquipmentType,CustomFieldName,AvailableFields
from itrack.rastreamento.forms import ConfigForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.context import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.utils.encoding import smart_str
from itrack.vehicles.models import Vehicle
from itrack.system.tools import lowestDepth
import pprint
from querystring_parser import parser


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

@login_required  
def loadData(request):
    
  if request.method == 'POST':  
    parsed_dict = parser.parse(request.POST.urlencode())
  
  #print parsed_dict['plate']
    
  system = request.session["system"]
  equips = Equipment.objects.filter(system=system)
  v_set = []
  
  for e in equips:
    try:
        v_set.append(Vehicle.objects.get(equipment=e.id).id)
    except:
        print "Veículo não encontrado."
        
  if parsed_dict.has_key('plate'):

      vehicles = Vehicle.objects.filter(id__in=v_set).filter(system=system).filter(license_plate__icontains=parsed_dict['plate'])
      print vehicles
      
  else:
    vehicles = Vehicle.objects.filter(id__in=v_set).filter(system=system)
    
  available_fields = CustomFieldName.objects.filter(
    system = request.session["system"]).filter(
        custom_field__availablefields__system = request.session["system"]).distinct().filter(
        custom_field__system = request.session["system"]).order_by('name')
        
  #vehicle_fields = 
  
  data = {}
  
  for i in vehicles:
    info = {}
    info["id"] = i.id
    info["hora"] = {}
    info["veiculo"] = {}
    info["info"] = {}
    info["geocode"] = {}
    tracking = Tracking.objects.filter(equipment=i.equipment.id).order_by('eventdate').reverse()[0]
    trackingData = TrackingData.objects.filter(tracking=tracking.id)
    info["hora"]["eventdate"] = smart_str(tracking.eventdate, encoding='utf-8', strings_only=False, errors='strict')
    info["veiculo"]["Chassi"] = i.chassi
    info["veiculo"]["license_plate"] = i.license_plate
    info["veiculo"]["Cor"] = i.color
    info["veiculo"]["Ano de fabricação"] = i.year
    info["veiculo"]["Modelo"] = i.model
    info["veiculo"]["Fabricante"] = i.manufacturer
    info["veiculo"]["type"] = i.type
    info["veiculo"]["sistema"] = lowestDepth(i.equipment.system.all()).name
    
        
    for j in trackingData:
      try:
        if j.type.tag == 'Lat':
          info["lat"] = j.value
        if j.type.tag == 'Long':
          info["lng"] = j.value  
        cfn = CustomFieldName.objects.filter(system=system).get(custom_field=j.type)
        if cfn.custom_field in CustomField.objects.filter(system=system):
            info["info"][smart_str(cfn.name, encoding='utf-8', strings_only=False, errors='strict')] = j.value          
      except:
        if j.type.type == "GPS" or j.type.type == "Geocode":
            info["geocode"][smart_str(j.type.name, encoding='utf-8', strings_only=False, errors='strict')] = j.value
        pass
    
    fields_list = [x.name for x in available_fields.distinct()]
    items = info["info"].keys()
    
    
    # this mapping adds items that are OFF but should be displayed 
    # saved in the configs and is present on the equip type
    #map(lambda k: k not in items and info["info"].setdefault(k,"OFF"),fields_list)
    
    print info["info"]
    
    #for field in fields_list:
    #    if field not in items:
            
        
           
    data[tracking.equipment.serial] =  info
    
       
  json = simplejson.dumps(data)

  return HttpResponse(json, mimetype='application/json')


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
    


