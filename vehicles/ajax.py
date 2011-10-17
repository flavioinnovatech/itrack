
from equipments.models import Equipment
from django.utils import simplejson
from django.http import HttpResponse

#TODO: falhar caso o equip nao pertenca ao sistema
def edit_equipment(request,equip_id):

    if request.method == 'POST':
        pass
    else:
        equip = Equipment.objects.get(pk=equip_id)
        
        json_output = simplejson.dumps(
            {'simcard':equip.simcard}
            )    
        print json_output  
    return HttpResponse(json_output, mimetype='application/json')


def delete_equipment(request):
    pass
