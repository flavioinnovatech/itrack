# -*- coding: utf-8 -*-
import urllib
import sys, httplib,urllib
import time
from xml.etree import cElementTree as ElementTree

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.template.defaultfilters import lower,title
from django.utils.encoding import smart_str
from django.utils import simplejson
from django.http import HttpResponse

from django.contrib.gis.geos.linestring import LineString
from django.contrib.gis.geos import Point


from itrack.pygeocoder import Geocoder
from itrack.geocodecache.models import CachedGeocode

def Routecalc(array,tolerance):
    
    ticket = "awFhbDzHd0vJaWVAzwkLyC9gf0LhbM9CyxSLyCH8aTphbIOidIZHdWOLyCtq"
    
    url = "webservices.apontador.com.br"
        
    xml = '<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><getRoute xmlns="http://webservices.maplink2.com.br"><rs>'
    
    #Loop around the points of the route
    for a in array:
        x = array[a]['lng']
        y = array[a]['lat']
        
        xml += '<RouteStop><description>origem</description><point><x>'+x+'</x><y>'+y+'</y></point></RouteStop>'
    
    xml += '</rs><ro><language>string</language><routeDetails><descriptionType>0</descriptionType><routeType>0</routeType><optimizeRoute>false</optimizeRoute></routeDetails><vehicle></vehicle><routeLine></routeLine></ro><token>'+ticket+'</token></getRoute></soap12:Body></soap12:Envelope>'
            
    conn = httplib.HTTPConnection(url,timeout=5)
    headers = {"Content-type":"application/soap+xml; charset=\"UTF-8\"","Host":"teste.webservices.apontador.com.br"}
    conn.request("POST", "/webservices/v3/Route/Route.asmx", xml, headers)
    response = conn.getresponse()
    conteudo = response.read()
    conn.close()
    
    print response.status, response.reason
    
    if response.status == 200:
        
        #TODO: Needs cached geocode here
        #TODO: refactor with try/except
    
        type = 'geofence'
        
        gxml = ElementTree.fromstring(conteudo)
        
        lngs = gxml.findall(".//{http://webservices.maplink2.com.br}x")
        lats = gxml.findall(".//{http://webservices.maplink2.com.br}y")
        
        i = 0
        j = 0
        route = []
        multiline =[]
        point = {}
        while(i != len(lngs) and j != len(lats)):
            point['lng'] = lngs[i].text
            point['lat'] = lats[j].text
            route.append(point)
            
            pnt = Point(float(lngs[i].text),float(lats[j].text))
                        
            multiline.append(pnt)
            
            i=i+1
            j=i+1
        
#        if type == 'geofence':
#            ls = LineString(multiline)
#            return HttpResponse(ls.wkt)
#        
#        else:
        print route
        json = simplejson.dumps(route)
        return HttpResponse(json, mimetype='application/json')
        
    #return 'ae'

def Maploader(request):
    
    ticket = "awFhbDzHd0vJaWVAzwkLyC9gf0LhbM9CyxSLyCH8aTphbIOidIZHdWOLyCtq"
    
    url = "webservices.apontador.com.br"
    
    xml = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><getMap xmlns="http://webservices.maplink2.com.br"><routeId>string</routeId><extent><XMin>-49.2962338995702</XMin><YMin>-25.4429948584803</YMin><XMax>-43.2075</XMax><YMax>-22.902778</YMax></extent><mo><scaleBar>true</scaleBar><mapSize><width>600</width><height>600</height></mapSize><showPoint>false</showPoint><icon><Icon><iconType>int</iconType><iconID>int</iconID><point xsi:nil="true" /></Icon><Icon><iconType>int</iconType><iconID>int</iconID><point xsi:nil="true" /></Icon></icon></mo><token>'+ticket+'</token></getMap></soap:Body></soap:Envelope>'
    conn = httplib.HTTPConnection(url,timeout=5)
    headers = {"Content-type":"text/xml; charset=\"UTF-8\"","Host":"teste.webservices.apontador.com.br"}
    conn.request("POST", "/webservices/v3/MapRender/MapRender.asmx", xml, headers)
    response = conn.getresponse()
    conteudo = response.read()
    print conteudo
    conn.close()
    
    
    return 'ae'

