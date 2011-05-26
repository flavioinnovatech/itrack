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
            rendered_list+=u"<tr style='width:5%;'><td style=\"width:100px\">"+c.equipment.name+": </td><td style=\"width:100px\">"+str(c.type)+"</td><td style=\"width:100px\">"+str(c.state)+"</td><td style=\"width:150px\">"+str(c.time_sent)+"</td><td style=\"width:150px\">"+ str(c.time_received)+"</td><td style=\"width:150px\">"+str(c.time_executed)+"</td><td><a class='table-button' href=\"/commands/edit/"+str(c.id)+"/\">Editar</a>  <a class='table-button'  href=\"/commands/delete/"+str(c.id)+"/\">Apagar</a></td></tr>"
        except:
            pass
    
    return render_to_response("command/templates/index.html",locals(),context_instance=RequestContext(request))


def create(request,offset):
    
    if request.method == 'POST':
        
        form = CommandForm(request.POST)
        if form.is_valid:
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
        return render_to_response("command/templates/create.html",locals(),context_instance=RequestContext(request),)
        
def create_finish(request):
    return render_to_response("command/templates/create_finish.html",locals())
        
def edit(request,offset):
    v = Vehicle.objects.get(pk=int(offset))
    if request.method == 'POST':    
        form = VehicleForm(request.POST,instance=v)
        if form.is_valid:
            e = Equipment.objects.get(pk=int(offset))
            v = form.save(commit=False)
            v.equipment = e
            v.save()
            return HttpResponseRedirect("/commands/edit/finish")
        else:
            return render_to_response("command/templates/edit.html",locals(),context_instance=RequestContext(request),)
        
    else:
        form = VehicleForm(instance=v)
        return render_to_response("command/templates/edit.html",locals(),context_instance=RequestContext(request),)
        
def edit_finish(request):
    return render_to_response("command/templates/edit_finish.html",locals())


    
def delete(request,offset):
  c = Command.objects.get(pk=int(offset))
  if request.method == 'POST':
    
    
    c.delete()
    
    return HttpResponseRedirect("/commands/delete/finish")
    
  else:
      return render_to_response("command/templates/delete.html",locals(),context_instance=RequestContext(request))
      
def delete_finish(request):
    return render_to_response("command/templates/delete_finish.html",locals())


        

