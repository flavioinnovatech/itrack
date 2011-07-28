# Create your views here.
from django.shortcuts import render_to_response
from itrack.system.models import System,Settings
from itrack.equipments.models import CustomField,Equipment,Tracking,TrackingData,EquipmentType
from itrack.geofence.models import Geofence
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.gis.geos.linestring import LineString
from querystring_parser import parser
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.gis import geos
from itrack.system.tools import findChild

def systemGeofenceDetails(sysid):
    lines = []
    system = System.objects.get(pk=sysid)
    geofences = Geofence.objects.filter(system=system)
    if system.parent == None:
        childof = None
    else:
        childof = system.parent.id
    lines.append({  'id':system.id,
                    'childof':childof,
                    'sysname':system.name,
                })
    for geofence in geofences:
        lines.append({  'id':geofence.id,
                        'childof':system.id,
                        'geofence':geofence.name,
                        'type':geofence.type,
                    })
    
    if geofences: 
        return lines    
    else: 
        return []

def mountGeofenceTree(list_of_childs,parent):
    table = []
    
    if type(list_of_childs).__name__ == 'list':
        if(len(list_of_childs) > 0):
            prev = list_of_childs[0]
            if type(prev).__name__ != 'list':
                lines = systemGeofenceDetails(prev)
                for line in lines:
                    table.append(line)
            else:
                pass
                
            for el in list_of_childs[1:]:
                
                if type(el).__name__ == 'list':
                    lines = mountGeofenceTree(el,prev)
                else:
                    lines = mountGeofenceTree(el,parent)
                
                for line in lines:
                    table.append(line)
                    
                prev = el
    
        return table
           
    else:
        return systemGeofenceDetails(list_of_childs)
    


def index(request):
    system_id = request.session['system']
        
    childs = findChild(system_id)
    geofence_tree = mountGeofenceTree([system_id,childs],system_id)
    
    return render_to_response("geofence/templates/index.html",locals())
    
def index2(request):
    system = System.objects.filter(administrator__username=request.user.username)

    return render_to_response("geofence/templates/multispectral.html",locals())
    
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
        
def saveGeofencev2(request):
  if request.method == "POST":
    parsed_dict = parser.parse(request.POST.urlencode())
    if parsed_dict['type'] == 'circle':
      print 'ae'
      
      system = System.objects.get(pk=request.session['system'])
      wkt = float(parsed_dict['coords'])
      
      return HttpResponse('success')
   
def loadGeofences(request):
  system = request.session["system"]
  geofence = Geofence.objects.filter(system=system)
  
  data = []
  
  for g in geofence:
    if g.type != 'R':
      data.append({"name":g.name,"id":g.id,"type":g.type,"polygon":g.polygon.coords})
    elif g.type == 'R':
      data.append({"name":g.name,"id":g.id,"type":g.type,"route":g.linestring.coords})
    
  print data
  json = simplejson.dumps(data)
  
  return HttpResponse(json, mimetype='application/json')
  
