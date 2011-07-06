# Create your views here.
from django.shortcuts import render_to_response
from itrack.system.models import System,Settings
from itrack.equipments.models import CustomField,Equipment,Tracking,TrackingData,EquipmentType
from itrack.geofence.models import GeoEntity,Geofence
from itrack.alerts.models import Alert
from django.contrib.auth.decorators import login_required, user_passes_test
from querystring_parser import parser
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.gis import geos

def index(request):
    system = System.objects.filter(administrator__username=request.user.username)

        
    return render_to_response("geofence/templates/home.html",locals())
    
def saveGeofence(request):
  if request.method == "POST":
    parsed_dict = parser.parse(request.POST.urlencode())
    if parsed_dict['type'] == 'circle':

        system = System.objects.get(pk=request.session['system'])
        
        center = geos.Point(float(parsed_dict['coords']['lat']), float(parsed_dict['coords']['lng']))
        
        radius = float(parsed_dict['coords']['radius'])
        
        circle = center.buffer(radius)
        
        print circle
        
        
        # Save geofence first
        # g = Geofence(name=parsed_dict['name'],system=system,type='C')
        # g.save()

        # Links GeoEntity with the previous created Geofence
        # p1 = GeoEntity(geofence=g,lat = float(parsed_dict['coords']['lat']), lng = float(parsed_dict['coords']['lng']), radius = float(parsed_dict['coords']['radius']))
            
        # p1.save()
        return HttpResponse("p1.id")
    elif parsed_dict['type'] == 'polygon':
      
        system = System.objects.get(pk=request.session['system'])
        g = Geofence(name=parsed_dict['name'],system=system,type='P')
        g.save()
        
        str_coords =  parsed_dict['coords']['points'].replace("(","").split(")")
        coords = []

        wkt = "POLYGON(("
        i = 0
        for coord in str_coords:
            if not coord == "":
                i = i+1
                wkt += coord.replace(","," ")
                if i != len(str_coords) - 1:
                  wkt += ","
                
        wkt += "))"
        
        print wkt 
        
        # list_ids = []
        #         sequence = 0
        #         for ent in coords:
            # p = GeoEntity(geofence=g,lat=float(ent[0]),lng=float(ent[1]),radius=0,seq=sequence)
            # sequence += 1
            # p.save()
            # list_ids.append(p.id)

        # for id in list_ids:
            # str_ids+=str(id)+","
        
        # print str_ids
        
        return HttpResponse(str_ids)
    elif parsed_dict['type'] == 'route':
        pass
    else:
        pass
   
  #return render_to_response("alerts/templates/create.html",locals())
def loadGeofences(request):
  system = request.session["system"]
  geofence = Geofence.objects.filter(system=system)
  
  data = []
  
  for g in geofence:
    
    if g.type == 'C':
      geoentities = GeoEntity.objects.filter(geofence=g)
      for ge in geoentities:
        coords = {"radius":ge.radius,"lat":ge.lat,"lng":ge.lng}
        data.append({"name":g.name,"id":g.id,"type":g.type,"coords":coords})
        
    if g.type == 'P':
      geoentities = GeoEntity.objects.filter(geofence=g).order_by('seq')
      coords = []
      for ge in geoentities:
        coord = {"lat":ge.lat,"lng":ge.lng}
        coords.append(coord)
        
      data.append({"name":g.name,"id":g.id,"type":g.type,"coords":coords})
        
  # data.append({ "name" : g.name, "type": g.type })
  # data.append({ "name" : "g.name", "type": "g.type" })
  print data
  json = simplejson.dumps(data)
  
  return HttpResponse(json, mimetype='application/json')
  