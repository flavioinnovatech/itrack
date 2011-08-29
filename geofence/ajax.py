# -*- coding: utf-8 -*-

from itrack.equipments.management.commands.geocoding import Geocode
from django.utils import simplejson
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.encoding import smart_str
from querystring_parser import parser


def geocoder(request):
    
    parsed_dict = parser.parse(request.POST.urlencode())
    
    a = parsed_dict['address']
    n = parsed_dict['number']
    c = smart_str(parsed_dict['city'], encoding='utf-8', strings_only=False, errors='strict')
    s = smart_str(parsed_dict['state'], encoding='utf-8', strings_only=False, errors='strict')
    
        
    r = Geocode(a,n,c,s)
    
    return HttpResponse(r, mimetype='application/json')