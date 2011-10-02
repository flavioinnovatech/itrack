# -*- coding:utf8 -*-
import sys 
import socket
import os
import sys 
import select
from xml.etree import cElementTree as ElementTree
import time
import datetime
import maxtrack

from datetime import datetime

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson
from django.conf import settings

from django.forms import model_to_dict
from itrack.command.models import Command, CPRSession
from itrack.vehicles.models import Vehicle
from itrack.command.forms import CommandForm
from itrack.equipments.models import Equipment,CustomFieldName,CustomField, Tracking,TrackingData,AvailableFields,EquipmentType
from itrack.system.models import System
from itrack.system.tools import findChild,findParents
from itrack.vehicles.models import Vehicle
from django.contrib.auth.models import User
from django.core import serializers
from querystring_parser import parser


TCP_IP = settings.EXTRACTOR_IP   # the server IP address
#TCP_IP = '192.168.1.119'

TCP_PORT = 5000			# the server port
BUFFER_SIZE = 20000		# the maximum buffer size (in chars) for a TCP packet


def systemCommandDetails(sysid):
    lines = []
    system = System.objects.get(pk=sysid)
    commands = Command.objects.filter(system=system)
    if system.parent == None:
        childof = None
    else:
        childof = system.parent.id
    lines.append({  'id':system.id,
                    'childof':childof,
                    'sysname':system.name,
                    'sysid':system.id
                })
    for command in commands:
    

        sender = User.objects.get(pk=command.sender_id)
        lines.append({  'id':command.id,
                        'childof':system.id,
                        'type':command.type,
                        'action':command.action,
                        'plate': command.equipment,
                        'state':command.state,
                        'time_sent':command.time_sent,
                        'time_received':str(command.time_received),
                        'time_executed':command.time_executed,
                        'sender': str(sender.username),
                        'test':command.equipment.equipment.type
                        
                    })
    
    if commands: 
        return lines    
    else: 
        return []

def mountCommandTree(list_of_childs,parent):
    table = []
    
    if type(list_of_childs).__name__ == 'list':
        if(len(list_of_childs) > 0):
            prev = list_of_childs[0]
            if type(prev).__name__ != 'list':
                lines = systemCommandDetails(prev)
                for line in lines:
                    table.append(line)
            else:
                pass
                
            for el in list_of_childs[1:]:
                
                if type(el).__name__ == 'list':
                    lines = mountCommandTree(el,prev)
                else:
                    lines = mountCommandTree(el,parent)
                
                for line in lines:
                    table.append(line)
                    
                prev = el
    
        return table
           
    else:
        return systemCommandDetails(list_of_childs)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='comando').count() != 0)

def test278(request):
    response = HttpResponse(mimetype='text/html')
    output2 = "Quanta Test"
    
    
    
    output1 = "<html><head><style>"
    output1 += ".vr{background-color:#0FF;}.ty{background-color:#FF0;}"
    output1 += ".eq{background-color:#F00;} .tr{background-color:#0F0;}"
    output1 += ".td{background-color:#00F;}</style></head><body>" + output2 + "</body></html>"
    response.write(output1)
    return response
