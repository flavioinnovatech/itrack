# -*- coding: utf-8 -*-
import urllib
import sys, httplib,urllib
import time
from xml.etree import cElementTree as ElementTree

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import lower,title

from itrack.pygeocoder import Geocoder
from itrack.geocodecache.models import CachedGeocode

def Geocode(address):

    
    

    return (0,0)

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
    
