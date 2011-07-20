# -*- coding:utf8 -*-
import sys 
import socket
import os
import sys 
import select
from xml.etree import cElementTree as ElementTree
import time
from datetime import datetime

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson

from itrack.command.models import Command, CPRSession
from itrack.vehicles.models import Vehicle
from itrack.command.forms import CommandForm
from itrack.equipments.models import Equipment,CustomFieldName,CustomField, Tracking,TrackingData
from itrack.system.models import System

from querystring_parser import parser

TCP_IP = '187.115.25.240'   # the server IP address
#TCP_IP = '192.168.1.119'

TCP_PORT = 5000			# the server port
BUFFER_SIZE = 20000		# the maximum buffer size (in chars) for a TCP packet


@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='comando').count() != 0)
def index(request):
    system = request.session['system']
    
    equipments = Command.objects.filter(system = system)
    rendered_list = ""
    
    display_list = []
    for c in equipments:
        
        #checks the status of the command and update if matches the equipment tracking table
        tracking = Tracking.objects.filter(equipment=c.equipment.equipment).order_by('eventdate').reverse()[0]
        trackingdata = TrackingData.objects.filter(tracking=tracking).filter(type=c.type.custom_field)
        if c.action == 'ON' and len(trackingdata) > 0:
            c.state = u"2"
            c.time_executed = tracking.eventdate
            c.save()
        elif c.action == 'OFF' and len(trackingdata) == 0 :
            c.state = u"2"
            c.time_executed = tracking.eventdate
            c.save()
        
        display_list.append({
            'plate': c.equipment.license_plate,
            'type': c.type,
            'state': str(c.state),
            'time_sent': (c.time_sent),
            'time_received': (c.time_received),
            'time_executed': (c.time_executed),
            'id': c.id,
            'action' : c.action,
        })    
    
    return render_to_response("command/templates/index.html",locals(),context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='comando').count() != 0)
def create(request,offset,vehicle=None):
    
    if request.method == 'POST':
        
        form = CommandForm(request.POST)
        if form.is_valid():
            s = System.objects.get(pk=int(offset))

            c = form.save(commit=False)
            
            #checks if the field exists for the selected equipment
            try:
                field_check = Vehicle.objects.get(equipment__type__custom_field=c.type.custom_field)
            except ObjectDoesNotExist:
                return render_to_response("command/templates/error.html",locals(),context_instance=RequestContext(request),)
            
            #checks if there's no other command in process for this equipment
            
            try:
                command_check = Command.objects.filter(equipment = c.equipment)
                print len(command_check)
                if len(command_check) > 0:
                    return render_to_response("command/templates/error2.html",locals(),context_instance=RequestContext(request),)
            except:
                pass
            
            #accessing the protocols to send the command
            sess = CPRSession.objects.all()[0]
            
            ack_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"98\" Reason=\"0\" Save=\"FALSE\"/><Data /></Package>"
            
            s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_out.connect((TCP_IP, TCP_PORT))
            
            seckey_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"2\" /><Data SessionId=\""+sess.key+"\" /></Package>"
            
            s_out.send(seckey_msg)
            data2 = s_out.recv(BUFFER_SIZE)
            
            
            blocker_msg =  "<?xml version=\"1.0\" encoding=\"ASCII\"?>\n<Package>\n  <Header Version=\"1.0\" Id=\"6\" />\n  <Data Account=\"2\" ProductId=\""+str(c.equipment.equipment.type.product_id)+"\" Serial=\""+c.equipment.equipment.serial+"\" Priority=\"2\" />\n  <Command "+c.type.custom_field.tag+"=\""+c.action+"\"/>\n</Package>"
            
            s_out.send(blocker_msg)
            data2 = s_out.recv(BUFFER_SIZE)
            s_out.send(ack_msg)
            
            c.system = s
            c.state = 0
            c.time_sent = datetime.now()
            c.save()
            return HttpResponseRedirect("/commands/create/finish")
        else:
        
            e_set = Equipment.objects.filter(system = int(offset))
            v_set = []
            
            for e in e_set:
                try:
                    v_set.append(Vehicle.objects.get(equipment=e.id).id)
                except:
                    print "Veículo não encontrado."
            form.fields["equipment"].queryset = Vehicle.objects.filter(id__in=v_set)
            form.fields["equipment"].label = "Veículo"
            form.fields["equipment"].empty_label = "(Selecione a placa)"
            
            form.fields["type"].queryset = CustomFieldName.objects.filter(Q(custom_field__type = 'Output') & Q(system = int(offset)) & Q(custom_field__availablefields__system = int(offset))).distinct()
            form.fields["type"].empty_label = "(selecione o Comando)"
            vehicles_exist = True
            return render_to_response("command/templates/create.html",locals(),context_instance=RequestContext(request),)
    else:
        
        form = CommandForm()
        e_set = Equipment.objects.filter(system = int(offset))
        v_set = []
        
        for e in e_set:
            try:
                v_set.append(Vehicle.objects.get(equipment=e.id).id)
            except:
                print "Veículo não encontrado."
             
        form.fields["equipment"].queryset = Vehicle.objects.filter(id__in=v_set)
        form.fields["equipment"].label = "Veículo"
        form.fields["equipment"].empty_label = "(Selecione a placa)"
        form.fields["equipment"].initial = vehicle
        form.fields["type"].queryset = CustomFieldName.objects.filter(Q(custom_field__type = 'Output') & Q(system = int(offset)) & Q(custom_field__availablefields__system = int(offset))).distinct()
        form.fields["type"].empty_label = "(selecione o Comando)"
        
        if form.fields["equipment"].queryset:
            vehicles_exist = True
        else:
            vehicles_exist = False
            
        return render_to_response("command/templates/create.html",locals(),context_instance=RequestContext(request),)
        
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='comando').count() != 0)
def create_finish(request):
    return render_to_response("command/templates/create_finish.html",locals())

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='comando').count() != 0)
def delete(request,offset):
  c = Command.objects.get(pk=int(offset))
  if request.method == 'POST':
    
    c.delete()
    
    return HttpResponseRedirect("/commands/delete/finish")
    
  else:
      print c.__dict__
      return render_to_response("command/templates/delete.html",locals(),context_instance=RequestContext(request))
      
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='comando').count() != 0)
def delete_finish(request):
    return render_to_response("command/templates/delete_finish.html",locals())
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='comando').count() != 0)
def load(request):
  
  parsed_dict = parser.parse(request.POST.urlencode())
  
  c = Command.objects.get(pk=parsed_dict['id'])

  send = {}

  send['vehicle'] = str(c)
  send['time_executed'] = str(c.time_executed)
  send['time_sent'] = str(c.time_sent)
  send['time_received'] = str(c.time_received)
  send['action'] = str(c.action)
  send['type'] = str(c.type)
  send['state'] = str(c.state)
    
  json = simplejson.dumps(send)
  
  return HttpResponse(json, mimetype='application/json')
