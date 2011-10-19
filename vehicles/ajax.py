
from equipments.models import Equipment
from django.utils import simplejson
from django.http import HttpResponse
from querystring_parser import parser
from django.contrib.auth.decorators import login_required, user_passes_test

#TODO: falhar caso o equip nao pertenca ao sistema
@login_required
def edit_equipment(request,equip_id):

    if request.method == 'POST':
        post = parser.parse(request.POST.urlencode())
        e = Equipment.objects.get(pk=int(post['equip']))
        e.simcard = post['simcard']
        e.save()
        
        
        return HttpResponse("ok", mimetype='application/json')
    else:
        equip = Equipment.objects.get(pk=equip_id)
        
        json_output = simplejson.dumps(
            {'simcard':equip.simcard,
              'equip':str(equip)}
            )     
    return HttpResponse(json_output, mimetype='application/json')

@login_required
def delete_equipment(request):
    if request.method == 'POST':
        post = parser.parse(request.POST.urlencode())
        e = Equipment.objects.get(pk=int(post['equip']))
        print 'vai deletar aqui'
        #e.delete()
    return HttpResponse("ok", mimetype='application/json')
        

