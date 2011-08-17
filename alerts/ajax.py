# -*- coding:utf8 -*-
from django.db.models import Q
from django.http import HttpResponse
from querystring_parser import parser
from itrack.alerts.models import Popup,Alert
from django.contrib.auth.models import User
from itrack.accounts.models import UserProfile
from itrack.system.models import System
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from itrack.system.tools import lowestDepth
from django.contrib.auth.decorators import login_required
from querystring_parser import parser
from django.utils import simplejson
from itrack.equipments.models import CustomFieldName,TrackingData
from django.utils.encoding import smart_str
from itrack.geofence.models import Geofence


@login_required
def status(request):
    if request.method == 'POST':
        # gets the system
        user = parser.parse(request.POST.urlencode())['user']
        
        #checks if there's a popup for this system
        popups_list = Popup.objects.filter(Q(user = user))
        for popup in popups_list:
            systemname = lowestDepth(popup.vehicle.equipment.system.all())
            
            systems = System.objects.filter(name=systemname)
            
            for sys in systems:
              admins = User.objects.filter(username=sys.administrator)
              
            for admin in admins:
              adminemail = admin.email
              adminname = admin.first_name
              adminprofiles = UserProfile.objects.filter(profile = admin.id)
              
            for adminprofile in adminprofiles:
              admincelular = adminprofile.cellphone
            
            data = {}

            for popup in popups_list:
               
               #TODO: otimization could be done, doing only one query on the database, but...
               geocs = TrackingData.objects.filter(
                    Q(tracking__eventdate=popup.date)
                    &Q(type__type='Geocode')
               )
               geodict = {}
               for field in geocs:
                   geodict[field.type.tag] = field.value
                                 
               print geodict
               
               
               data[popup.id] = {
                'name': popup.alert.name, 
                'date': popup.date, 
                'trigger': popup.alert.trigger, 
                'plate': popup.vehicle.license_plate, 
                'limit':popup.alert.linear_limit, 
                'state':popup.alert.state, 
                'system': systemname.name, 
                'adminemail': adminemail,
                'admincelular':admincelular,
                'adminname':adminname,
                'vehicle_id':popup.vehicle.id, 
                'system_id':systemname.id,
                'address': geodict['Address']+"-"+geodict['City']+", "+geodict['State']+" - "+geodict['PostalCode'],
               }
               
               #data[popup.id].setdefault()
                       
            numalerts = len(data)
         
            Popup.objects.filter(Q(user = user)).delete()
                
        return render_to_response("alerts/templates/status.html",locals(),context_instance=RequestContext(request))

    else:
       return HttpResponse("fail") 

@login_required       
def load(request):

 parsed_dict = parser.parse(request.POST.urlencode())

 a = Alert.objects.get(pk=parsed_dict['id'])
 
 c = CustomFieldName.objects.get(pk=a.trigger_id)
 
 vehicles = a.vehicle.all()
 
 send = {}
 
 v_array = []
 
 for v in vehicles:
   v_array.append(v.license_plate)
 
 v_string = ', '.join(v_array)
 
 send['vehicles'] = v_string
 
 dests = a.destinataries.all()
 
 d_array = []
 
 for d in dests:
   d_array.append(d.username)
   
 d_string = ', '.join(d_array)
 
 send['destinataries'] = d_string
 
 send['sender'] = a.sender.username

 if (c.custom_field.type == 'LinearInput'):
   send['event'] = smart_str(c.name, encoding='utf-8', strings_only=False, errors='strict')
   if a.state == True:
      send['when'] = 'Sinal acima do limite'
   else:
      send['when'] = 'Sinal abaixo do limite'  
   
 elif (c.custom_field.tag == 'GeoFence'):
   g = Geofence.objects.get(pk=a.geofence_id)
   send['event'] = smart_str(c.name, encoding='utf-8', strings_only=False, errors='strict') +" - "+smart_str(g.name, encoding='utf-8', strings_only=False, errors='strict')
   if a.state == True:
     send['when'] = 'Veículo entrar na cerca'
   else:
     send['when'] = 'Veículo sair da cerca'
 
 else:
   send['event'] = smart_str(c.name, encoding='utf-8', strings_only=False, errors='strict')
   if a.state == True:
       send['when'] = 'Ligado'
   else:
       send['when'] = 'Desligado'


 # print a.__dict__

 
 send['name'] = smart_str(a.name, encoding='utf-8', strings_only=False, errors='strict')
 send['time_end'] = str(a.time_end)
 send['time_start'] = str(a.time_start)
 send['active'] = str(son(a.active))
 send['receive_popup'] = str(son(a.receive_popup))
 send['receive_email'] = str(son(a.receive_email))
 send['receive_sms'] = str(son(a.receive_sms))
 
 # if (send['event'] != None):
   # pass
  # send['event'] = smart_str(c.name, encoding='utf-8', strings_only=False, errors='strict')
 

 json = simplejson.dumps(send)

 return HttpResponse(json, mimetype='application/json')
 
def son(request):
  
  if request == True:
    return 'Sim'
  else:
    return 'Não'
  