def test277(request):

    output1 = "<table border=1>"
    equipTypeIndex = {}
    list0 = []
    data = {}
    eqX = Equipment.objects.filter(serial="98285")
    cfX = CustomField.objects.get(tag="SendCmdState")
    t0 = TrackingData.objects.filter(type=cfX).filter(tracking__equipment=eqX).latest('tracking__eventdate')

    try :
        output1 += "<tr><td>" +str(t0.type) + "</td><td>" + str(t0.value) + "</td><td>" + str(t0.tracking.eventdate) + "</td></tr>"
    except:
        pass

    equipTypeIndex = {}
    list0 = []
    data = {}
    tX = TrackingData.objects.filter(tracking__equipment=eqX).order_by('tracking__eventdate').reverse()[:200]
    
    for t0 in tX:
        if t0.type.pk in list0:
            continue
        list0.append(t0.type.pk)
        try :
            data[t0.type.pk] = {}
            data[t0.type.pk]['type'] = str(t0.type)
            data[t0.type.pk]['value'] = str(t0.value)
            data[t0.type.pk]['evtdt'] = str(t0.tracking.eventdate)
            output1 += "<tr><td>" +str(t0.type) + "</td><td>" + str(t0.value) + "</td><td>" + str(t0.tracking.eventdate) + "</td></tr>"
        except:
            pass
    output1 += "</table>"
    response = HttpResponse(mimetype='text/html')
    output1 = "<html><head><style>.vr{background-color:#0FF;}.ty{background-color:#FF0;} .eq{background-color:#F00;} .tr{background-color:#0F0;} .td{background-color:#00F;}</style></head><body>" + output1 + "</body></html>"
    response.write(output1)
    return response
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='comando').count() != 0)
def index(request):
    system = request.session['system']
    
    equipments = Command.objects.filter(system = system)
    rendered_list = ""
    
    display_list = []
    
    
    #conect to mt gateway to get status updates
    
    #host = settings.MXT_IP
    #port = settings.MXT_PORT
    #skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    #skt.connect((host,port))
    
    hasmtcinlist = False
    for c in equipments:
        _equiptype = str(c.equipment.equipment.type).strip()
        if _equiptype == "MTC-400":
            if c.state!= u'2' and c.state!= u'3':
                eqX = c.equipment.equipment
                sent = False 
                cfX = CustomField.objects.get(tag="SendCmdState")
                t0 = TrackingData.objects.filter(type=cfX).filter(tracking__equipment=eqX).latest('tracking__eventdate')
                if t0.value=='1' or t0.value==1:
                    c.state = u'1'
                    t0.value = 201 # value 1, which is 'sending', is also being used now.
                    t0.save()
                cfX = CustomField.objects.get(tag="Output1")
                tX = TrackingData.objects.filter(type=cfX).filter(tracking__equipment=eqX).latest('tracking__eventdate')
                if str(tX.value)=="1" and c.action=='ON':
                    c.state = u'2'
                    c.time_executed = tX.tracking.eventdate
                elif str(tX.value)=="0" and c.action=='OFF':
                    c.state= u'2'
                    c.time_executed = tX.tracking.eventdate
                c.save()
        else: #old code (leandro|fabio)
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
            
        sender = User.objects.get(pk=c.sender_id)
        
        display_list.append({
            'plate': c.equipment.license_plate,
            'type': c.type,
            'state': str(c.state),
            'time_sent': (c.time_sent),
            'time_received': str(c.time_received),
            'time_executed': (c.time_executed),
            'id': c.id,
            'action' : c.action,
            'sender': str(sender.username)
#            'test':str(c.type)
        })

    childs = findChild(system)
    command_tree = mountCommandTree([system,childs],system)    
    
    return render_to_response("command/templates/index.html",locals(),context_instance=RequestContext(request))
def loadavailable(request):
    response = HttpResponse(mimetype='text/xml')
    output1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    output1 += "<document>"
    id = request.GET.get('id', '')
    system = request.session['system']
    msg = ""
    try:
        if id == '':
            equipments = Vehicle.objects.get(system = system)
            #msg = "no id"
        else:
            equipments = Vehicle.objects.get(pk = int(id))
            #msg = "id" + str(id) +"\n"
    except:
        msg = "erro1"
    count = 0;
    try:
        ets = equipments.equipment.type
        #        msg += str(ets.custom_field)
#cfn = CustomFieldName.objects.filter(
#Q(system=int(offset))&
#Q(custom_field__availablefields__system=int(offset))&
#Q(custom_field__availablefields__equip_type__custom_field__in=e.type.custom_field.all())&
#Q(custom_field__type="Output")).distinct()
        cfs = [x for x in Vehicle.objects.get(pk=int(id)).equipment.type.custom_field.filter(type="Output")]
        print("$$$")
        print(cfs)
        cfns = CustomFieldName.objects.filter(custom_field__in=cfs,system=request.session['system'],custom_field__availablefields__system=request.session['system'])
        print("$$$")
        print(cfns)
        for cfn in cfns:
            output1 += "<field>"
            output1 += "<key>"+str(cfn.pk)+"</key>"
            output1 += "<val>"+str(cfn.name.encode("UTF-8"))+"</val>"
            output1 += "</field>"
            count += 1
            # 
    except Exception as err:
        msg += str(type(err)) + " % " + str(err.args) + " % " + str(err)

    msg += str(count)
