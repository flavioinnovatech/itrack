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
from itrack.equipments.models import CustomFieldName
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
               }
                       
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
 
 
 send = {}
 
 if (a.geofence_id != None):
   g = Geofence.objects.get(pk=a.geofence_id)
   send['event'] = smart_str(c.name, encoding='utf-8', strings_only=False, errors='strict') +" - "+smart_str(g.name, encoding='utf-8', strings_only=False, errors='strict')
   if a.state == True:
     send['when'] = 'Veículo entrar na cerca'
   else:
     send['when'] = 'Veículo sair da cerca'
 


 print a.__dict__

 
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
  
