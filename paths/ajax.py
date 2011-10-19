from datetime import datetime

from django.http import HttpResponse
from querystring_parser import parser
from django.utils import simplejson
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from paths.forms import PathForm
from equipments.models import Tracking, TrackingData,Equipment
from vehicles.models import Vehicle
from geofence.models import Geofence
from system.tools import lowestDepth,findParents
from system.models import System

import math


def geoDistance(lat1,lon1,lat2,lon2):

    dla1 = math.floor(lat1)
    mla1 = math.floor(((lat1)-dla1)*60)
    sla1 = math.floor( ( ((lat1-dla1)*60) - mla1 )*60 )
    
    #    print("LA1 # " + str(dla1) + ":" + str(mla1) + ":" + str(sla1))
    
    
    dlo1 = math.floor(lon1)
    mlo1 = math.floor(((lon1)-dlo1)*60)
    slo1 = math.floor( ( ((lon1-dlo1)*60) - mlo1 )*60 )
    
    #    print("LO1 # " + str(dlo1) + ":" + str(mlo1) + ":" + str(slo1))
    
    dla2 = math.floor(lat2)
    mla2 = math.floor(((lat2)-dla2)*60)
    sla2 = math.floor( ( ((lat2-dla2)*60) - mla2 )*60 )
    
    #    print("LA2 # " + str(dla2) + ":" + str(mla2) + ":" + str(sla2))
    
    dlo2 = math.floor(lon2)
    mlo2 = math.floor(((lon2)-dlo2)*60)
    slo2 = math.floor( ( ((lon2-dlo2)*60) - mlo2 )*60 )
    
    #    print("LO2 # " + str(dlo2) + ":" + str(mlo2) + ":" + str(slo2))
    
    
    lat1 = dla1 + mla1/60 + sla1/3600
    lon1 = dlo1 + mlo1/60 + slo1/3600
    lat2 = dla2 + mla2/60 + sla2/3600
    lon2 = dlo2 + mlo2/60 + slo2/3600
    
    
    #padronizado
    
    rad_lat1 = (lat1)*math.pi/180
    rad_lon1 = (lon1)*math.pi/180
    
    rad_lat2 = (lat2)*math.pi/180
    rad_lon2 = (lon2)*math.pi/180
     
     
    dlat = rad_lat2 - rad_lat1
    dlon = rad_lon2 - rad_lon1
    
    #    print("dLat:" + str(dlat))
    #    print("dLon:" + str(dlon))
    
    a1 = math.sin(dlat/2)*math.sin(dlat/2)
    a2 = math.cos(lat1)*math.cos(lat2)
    a3 = math.sin(dlon/2)*math.sin(dlon/2)
    a = a1 + a2 * a3
    
    #    print("A:" + str(a))
        
    # verify this
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    
    #    print("C:" + str(c))
    
    
    d = 6371 *c # (Raio da terra) * c
        
    #    print("D:" + str(d))
    
    #    print("-----------------------------------")

    return d
def load(request):
    parsed_POST = parser.parse(request.POST.urlencode())
    try:
        if parsed_POST.has_key("vehicle_other"):
            
            v = Vehicle.objects.get(license_plate=request.POST["vehicle"])
            parsed_POST["vehicle"] = str(v.id)
    except ObjectDoesNotExist:
        pass
    
    print parsed_POST
    form = PathForm(request.session['system'],parsed_POST)
    if form.is_valid():
        system = request.session["system"]
        s = System.objects.get(pk=system)
        parents = findParents(s,[s])
        
        # getting the path points and mounting the multidimensional list
        #print form.cleaned_data['vehicle']
        vehicle = Vehicle.objects.get(pk=form.cleaned_data["vehicle"])
        d1 = datetime.now()
        
        #trackings = Tracking.objects.filter(Q(equipment=equipment) & Q(eventdate__gte=form.cleaned_data['period_start']) & Q(eventdate__lte=form.cleaned_data['period_end']))
                
        if s.parent == None:
            trackings = Tracking.objects.filter(
                Q(eventdate__gte=form.cleaned_data['period_start'])  
                &Q(eventdate__lte=form.cleaned_data['period_end'])
                &(
                    Q(trackingdata__type__type = 'Vehicle')
                    &Q(trackingdata__value = vehicle.id)
                )
            )
        else:
            trackings = Tracking.objects.filter(
                Q(eventdate__gte=form.cleaned_data['period_start'])  
                &Q(eventdate__lte=form.cleaned_data['period_end'])
                &(
                    Q(trackingdata__type__type = 'Vehicle')
                    &Q(trackingdata__value = vehicle.id)
                )
                &(
                    Q(trackingdata__type__type = 'System')
                    &Q(trackingdata__value__in = parents)
                )
            )
        print trackings
            
        datas = TrackingData.objects.select_related('tracking').filter(Q(tracking__in=trackings) & (Q(type__tag='Lat')|Q(type__tag='Long')))
        
        tdata_dict = {}
        for tdata in datas:
            tdata_dict.setdefault(str(tdata.tracking.eventdate), []).append(tdata)
            
        tdata_dk = tdata_dict.keys()
        tdata_dk.sort()
        
        
        geodist_started = False
        geodist_total = 0
        geodist_last_lat = 0
        geodist_last_lon = 0
        try:
            for date in tdata_dk:
                tdata = tdata_dict[date]
                geodist_state = 0
                geodist_cur_lat = 0
                geodist_cur_lon = 0
                
                for y in tdata:
                    if y.type.name == "Longitude":
                        #print(unicode(y.type.name) +  " :: " + unicode(y.value))
                        geodist_cur_lon = y.value
                        geodist_state += 1
                    elif y.type.name == "Latitude":
                        #print(unicode(y.type.name) +  " :: " + unicode(y.value))
                        geodist_cur_lat = y.value
                        geodist_state += 1000
                if geodist_started:

                    if ((geodist_state / 1000) >= 1) and ((geodist_state - math.floor(geodist_state/1000)) >= 1):
                        try:
                            geodist_plus = geoDistance(float(geodist_last_lat),float(geodist_last_lon),float(geodist_cur_lat),float(geodist_cur_lon))
                            #print( getLabel(geodist_last_lat,geodist_last_lon) )
                            if geodist_plus > 0.1 :
                                geodist_total += geodist_plus
                                geodist_last_lat = geodist_cur_lat
                                geodist_last_lon = geodist_cur_lon
                        except Exception as err:
                            raise err
                    #print("after:" + str(geodist_total))
                else:
                    if ((geodist_state / 1000) >= 1) and ((geodist_state - math.floor(geodist_state/1000)) >= 1):
                        geodist_started = True
                        geodist_last_lat = geodist_cur_lat
                        geodist_last_lon = geodist_cur_lon
        except Exception as err:
            print(err.args)
            
        #getting the geofence points and mounting the list
        geofence = form.cleaned_data['geofence']
        geofencedata = {}
        if geofence:
            if geofence.type == 'R':
                geofencedata = {'type': geofence.type, 'coords': str(geofence.linestring)}
            else:
                geofencedata = {'type': geofence.type, 'coords': str(geofence.polygon)}
        
        print geofencedata
        #mounting the json list
        pathdata = {}
        for key,value in tdata_dict.items():
            try:
                pathdata[key]= (value[1].value,value[0].value)
            except:
                pass    

        json = simplejson.dumps([pathdata,geofencedata,{"distance":geodist_total}])
    return HttpResponse(json, mimetype='application/json')
