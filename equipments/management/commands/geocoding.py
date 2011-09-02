# -*- coding: utf-8 -*-
import urllib
import sys, httplib,urllib
import time
from xml.etree import cElementTree as ElementTree

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import lower,title
from django.utils.encoding import smart_str
from django.utils import simplejson
from django.http import HttpResponseRedirect, HttpResponse

from itrack.pygeocoder import Geocoder
from itrack.geocodecache.models import CachedGeocode

def Routecalc(request):
    
    ticket = "awFhbDzHd0vJaWVAzwkLyC9gf0LhbM9CyxSLyCH8aTphbIOidIZHdWOLyCtq"
    
    url = "teste.webservices.apontador.com.br"
    
    x0 = "-49.2411452173913"
    y0 = "-25.4008260869565"
    
    x1 = "-49.2499139449541"
    y1 = "-25.5094316513761"
    
    xml = '''
  
      <rs>
        <RouteStop>
          <description>Nicaragua</description>
          <point>
            <x>'''+x0+'''</x>
            <y>'''+y0+'''</y>
          </point>
        </RouteStop>
        <RouteStop>
          <description>Henrique Martins Torres</description>
          <point>
            <x>'''+x1+'''</x>
            <y>'''+y1+'''</y>
          </point>
        </RouteStop>
      </rs>
      <ro>
        <language>portugues</language>
        <routeDetails>
          <descriptionType>0</descriptionType>
          <routeType>0</routeType>
          <optimizeRoute>false</optimizeRoute>
          <poiRoute>
            <string></string>
            <string></string>
          </poiRoute>
          <barriersList>
            <string></string>
            <string></string>
          </barriersList>
          <barrierPoints>
            <Point xsi:nil="true" />
            <Point xsi:nil="true" />
          </barrierPoints>
        </routeDetails>
        <vehicle>
          <tankCapacity>64</tankCapacity>
          <averageConsumption>10</averageConsumption>
          <fuelPrice>2.15</fuelPrice>
          <averageSpeed>70</averageSpeed>
          <tollFeeCat>2</tollFeeCat>
        </vehicle>
        <routeLine>
          <RouteLine>
            <width></width>
            <RGB></RGB>
            <transparency></transparency>
          </RouteLine>
          <RouteLine>
            <width></width>
            <RGB></RGB>
            <transparency></transparency>
          </RouteLine>
        </routeLine>
      </ro>
      <token>'''+ticket+'''</token>
    </getRoute>
  </soap12:Body>
</soap12:Envelope>
'''
    
    xml = xml.replace('\n','').replace(' ','')
    
    begin = '<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><getRoute xmlns="http://webservices.maplink2.com.br">'
    xml = begin + xml 
    
    print xml
    
    conn = httplib.HTTPConnection(url,timeout=5)
    headers = {"Content-type":"application/soap+xml; charset=\"UTF-8\"","Host":"teste.webservices.apontador.com.br"}
    conn.request("POST", "/webservices/v3/Route/Route.asmx", xml, headers)
    response = conn.getresponse()
    conteudo = response.read()
    conn.close()
    
    print conteudo
    
    return 'ae'

def Maploader(request):
    
    ticket = "awFhbDzHd0vJaWVAzwkLyC9gf0LhbM9CyxSLyCH8aTphbIOidIZHdWOLyCtq"
    
    url = "teste.webservices.apontador.com.br"
    
    xml = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><getMap xmlns="http://webservices.maplink2.com.br"><routeId>string</routeId><extent><XMin>-49.2962338995702</XMin><YMin>-25.4429948584803</YMin><XMax>-43.2075</XMax><YMax>-22.902778</YMax></extent><mo><scaleBar>true</scaleBar><mapSize><width>600</width><height>600</height></mapSize><showPoint>false</showPoint><icon><Icon><iconType>int</iconType><iconID>int</iconID><point xsi:nil="true" /></Icon><Icon><iconType>int</iconType><iconID>int</iconID><point xsi:nil="true" /></Icon></icon></mo><token>'+ticket+'</token></getMap></soap:Body></soap:Envelope>'
    conn = httplib.HTTPConnection(url,timeout=5)
    headers = {"Content-type":"text/xml; charset=\"UTF-8\"","Host":"teste.webservices.apontador.com.br"}
    conn.request("POST", "/webservices/v3/MapRender/MapRender.asmx", xml, headers)
    response = conn.getresponse()
    print response.status, response.reason, response.read()
    conteudo = response.read()
    conn.close()
    
    print conteudo
    
    return 'ae'