def Geocode(array):    

    ticket = "awFhbDzHd0vJaWVAzwkLyC9gf0LhbM9CyxSLyCH8aTphbIOidIZHdWOLyCtq"
    
    url = "webservices.apontador.com.br"
    
    results = []
        
    for a in array:
        city = array[a]['city']
        state = array[a]['state']
        number = array [a]['number']
        street = array[a]['address']
        
        xml = '<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><getXY xmlns="http://webservices.maplink2.com.br"><address><street>'+street+'</street><houseNumber>'+str(number)+'</houseNumber><zip></zip><district></district><city><name>'+city+'</name><state>'+state+'</state></city></address><token>'+ticket+'</token></getXY></soap12:Body></soap12:Envelope>'
    
        conn = httplib.HTTPConnection(url,timeout=3)
        headers = {"Content-type":"text/xml; charset=\"UTF-8\"","Host":"teste.webservices.apontador.com.br"}
        conn.request("POST", "/webservices/v3/AddressFinder/AddressFinder.asmx", xml, headers)
        response = conn.getresponse()
        conteudo = response.read()
        conn.close()
        
        #<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><getMapResponse xmlns="http://webservices.maplink2.com.br"><getMapResult><url>http://teste.webservices.maplink2.com.br/output/</url><extent><XMin>-49.2962339</XMin><YMin>-26.94037873</YMin><XMax>-43.2075</XMax><YMax>-21.356430578</YMax></extent></getMapResult></getMapResponse></soap:Body></soap:Envelope>
    
        if response.status == 200:
            gxml = ElementTree.fromstring(conteudo)
            
            lng = gxml.find(".//{http://webservices.maplink2.com.br}x")
            lat = gxml.find(".//{http://webservices.maplink2.com.br}y")
            
            try:
                c = CachedGeocode.objects.get(Q(lng=lng.text) & Q(lat=lat.text))
            
            except ObjectDoesNotExist:    
                c = CachedGeocode(
                    lat = float(lat.text),
                    lng = float(lng.text),
                    full_address = "",
                    number = number,
                    street = title(lower(smart_str(street, encoding='utf-8', strings_only=False, errors='strict'))),
                    city = title(smart_str(city, encoding='utf-8', strings_only=False, errors='strict')),
                    state = state,
                    country = "Brasil",
                    #postal_code = postal.text,
                    #administrative_area = title(lower(address[0].get("Bairro")))
                )
        
                c.full_address = smart_str(c.street, encoding='utf-8', strings_only=False, errors='strict')+" "+str(c.number)+", "+smart_str(c.city, encoding='utf-8', strings_only=False, errors='strict')+", "+str(c.state)
                try:
                    c.save()
                except:
                    pass
            except MultipleObjectsReturned:
                c = CachedGeocode.objects.filter(Q(lng=lng.text) & Q(lat=lat.text))[0]
    
            result = {}
            result['lng'] = lng.text
            result['lat'] = lat.text
            results.append(result)
            
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
    

def ReverseGeocode(lat,lng):
    #first,tries to search in the database the lat lng pair
    try:
        c = CachedGeocode.objects.get(Q(lng=lng) & Q(lat=lat))
        
        #return a list with first element being the full address, the second the city and the third the administrative area.
        return [unicode(c.full_address),unicode(c.street)+" "+unicode(c.number)+", "+unicode(c.administrative_area),unicode(c.city),unicode(c.state),unicode(c.postal_code)]
    except ObjectDoesNotExist:
        try:
            return MaplinkRGeocode(lat,lng)
        except:
            #fails silently returning empty strings
            return [str(lat)+","+str(lng),str(lat)+","+str(lng),"","",""]
            
