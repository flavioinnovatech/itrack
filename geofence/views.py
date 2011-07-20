# Create your views here.
from django.shortcuts import render_to_response
from itrack.system.models import System,Settings
from itrack.equipments.models import CustomField,Equipment,Tracking,TrackingData,EquipmentType
from itrack.geofence.models import Geofence
from itrack.alerts.models import Alert
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.gis.geos.linestring import LineString
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
        
        center = geos.Point(float(parsed_dict['coords']['lng']),float(parsed_dict['coords']['lat']))
        
        radius = float(parsed_dict['coords']['radius'])
        
        circle = center.buffer(radius/1000/40000*360)

        circle = str(circle)[8:len(str(circle))]
        
        circle = "MULTIPOLYGON(" + circle + ")"
        
        print circle
                
        g = Geofence(name=parsed_dict['name'],system=system,type='C',polygon=circle)
        
        g.save()
      

        return HttpResponse(g.id)
        
    elif parsed_dict['type'] == 'polygon':
      
        system = System.objects.get(pk=request.session['system'])
        g = Geofence(name=parsed_dict['name'],system=system,type='P')
        
        str_coords =  parsed_dict['coords']['points'].replace("(","").split(")")
        coords = []

        wkt = "MULTIPOLYGON((("
        i = 0
        firstpoint = ""
        for coord in str_coords:
            if not coord == "":
                i = i+1
                arraytemp = coord.split(",")
                wkt += arraytemp[1]
                wkt += " "
                wkt += arraytemp[0]
                
                if i == 1:
                  firstpoint += arraytemp[1] + " " + arraytemp[0] 
                
                wkt += ","
        
        wkt += firstpoint
        wkt += ")))"
                
        print wkt
        
        g = Geofence(name=parsed_dict['name'],system=system,type='P',polygon=wkt)
        g.save()
        
        return HttpResponse(g.id)
    elif parsed_dict['type'] == 'route':
        system = System.objects.get(pk=request.session['system'])
        
        coords = parsed_dict['coords']
        line = coords[''][0] +','+ coords[''][1]

        wkt="LINESTRING("

        i = 0
        for point in coords['']:
          arraytemp = point.replace("(","").replace(")","").split(",")
          wkt += arraytemp[1]
          wkt += " "
          wkt += arraytemp[0]
          
          i=i+1
          if i != len(coords['']):
            wkt += ","

        wkt+=")"
        print wkt
        
        g = Geofence(name=parsed_dict['name'],system=system,type='R',linestring=wkt)
        g.save()
        
        return HttpResponse('qqrcoisa')
    else:
        pass
   
  #return render_to_response("alerts/templates/create.html",locals())
def loadGeofences(request):
  system = request.session["system"]
  geofence = Geofence.objects.filter(system=system)
  
  data = []
  
  for g in geofence:
    if g.type != 'R':
      data.append({"name":g.name,"id":g.id,"type":g.type,"polygon":g.polygon.coords})
    elif g.type == 'R':
      data.append({"name":g.name,"id":g.id,"type":g.type,"route":g.linestring.coords})
    # if g.type == 'C':
      # geoentities = GeoEntity.objects.filter(geofence=g)
      # for ge in geoentities:
      #         coords = {"radius":ge.radius,"lat":ge.lat,"lng":ge.lng}
      #         data.append({"name":g.name,"id":g.id,"type":g.type,"coords":coords})
      #         
      #     if g.type == 'P':
      # geoentities = # GeoEntity.objects.filter(geofence=g).order_by('seq')
      # coords = []
      # for ge in geoentities:
        # coord = {"lat":ge.lat,"lng":ge.lng}
        # coords.append(coord)
        
      # data.append({"name":g.name,"id":g.id,"type":g.type,"coords":coords})
        
  # data.append({ "name" : g.name, "type": g.type })
  # data.append({ "name" : "g.name", "type": "g.type" })
  print data
  json = simplejson.dumps(data)
  
  return HttpResponse(json, mimetype='application/json')
  
