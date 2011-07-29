from django.http import HttpResponse
from querystring_parser import parser
from django.utils import simplejson
from django.db.models import Q

from paths.forms import PathForm
from equipments.models import Tracking, TrackingData,Equipment
from geofence.models import Geofence
from datetime import datetime

def load(request):
    parsed_POST = parser.parse(request.POST.urlencode())
    form = PathForm(request.session['system'],parsed_POST)
    if form.is_valid():
    
        # getting the path points and mounting the multidimensional list
        equipment = Equipment.objects.get(vehicle=form.cleaned_data['vehicle'])
        d1 = datetime.now()
        trackings = Tracking.objects.filter(Q(equipment=equipment) & Q(eventdate__gte=form.cleaned_data['period_start']) & Q(eventdate__lte=form.cleaned_data['period_end']))
        datas = TrackingData.objects.select_related('tracking').filter(Q(tracking__in=trackings) & (Q(type__tag='Lat')|Q(type__tag='Long')))
        print (datetime.now() - d1).total_seconds()
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
