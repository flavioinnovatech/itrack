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
from django.db.models import Q,Max
from itrack.vehicles.models import Vehicle
from itrack.system.tools import lowestDepth
from querystring_parser import parser
import time
import json as Json
import itertools
from datetime import datetime


@login_required
def index(request):
  
  form = ConfigForm()
  form.fields["custom_names"].queryset = CustomFieldName.objects.filter(system = request.session["system"]).filter(custom_field__availablefields__system = request.session["system"]).distinct()
  form.fields["vehicles"].queryset = Vehicle.objects.filter(equipment__system = request.session["system"])
  form.fields["custom_names"].initial = CustomFieldName.objects.filter(custom_field__system = request.session["system"])
  form.fields["vehicles"].initial = Vehicle.objects.filter(system = request.session["system"])
  return render_to_response("rastreamento/templates/rastreamento.html",locals(),context_instance=RequestContext(request),)

@login_required  
def loadData(request):
  _loaddata_count0 = 0
  if request.method == 'POST':  
    d1=datetime.now()
    parsed_dict = parser.parse(request.POST.urlencode())
    system = request.session["system"]
    #getting the last tracking of the selected equipments
    if parsed_dict.has_key('plate'):
        equipments = Equipment.objects.filter(
            Q(vehicle__license_plate__icontains=parsed_dict['plate'])&
            Q(system=system)&
            Q(vehicle__system=system)
        ).annotate(last_tracking=Max('tracking__id'))
        print 'aiudhauidhuiad'
    else:
        equipments = Equipment.objects.filter(
            Q(system=system)&
            Q(vehicle__system=system)
        ).annotate(last_tracking=Max('tracking__id'))
    
    #mounting the dict of trackings and it's tracking datas.     
    tdata_dict = {}
    vehicle_dict = {}
    tracking_dict = {}
    system_list={}
    field_list={}
    
    trackings = [e.last_tracking for e 
                        in equipments 
                        if e.last_tracking is not None]
    
    equips_id = [e.id for e 
                        in equipments 
                        if e.last_tracking is not None]
    
    
    data = TrackingData.objects.select_related(depth=2).filter(
            tracking__id__in=trackings).order_by('tracking__id').iterator()
        
    vehicles = Vehicle.objects.select_related('equipment').filter(
            equipment__in=equips_id).iterator()   
    
    systems = System.objects.select_related(depth=1).all().iterator()
    customnames = CustomFieldName.objects.select_related(depth=1).filter(
            Q(system=system)&
            Q(custom_field__system=system)).distinct()
    
    
    #data TrackingData[]
    for tdata in itertools.chain(data):
        tdata_dict.setdefault(tdata.tracking, []).append(tdata)
    #tdata_dict TrackingData{Tracking}
    
    #vehicle Vehicles[]
    for vehicle in itertools.chain(vehicles):
        vehicle_dict.setdefault(vehicle.equipment, vehicle)
    #vehicle_dict = Vehicle{Equipment}
    
    for tracking,data_list in itertools.chain(tdata_dict.items()):
        data_list.append(vehicle_dict[tracking.equipment])
    #data_list = Vehicle[]
    
    for system in systems:
        system_list.setdefault(system.id,system)
    #system_list = System{System.id}
       
    for name in customnames:
        field_list.setdefault(name.custom_field.id,name.name)
    #field_list = string:CustomFieldName.name{CustomField.id}
    
    
    # now we have a dict that looks like this:
    # { ...
    #   ...
    #   <Tracking>:[<TrackingData>,<TrackingData>, ...,<TrackingData>,<Vehicle>]   
    #   ... 
    #   ... }
    #
    # and we are going to iterate over it, mounting the json output.
       
    json_output = {}
    
    for tracking, data_list in itertools.chain(tdata_dict.items()):
        vehicle = data_list.pop()        
        info = {}
        info["id"] = vehicle.id
        info["hora"] = {}
        info["veiculo"] = {}
        info["info"] = {}
        info["geocode"] = {}
        info["geocode"][smart_str("Endereço", encoding='utf-8', strings_only=False, errors='strict')]=""
        info["hora"]["eventdate"] = smart_str(tracking.eventdate, encoding='utf-8', strings_only=False, errors='strict')

        info["veiculo"]["Chassi"] = vehicle.chassi
        info["veiculo"]["license_plate"] = vehicle.license_plate
        info["veiculo"]["Cor"] = vehicle.color
        info["veiculo"]["Ano de fabricação"] = vehicle.year
        info["veiculo"]["Modelo"] = vehicle.model
        info["veiculo"]["Fabricante"] = vehicle.manufacturer
        info["veiculo"]["type"] = vehicle.type
        
        try:
            sysid = int([x.value for x in data_list if x.type.tag=='System'][0])
            info["veiculo"]["sistema"] = smart_str(system_list[sysid], encoding='utf-8', strings_only=False, errors='strict')
        except:
            info["veiculo"]["sistema"] = smart_str(system_list[2], encoding='utf-8', strings_only=False, errors='strict')
        
        for j in data_list:
            if j.type.type == "Geocode":
                info["geocode"][smart_str(j.type.name, encoding='utf-8', strings_only=False, errors='strict')] = j.value
        for j in data_list:
            if j.type.tag == 'Lat':
              info["lat"] = j.value
            elif j.type.tag == 'Long':
              info["lng"] = j.value  
            elif field_list.has_key(j.type.id):
                info["info"][smart_str(field_list[j.type.id], encoding='utf-8', strings_only=False, errors='strict')] = j.value          

            
        json_output[vehicle.license_plate]=info
    
    json_output = simplejson.dumps(json_output)
    
    return HttpResponse(json_output, mimetype='application/json')
    
    

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
    



