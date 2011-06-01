# -*- coding:utf8 -*-
from django.db.models import Q
from django.contrib.auth.models import User
from itrack.system.models import System
from itrack.system.views import findChild,isChild
from itrack.equipments.models import Equipment
from itrack.alerts.models import Alert
from itrack.alerts.forms import AlertForm
from itrack.equipments.models import Equipment
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def index(request):
    system_id = request.session['system']
   
    equipments = Equipment.objects.filter(system = system_id)
    rendered_list = ""
    for item in equipments:
     
      alerts = Alert.objects.filter(equipment=item.id)
      for v in alerts:
        rendered_list+=u"<tr style='width:5%;'><td style='width:25%;'>"+v.name+" </td><td style='width:18%'>"+item.name+"</td><td style='width:25%'>"+str(v.time_start)+"</td><td style='width:20%'>"+str(v.time_end)+"</td><td style='width:120px; padding-left:5px;'><a class='table-button' href=\"/alerts/edit/"+str(v.id)+"/\">Editar</a>  <a class='table-button'  href=\"/alerts/delete/"+str(v.id)+"/\">Apagar</a></td></tr>"


    return render_to_response("alerts/templates/index.html",locals(),context_instance=RequestContext(request))


def create(request,offset):
    
    if request.method == 'POST':
        
        form = AlertForm(request.POST)
        if form.is_valid():
            
            system_id = request.session['system']
            
            v = form.save(commit=False)

            v.system_id = system_id
            v.save()
            return HttpResponseRedirect("/alerts/create/finish")
        else:
            return render_to_response("alerts/templates/create.html",locals(),context_instance=RequestContext(request),)
        
    else:
        system_id = request.session['system']
        form = AlertForm()
        adm_id = System.objects.get(pk=int(system_id)).administrator.id
        form.fields['equipment'].queryset=Equipment.objects.filter(system=int(system_id))
        
        form.fields['destinataries'].queryset=User.objects.filter(Q(system=int(system_id)) | Q(pk=adm_id) )
        
        return render_to_response("alerts/templates/create.html",locals(),context_instance=RequestContext(request))
        
def create_finish(request):
    return render_to_response("alerts/templates/create_finish.html",locals())
        
def edit(request,offset):
    v = Alert.objects.get(pk=int(offset))
    if request.method == 'POST':    
        form = AlertForm(request.POST,instance=v)
        if form.is_valid():
          
            system_id = request.session['system']
           
            v = form.save(commit=False)

            v.system_id = system_id
            v.save()
            return HttpResponseRedirect("/alerts/edit/finish")
        else:
            return render_to_response("alerts/templates/edit.html",locals(),context_instance=RequestContext(request),)
        
    else:
        system_id = request.session['system']
        form = AlertForm(instance=v)
        adm_id = System.objects.get(pk=system_id).administrator.id
        form.fields['equipment'].queryset=Equipment.objects.filter(system=system_id)
        
        systems = System.objects.all()
        
        sysids = []
        queryset =""
        for sys in systems:
          if ( isChild(sys.id,[system_id,findChild(system_id)]) == True):
            sysids.append(sys.id)

        filter_dict = {'system__id__in': sysids}
                
        form.fields['destinataries'].queryset=User.objects.filter(**filter_dict)
        
        return render_to_response("alerts/templates/edit.html",locals(),context_instance=RequestContext(request),)
        
def edit_finish(request):
    return render_to_response("alerts/templates/edit_finish.html",locals())


    
def delete(request,offset):
  a = Alert.objects.get(pk=int(offset))
  if request.method == 'POST':
    
    a.delete()
    
    return HttpResponseRedirect("/alerts/delete/finish")
    
  else:
      return render_to_response("alerts/templates/delete.html",locals(),context_instance=RequestContext(request))
      
def delete_finish(request):
    return render_to_response("alerts/templates/delete_finish.html",locals())


        
