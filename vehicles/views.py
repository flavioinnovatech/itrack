# -*- coding:utf8 -*-

from itrack.vehicles.models import Vehicle
from itrack.vehicles.forms import VehicleForm,SwapForm
from itrack.equipments.models import Equipment
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect

def index(request):
    system = request.session['system']
    
    
    equipments = Equipment.objects.filter(system = system)
    
    rendered_list = ""
    
    for item in equipments:
        print item.id
        print Vehicle.objects.filter(equipment=1)
        try:
            v = Vehicle.objects.get(equipment__id=item.id)
            rendered_list+=u"<tr style='width:5%;'><td>"+item.name+" </td><td>"+str(v.license_plate)+"</td><td><a class='table-button' href=\"/vehicles/edit/"+str(v.id)+"/\">Editar</a>  <a class='table-button'  href=\"/vehicles/delete/"+str(v.id)+"/\">Apagar</a>  <a class='table-button'  href=\"/vehicles/swap/"+str(v.id)+"/\">Remanejar</a></td></tr>"
        except:
            v_str = "<a class='table-button' href=\"/vehicles/create/"+str(item.id)+"/\">Criar veiculo</a>"
            rendered_list+=u"<tr style='width:5%;'><td style='width:40%;'>"+item.name+" </td><td style='width:40%;'></td><td>"+v_str+"</td><td></td></tr>"
    
    return render_to_response("vehicles/templates/index.html",locals(),context_instance=RequestContext(request))


def create(request,offset):
    
    if request.method == 'POST':
        
        form = VehicleForm(request.POST)
        if form.is_valid():
            e = Equipment.objects.get(pk=int(offset))
            v = form.save(commit=False)
            v.equipment = e
            v.save()
            return HttpResponseRedirect("/vehicles/create/finish")
        else:
            return render_to_response("vehicles/templates/create.html",locals(),context_instance=RequestContext(request),)
        
    else:
        form = VehicleForm()
        return render_to_response("vehicles/templates/create.html",locals(),context_instance=RequestContext(request),)
        
def create_finish(request):
    return render_to_response("vehicles/templates/create_finish.html",locals())
        
def edit(request,offset):
    v = Vehicle.objects.get(pk=int(offset))
    if request.method == 'POST':    
        form = VehicleForm(request.POST,instance=v)
        if form.is_valid():
            e = Equipment.objects.get(pk=int(offset))
            v = form.save(commit=False)
            v.equipment = e
            v.save()
            return HttpResponseRedirect("/vehicles/edit/finish")
        else:
            return render_to_response("vehicles/templates/edit.html",locals(),context_instance=RequestContext(request),)
        
    else:
        form = VehicleForm(instance=v)
        return render_to_response("vehicles/templates/edit.html",locals(),context_instance=RequestContext(request),)
        
def edit_finish(request):
    return render_to_response("vehicles/templates/edit_finish.html",locals())


    
def delete(request,offset):
  v = Vehicle.objects.get(pk=int(offset))
  if request.method == 'POST':
    v.delete()
    
    return HttpResponseRedirect("/vehicles/delete/finish")
    
  else:
      return render_to_response("vehicles/templates/delete.html",locals(),context_instance=RequestContext(request))
      
def delete_finish(request):
    return render_to_response("vehicles/templates/delete_finish.html",locals())


def swap_finish(request):
    return render_to_response("vehicles/templates/swap_finish.html",locals())

def swap(request,offset):
  v = Vehicle.objects.get(pk=int(offset))
  
  if request.method == 'POST':
    form = SwapForm(request.POST)
    
    print "form:",form
    if form.is_valid():
  
        e = Equipment.objects.get(pk=request.POST["equipment"])
        try:
            v2 = Vehicle.objects.get(equipment = e)
        except:
            v2 = None
            
        if v2 != None:
            e2 = Equipment.objects.get(vehicle=v)
            v.equipment = e
            v2.equipment = e2
            v.save()
            v2.save()
            
        else:
            v.equipment = e
            v.save()
            
        return HttpResponseRedirect("/vehicles/swap/finish")
    else:
        form.fields["equipment"].queryset = Equipment.objects.filter(system=request.session["system"])
        return render_to_response("vehicles/templates/swap.html",locals(),context_instance=RequestContext(request))
  else:
    form = SwapForm()
    form.fields["equipment"].queryset = Equipment.objects.filter(system=request.session["system"])
    return render_to_response("vehicles/templates/swap.html",locals(),context_instance=RequestContext(request))
        

