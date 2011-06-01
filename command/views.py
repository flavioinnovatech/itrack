# -*- coding:utf8 -*-
from itrack.command.models import Command
from itrack.command.forms import CommandForm
from itrack.equipments.models import Equipment
from itrack.system.models import System
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect

def index(request):
    system = request.session['system']
    
    equipments = Command.objects.filter(system = system)
    
    rendered_list = ""
    
    for c in equipments:
        try:
            rendered_list+=u"<tr style='width:5%;'><td style=\"width:100px\">"+c.equipment.name+" </td><td style=\"width:100px\">"+str(c.type)+"</td><td style=\"width:100px\">"+str(c.state)+"</td><td style=\"width:150px\">"+(str(c.time_sent) if (c.time_sent is not None) else "")+"</td><td style=\"width:150px\">"+(str(c.time_received) if (c.time_received is not None) else "")+"</td><td style=\"width:150px\">"+(str(c.time_executed) if (c.time_executed is not None) else "")+"</td><td> <a class='table-button'  href=\"/commands/delete/"+str(c.id)+"/\">Apagar</a></td></tr>"
        except:
            pass
    
    return render_to_response("command/templates/index.html",locals(),context_instance=RequestContext(request))


def create(request,offset):
    
    if request.method == 'POST':
        
        form = CommandForm(request.POST)
        if form.is_valid():
            s = System.objects.get(pk=int(offset))
            c = form.save(commit=False)
            c.system = s
            c.state = "Enviado para o servidor"
            c.save()
            return HttpResponseRedirect("/commands/create/finish")
        else:
            return render_to_response("command/templates/create.html",locals(),context_instance=RequestContext(request),)
        
    else:
        
        form = CommandForm()
        form.fields["equipment"].queryset = Equipment.objects.filter(system = int(offset))
        return render_to_response("command/templates/create.html",locals(),context_instance=RequestContext(request),)
        
def create_finish(request):
    return render_to_response("command/templates/create_finish.html",locals())

def delete(request,offset):
  c = Command.objects.get(pk=int(offset))
  if request.method == 'POST':
    
    c.delete()
    
    return HttpResponseRedirect("/commands/delete/finish")
    
  else:
      print c.__dict__
      return render_to_response("command/templates/delete.html",locals(),context_instance=RequestContext(request))
      
def delete_finish(request):
    return render_to_response("command/templates/delete_finish.html",locals())

