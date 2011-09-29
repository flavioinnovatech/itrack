# -*- coding: utf-8 -*-

from itrack.equipments.management.commands.geocoding import Geocode,Routecalc
from django.utils import simplejson
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.encoding import smart_str
from querystring_parser import parser


def geocoder(request):
    
    parsed_dict = parser.parse(request.POST.urlencode())
                    
    r = Geocode(parsed_dict['addresses'])
        
    return HttpResponse(r, mimetype='application/json')

def route_calculator(request):
    
    parsed_dict = parser.parse(request.POST.urlencode())
    
    p = parsed_dict['points']
    t = parsed_dict['tolerance']
    
    r = Routecalc(p,t)
    
    return HttpResponse(r, mimetype='application/json')