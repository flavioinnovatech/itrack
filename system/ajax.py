
from django.utils import simplejson
from django.http import HttpResponse

from itrack.system.models import System
from itrack.system.tools import flatten, findChildInstance


def get_sms_count(request):
    
    try:
        s = System.objects.get(pk=int(request.session['system']))
        
        child_list=flatten(findChildInstance(s.id))
            
        sms_total = 0
        for it in child_list:
            sms_total += it.sms_count
            
        sms_total += s.sms_count
        
        request.session['sms_sent'] = s.sms_count
        request.session['sms_total'] = sms_total
        json_output = {'sms_sent':s.sms_count, 'sms_total':sms_total}
        json_output = simplejson.dumps(json_output)
    
        return HttpResponse(json_output, mimetype='application/json')
    except:
        return HttpResponse('fail')
