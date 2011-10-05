# -*- coding:utf8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils import simplejson
from django.db.models import Q

from itrack.command.models import Command, CPRSession
from itrack.system.models import System
from itrack.equipments.models import CustomFieldName,CustomField
from itrack.vehicles.models import Vehicle

from querystring_parser import parser

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='comando').count() != 0)
def load(request):
  
  parsed_dict = parser.parse(request.POST.urlencode())
  
  c = Command.objects.get(pk=parsed_dict['id'])

  s = User.objects.get(pk=c.sender.id)

  send = {}

  send['vehicle'] = str(c)
  send['time_executed'] = str(c.time_executed)
  send['time_sent'] = str(c.time_sent)
  send['time_received'] = str(c.time_received)
  send['action'] = str(c.action)
  send['type'] = str(c.type)
  send['state'] = str(c.state)
  send['sender'] = str(s.username)
    
  json = simplejson.dumps(send)
  
  return HttpResponse(json, mimetype='application/json')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0 or u.groups.filter(name='comando').count() != 0)
def check(request):
  
  system = request.session['system']
  s = System.objects.get(pk=system)
  parsed_dict = parser.parse(request.POST.urlencode())
  v = Vehicle.objects.get(license_plate=parsed_dict['vehicle'])
  cfn = CustomFieldName.objects.filter(Q(name=parsed_dict['command']),Q(system=s))
  
  try:
    c = Command.objects.filter(Q(system=s),Q(equipment=v),Q(type=cfn)).order_by('time_executed').reverse()[0]
    
  except:
    send = {}
    json = simplejson.dumps(send)
    return HttpResponse(json, mimetype='application/json')

  send = {}
  
  print c.action
  

  json = simplejson.dumps(send)
  
  return HttpResponse(json, mimetype='application/json')