#    cfs = CustomFields.objects.filter(pk=af.custom_fields)
 #   for a in cfs:
  #      msg += a.name
        
    output1 += "<msg>" + msg + "</msg>"
    output1 += "</document>"
    response.write(output1)
    return response
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='comando').count() != 0)
def create(request,offset,vehicle=None):
    
    if request.method == 'POST':
        
        form = CommandForm(request.POST)
        if form.is_valid():
            s = System.objects.get(pk=int(offset))

            c = form.save(commit=False)
            
            u = str(form.cleaned_data['username'])
            p = str(form.cleaned_data['password'])
            
            user = authenticate(username=u, password=p)
            if user is None:
                error_title = 'Erro: Usuário e/ou senha incorretos'
                error = 'Usuário e/ou senha incorretos'
                return render_to_response("command/templates/error.html",locals(),context_instance=RequestContext(request),)

            else:
                sender = User.objects.get(username=u)

                #checks if the sender has permission to send command from this system
                if (s.administrator_id != sender.id):
                    
                    parents = findParents(s,[])
                    
                    userisparent = 0;
                    for p in parents:
                        if (p.administrator_id == sender.id):
                            userisparent = 1

                    if (userisparent == 0):                    
                        error_title = 'Erro: Usuário sem permissão'
                        error = 'O usuário não tem permissão para enviar comandos nesse cliente.'
                        return render_to_response("command/templates/error.html",locals(),context_instance=RequestContext(request),)
                    
                            
                c.sender = sender
                #checks if the field exists for the selected equipment
                try:
                    cfs = [x for x in Vehicle.objects.get(pk=int(request.POST['equipment'])).equipment.type.custom_field.filter(type="Output")]
                    cfns = CustomFieldName.objects.filter(custom_field=c.type,system=s,custom_field__availablefields__system=s)
                    print cfns
        
                except ObjectDoesNotExist:
                    error_title = 'Erro: O atuador selecionado não existe'
                    error = 'O comando a ser enviado selecionou um atuador inexistente para o tipo de equipamento cadastrado.'
                    return render_to_response("command/templates/error.html",locals(),context_instance=RequestContext(request),)
                except:
                    pass
                    
                #checks if there's no other command in process for this equipment
                
                try:
                    command_check = Command.objects.filter(equipment = c.equipment).exclude(state=u'2').exclude(state=u'3')
                    print len(command_check)
                    if len(command_check) > 0:
                        return render_to_response("command/templates/error2.html",locals(),context_instance=RequestContext(request),)
                except:
                    pass
                    
                _equiptype = str(c.equipment.equipment.type).strip()
                if _equiptype == "MTC-400" or _equiptype == "MTC-500" :
                    #MAX TRACK
                    print "INMAX"
                    host = settings.MXT_IP
                    port = settings.MXT_PORT
                    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
                    skt.connect((host,port))
                    mount0 = ""
                    mount0 += "<command><equipment>" + str(c.equipment.equipment.name).strip() + "</equipment>"
                    mount0 += "<serial>" + str(c.equipment.equipment.serial).strip() + "</serial>"
                    mount0 += "<type>" + str(c.equipment.equipment.type).strip() + "</type>"
                    mount0 += "<function>" + str(c.type.custom_field.tag).strip() + "</function>"
                    t = datetime.now()
                    mount0 += "<id>" + str(time.mktime(t.timetuple())).strip() + "</id>"
                    mount0 += "<argument>" + str(c.action) + "</argument></command>"
                    print(mount0)
                    msg = mount0
                    totalsent = 0   
                    while totalsent < len(msg):   
                        sent = skt.send(msg[totalsent:])   
                        if sent == 0:
                            c.system = s
                            c.state = u'3'
                            c.time_sent = datetime.now()
                            c.save()                        
                            error_title = 'Erro: falha na transmissao.'
                            error = 'Ocorreu uma falha na transmissao do comando para a central. Tente novamente.'
                            return render_to_response("command/templates/error.html",locals(),context_instance=RequestContext(request),)
                    
                        totalsent = totalsent + sent
                    chunk = skt.recv(4096)
                    # WAIT FOR RESPONSE??
                    skt.close()
                    c.system = s
                    c.state = u'0'
                    c.time_sent = datetime.now()
                    c.save()
                    return HttpResponseRedirect("/commands/create/finish")
                else:                
                
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
                    c.state = u'0'
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
        form.fields["type"].queryset = CustomFieldName.objects.filter(
        Q(custom_field__type = 'Output') & Q(system = int(offset)) & 
        Q(custom_field__availablefields__system = int(offset))).distinct()
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
    
    
def check_state_onserver(request):

    cmds = Command.objects.filter(system = system)
    for cmd in cmds:
        if cmd.state < 2: # need to be verified (not ready or fail)
            pass
        
    # verifica no maxtrack se os commandos enviados estao prontos
    host = settings.MXT_IP
    port = settings.MXT_PORT
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    skt.connect((host,port))
    mount0 = ""
    mount0 += "<command><equipment>InfotrackWS</equipment>"
    mount0 += "<serial>" + str(c.equipment.equipment.serial).strip() + "</serial>"
    mount0 += "<type>" + str(c.equipment.equipment.type).strip() + "</type>"
    mount0 += "<function>" + str(c.type.custom_field.tag).strip() + "</function>"
    mount0 += "<argument>" + str(c.action) + "</argument></command>"
    msg = mount0;
    totalsent = 0   
    while totalsent < len(msg):   
        sent = skt.send(msg[totalsent:])   
        if sent == 0:
            c.system = s
            c.state = u'3'
            c.time_sent = datetime.now()
            c.save()                        
            error_title = 'Erro: falha na transmissao.'
            error = 'Ocorreu uma falha na transmissao do comando para a central. Tente novamente.'
            return render_to_response("command/templates/error.html",locals(),context_instance=RequestContext(request),)
    
        totalsent = totalsent + sent
    chunk = skt.recv(4096)
                    
    
    response = HttpResponse(mimetype='text/xml')
    writer = UnicodeWriter(response)
    writer.writerow("<html><head></head><body>ok</body></html>")
    return response
    
    
