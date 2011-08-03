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
                pathdata[key]= (value[0].value,value[1].value)
            except:
                pass    

        json = simplejson.dumps([pathdata,geofencedata])
    return HttpResponse(json, mimetype='application/json')
