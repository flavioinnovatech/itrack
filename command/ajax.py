# -*- coding:utf8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils import simplejson

from itrack.command.models import Command, CPRSession

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
