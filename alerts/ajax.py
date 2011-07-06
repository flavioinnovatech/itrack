from django.db.models import Q
from django.http import HttpResponse
from querystring_parser import parser
from itrack.alerts.models import Popup
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from itrack.system.tools import systemDepth


def status(request):
    if request.method == 'POST':
        # gets the system
        user = parser.parse(request.POST.urlencode())['user']
        
        #checks if there's a popup for this system
        popups_list = Popup.objects.filter(Q(user = user))
        print popups_list
        data = {}

        for popup in popups_list:
           data[popup.id] = {'name': popup.alert.name, 'date': popup.date, 'trigger': popup.alert.trigger, 'plate': popup.vehicle.license_plate, 'limit':popup.alert.linear_limit, 'state':popup.alert.state, 'system':systemDepth(popup.vehicle.equipment.system.all()).name }
           popup.delete()
                   
        numalerts = len(data)
         
        return render_to_response("alerts/templates/status.html",locals(),context_instance=RequestContext(request))

    else:
       return HttpResponse("fail") 
