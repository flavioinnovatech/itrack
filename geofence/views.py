# Create your views here.
from django.shortcuts import render_to_response
from itrack.system.models import System,Settings
from itrack.equipments.models import CustomField,Equipment,Tracking,TrackingData,EquipmentType
from django.contrib.auth.decorators import login_required, user_passes_test
from querystring_parser import parser
from itrack.geofence.models import GeoEntity,Geofence
from django.http import HttpResponse

def index(request):
    parent = []
    system = System.objects.filter(administrator__username=request.user.username)
    for item in system:
        parent = item.id
    vector = []
    if parent != []:
        childs = findChild(parent)
        vector.append(parent)
        vector.append(childs)
        
        vector_html = render_system_html2(childs)
        
    return render_to_response("system/templates/home.html",locals())
    
def saveGeofence(request):
  if request.method == "POST":
    parsed_dict = parser.parse(request.POST.urlencode())
    if parsed_dict['type'] == 'circle':
        p1 = GeoEntity(geofence=None,lat = float(parsed_dict['coords']['lat']), lng = float(parsed_dict['coords']['lng']), radius = float(parsed_dict['coords']['radius']))
        p1.save()
        return HttpResponse(p1.id)
        pass
    elif parsed_dict['type'] == 'polygon':
        pass
    elif parsed_dict['type'] == 'route':
        pass
    else:
        pass
   
  #return render_to_response("alerts/templates/create.html",locals())