def MultispectralRGeocode(lat,lng):
    ticket = "76333D50-F9F4-4088-A9D7-DE5B09F9C27C"
    url  = "http://www.geoportal.com.br/xgeocoder/cxinfo.aspx?x="+lng+"&y="+lat+"&Ticket="+str(ticket)
    page = urllib.urlopen(url)
    conteudo = page.read()
    page.close()
    geocodexml = ElementTree.fromstring(conteudo)
    address = geocodexml.findall("INFO")
     #self.stdout.write(address[0].text+","+address[0].get("NroIni")+"-"+address[0].get("NroFim")+","+address[0].get("Bairro")+","+address[1].text+"-"+address[2].text+","+address[0].get("CEP"))
    if (address != []):
        c = CachedGeocode(
            lat = float(lat),
            lng = float(lng),
            full_address = "",
            number = address[0].get("NroIni")+"-"+address[0].get("NroFim"),
            street = title(lower(address[0].text)),
            city = title(lower(address[1].text)),
            state = address[2].text,
            country = "Brasil",
            postal_code = address[0].get("CEP"),
            administrative_area = title(lower(address[0].get("Bairro")))
        )
        c.full_address = c.street+" "+c.number+", "+c.administrative_area+" - "+c.city+", "+c.state
        c.save()
        
        return [c.full_address,c.street+" "+c.number+", "+c.administrative_area,c.city,c.state,c.postal_code]
    else: 
        raise NotImplementedError

    
def GoogleGeocode(lat,lng):
    result = Geocoder.reverse_geocode(float(lat),float(lng))
    #raise NotImplementedError
    #print
    #addr = unicode(result[0])

def MaplinkRGeocode(lat,lng):
    
    ticket = "awFhbDzHd0vJaWVAzwkLyC9gf0LhbM9CyxSLyCH8aTphbIOidIZHdWOLyCtq"
    
    url = "webservices.apontador.com.br"
    
    xml = '''<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><getAddress xmlns="http://webservices.maplink2.com.br"><point><x>'''+str(lng)+'''</x><y>'''+str(lat)+'''</y></point><token>'''+str(ticket)+'''</token><tolerance>'''+str(10)+'''</tolerance></getAddress></soap:Body></soap:Envelope>'''

    conn = httplib.HTTPConnection(url,timeout=3)
    headers = {"Content-type":"text/xml; charset=\"UTF-8\"","SOAPAction":"http://webservices.maplink2.com.br/getAddress","Host":"teste.webservices.apontador.com.br"}
    
    try:
        conn.request("POST", "/webservices/v3/AddressFinder/AddressFinder.asmx", xml, headers)
        response = conn.getresponse()
        conteudo = response.read()
        conn.close()
       
    except:
      raise NotImplementedError

    if response.status == 200:
        print conteudo
        gxml = ElementTree.fromstring(conteudo)
        
        street = gxml.find(".//{http://webservices.maplink2.com.br}street")
        city = gxml.find(".//{http://webservices.maplink2.com.br}name")
        state = gxml.find(".//{http://webservices.maplink2.com.br}state")
        number = gxml.find(".//{http://webservices.maplink2.com.br}houseNumber")
        postal = gxml.find(".//{http://webservices.maplink2.com.br}zip")
        
        c = CachedGeocode(
            lat = float(lat),
            lng = float(lng),
            full_address = "",
            number = number.text,
            street = title(lower(street.text)),
            city = title(city.text),
            state = state.text,
            country = "Brasil",
            postal_code = postal.text,
            #administrative_area = title(lower(address[0].get("Bairro")))
        )
    
        c.full_address = c.street+" "+c.number+", "+c.city+", "+c.state
        
        c.save()
    
        return [c.full_address,c.street+" "+c.number,c.city,c.state,c.postal_code]
        #raise NotImplementedError
    else:
      print conteudo
            #
    #except:
    #    raise NotImplementedError
    
    
    
        #print response.status, response.reason, response.read()
        
    