def Geocode(street,number,city,state):

    ticket = "awFhbDzHd0vJaWVAzwkLyC9gf0LhbM9CyxSLyCH8aTphbIOidIZHdWOLyCtq"
    
    url = "teste.webservices.apontador.com.br"
    
    xml = '<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><getXY xmlns="http://webservices.maplink2.com.br"><address><street>'+street+'</street><houseNumber>'+str(number)+'</houseNumber><zip></zip><district></district><city><name>'+city+'</name><state>'+state+'</state></city></address><token>'+ticket+'</token></getXY></soap12:Body></soap12:Envelope>'

    conn = httplib.HTTPConnection(url,timeout=5)
    headers = {"Content-type":"text/xml; charset=\"UTF-8\"","Host":"teste.webservices.apontador.com.br"}
    conn.request("POST", "/webservices/v3/AddressFinder/AddressFinder.asmx", xml, headers)
    response = conn.getresponse()
    #print response.status, response.reason, response.read()
    #print response.status
    print "\n"
    conteudo = response.read()
    conn.close()
    
    #<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><getMapResponse xmlns="http://webservices.maplink2.com.br"><getMapResult><url>http://teste.webservices.maplink2.com.br/output/</url><extent><XMin>-49.2962339</XMin><YMin>-26.94037873</YMin><XMax>-43.2075</XMax><YMax>-21.356430578</YMax></extent></getMapResult></getMapResponse></soap:Body></soap:Envelope>

    
    if response.status == 200:
        print conteudo
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
        
            c.save()

        result = {}
        result['lng'] = lng.text
        result['lat'] = lat.text
        json = simplejson.dumps(result)
        return HttpResponse(json, mimetype='application/json')
    
    return 'ae'

def ReverseGeocode(lat,lng):
    #first,tries to search in the database the lat lng pair
    try:
        c = CachedGeocode.objects.get(Q(lng=lng) & Q(lat=lat))
        
        #return a list with first element being the full address, the second the city and the third the administrative area.
        return [c.full_address,c.street+" "+c.number+", "+c.administrative_area,c.city,c.state,c.postal_code]
    except ObjectDoesNotExist:
        #tries to reverse geocode by google
        try:
            return GoogleGeocode(lat,lng)
        except NotImplementedError:
            #tries to reverse geocode by multispectral
            try:
                return MultispectralRGeocode(lat,lng)
            except NotImplementedError:
                #tries to reverse geocode by maplink
                try:
                    return MaplinkRGeocode(lat,lng)
                except NotImplementedError:
                    #fails silently returning empty strings
                    return [str(lat)+","+str(lng),"","",""]
            
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
        return [str(lat)+","+str(lng),str(lat)+","+str(lng),"","",""]

    
def GoogleGeocode(lat,lng):
    #result = Geocoder.reverse_geocode(lat,lng)
    raise NotImplementedError
    #print
    #addr = unicode(result[0])

def MaplinkRGeocode(lat,lng):
    
    ticket = "awFhbDzHd0vJaWVAzwkLyC9gf0LhbM9CyxSLyCH8aTphbIOidIZHdWOLyCtq"
    
    url = "teste.webservices.apontador.com.br"
    
    xml = '''<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><getAddress xmlns="http://webservices.maplink2.com.br"><point><x>'''+str(lng)+'''</x><y>'''+str(lat)+'''</y></point><token>'''+str(ticket)+'''</token><tolerance>'''+str(10)+'''</tolerance></getAddress></soap:Body></soap:Envelope>'''

    conn = httplib.HTTPConnection(url,timeout=10)
    headers = {"Content-type":"text/xml; charset=\"UTF-8\"","SOAPAction":"http://webservices.maplink2.com.br/getAddress","Host":"teste.webservices.apontador.com.br"}
    conn.request("POST", "/webservices/v3/AddressFinder/AddressFinder.asmx", xml, headers)
    response = conn.getresponse()
    #print response.status, response.reason, response.read()
    print response.status
    print "\n"
    conteudo = response.read()
    conn.close()
   
    #conteudo = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><getAddressResponse xmlns="http://webservices.maplink2.com.br"><getAddressResult><key /><address><street>Estr dos Cunha</street><houseNumber>768</houseNumber><zip>13860-000</zip><district /><city><name>Aguaí</name><state>SP</state></city></address><zipL>13860-000</zipL><zipR>13860-000</zipR><carAccess>true</carAccess><dataSource /><point><x>-47.000186</x><y>-22.021521</y></point></getAddressResult></getAddressResponse></soap:Body></soap:Envelope>'
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
    
        return [c.full_address,c.street+" "+c.number+", "+c.city,c.state,c.postal_code]


    else:
        return [str(lat)+","+str(lng),str(lat)+","+str(lng),"","",""]
    
