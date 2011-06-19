from django.db.models import Q
from django.http import HttpResponse
from querystring_parser import parser
from itrack.alerts.models import Popup
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def status(request):
    if request.method == 'POST':
        # gets the system
        system = parser.parse(request.POST.urlencode())['system']
        
        #checks if there's a popup for this system
        popups_list = Popup.objects.filter(Q(system = system) & Q(alert__destinataries = request.user.id))
        print popups_list
        data = {}

        for popup in popups_list:
           data[popup.id] = {'name': popup.alert.name, 'date': popup.date, 'trigger': popup.alert.trigger, 'plate': popup.vehicle.license_plate, 'limit':popup.alert.linear_limit, 'state':popup.alert.state }

                   
        numalerts = len(data)
         
        return render_to_response("alerts/templates/status.html",locals(),context_instance=RequestContext(request))

    else:
       return HttpResponse("fail") 
