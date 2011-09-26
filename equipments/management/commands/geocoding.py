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
    
    x0 = "-49.2411452173913"
    y0 = "-25.4008260869565"
    
    x1 = "-49.2499139449541"
    y1 = "-25.5094316513761"
    
    xml = '<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><getRoute xmlns="http://webservices.maplink2.com.br"><rs><RouteStop><description>origem</description><point><x>'+x0+'</x><y>'+y0+'</y></point></RouteStop><RouteStop><description>destino</description><point><x>'+x1+'</x><y>'+y1+'</y></point></RouteStop></rs><ro><language>string</language><routeDetails><descriptionType>0</descriptionType><routeType>0</routeType><optimizeRoute>false</optimizeRoute></routeDetails><vehicle></vehicle><routeLine></routeLine></ro><token>'+ticket+'</token></getRoute></soap12:Body></soap12:Envelope>'
    
    '''    
    conn = httplib.HTTPConnection(url,timeout=5)
    headers = {"Content-type":"application/soap+xml; charset=\"UTF-8\"","Host":"teste.webservices.apontador.com.br"}
    conn.request("POST", "/webservices/v3/Route/Route.asmx", xml, headers)
    response = conn.getresponse()
    conteudo = response.read()
    conn.close()
    
    print response.status, response.reason
    #print conteudo
    '''
    
    #### DEBUGGING
    conteudo = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><getRouteResponse xmlns="http://webservices.maplink2.com.br"><getRouteResult><routeId>192.168.3.96_34751356f23d4c47afce2b2948ce1074</routeId><MapInfo><url /><extent><XMin>-49.26025</XMin><YMin>-25.50943</YMin><XMax>-49.23368</XMax><YMax>-25.40083</YMax></extent></MapInfo><segDescription><SegmentDescription><command>Início da rota</command><description>origem</description><city><name /><state /></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><distance>0</distance><cumulativeDistance>0</cumulativeDistance><point><x>-49.24115</x><y>-25.40083</y></point></SegmentDescription><SegmentDescription><command>Turn Left</command><description>R. Nicarágua</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>0.6</distance><cumulativeDistance>0.6</cumulativeDistance><point><x>-49.24598</x><y>-25.40399</y></point></SegmentDescription><SegmentDescription><command>Continue</command><description>Av. Ns. da Luz</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>3</distance><cumulativeDistance>3.6</cumulativeDistance><point><x>-49.24176</x><y>-25.42769</y></point></SegmentDescription><SegmentDescription><command>Turn Left</command><description>Av. Mal. Humberto de A C Branco</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>1.18</distance><cumulativeDistance>4.78</cumulativeDistance><point><x>-49.23531</x><y>-25.43642</y></point></SegmentDescription><SegmentDescription><command>Bear Right</command><description>R. Gov. Agamenon Magalhães</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>0.1</distance><cumulativeDistance>4.88</cumulativeDistance><point><x>-49.23436</x><y>-25.43626</y></point></SegmentDescription><SegmentDescription><command>Bear Right</command><description>Ac. P/ Rod BR-116</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>0.03</distance><cumulativeDistance>4.91</cumulativeDistance><point><x>-49.2341</x><y>-25.4364</y></point></SegmentDescription><SegmentDescription><command>Turn Right</command><description>Rod. Régis Bittencourt</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>PD</roadType><distance>5.27</distance><cumulativeDistance>10.18</cumulativeDistance><point><x>-49.25843</x><y>-25.47414</y></point></SegmentDescription><SegmentDescription><command>Turn Left</command><description>R. Antônio Bariquelo</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>0.12</distance><cumulativeDistance>10.3</cumulativeDistance><point><x>-49.25944</x><y>-25.4735</y></point></SegmentDescription><SegmentDescription><command>Turn Left</command><description>R. Omílio Monteiro Soares</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>0.14</distance><cumulativeDistance>10.44</cumulativeDistance><point><x>-49.26025</x><y>-25.4745</y></point></SegmentDescription><SegmentDescription><command>Continue</command><description>R. Roberto Faria</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>0.12</distance><cumulativeDistance>10.56</cumulativeDistance><point><x>-49.25931</x><y>-25.4752</y></point></SegmentDescription><SegmentDescription><command>Continue</command><description>Acesso</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>0.07</distance><cumulativeDistance>10.63</cumulativeDistance><point><x>-49.25872</x><y>-25.47557</y></point></SegmentDescription><SegmentDescription><command>Turn Left</command><description>R. Oliveira Viana</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>0.05</distance><cumulativeDistance>10.68</cumulativeDistance><point><x>-49.25829</x><y>-25.47585</y></point></SegmentDescription><SegmentDescription><command>Turn Right</command><description>R. Sônia Maria</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>0.13</distance><cumulativeDistance>10.81</cumulativeDistance><point><x>-49.25712</x><y>-25.47537</y></point></SegmentDescription><SegmentDescription><command>Turn Right</command><description>R. Prf. João Soares Barcelos</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>3.64</distance><cumulativeDistance>14.45</cumulativeDistance><point><x>-49.24245</x><y>-25.50537</y></point></SegmentDescription><SegmentDescription><command>Turn Left</command><description>R. Waldemar Loureiro Campos</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>0.87</distance><cumulativeDistance>15.32</cumulativeDistance><point><x>-49.25034</x><y>-25.50853</y></point></SegmentDescription><SegmentDescription><command>Continue</command><description>R. Henrique Martins Torres</description><city><name>Curitiba</name><state>PR</state></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><roadType>P</roadType><distance>0.11</distance><cumulativeDistance>15.43</cumulativeDistance><point><x>-49.24992</x><y>-25.50943</y></point></SegmentDescription><SegmentDescription><command>Fim da rota</command><description>destino</description><city><name /><state /></city><tollFeeDetails><price>0</price><pricePerAxle>0</pricePerAxle></tollFeeDetails><distance>0</distance><cumulativeDistance>15.43</cumulativeDistance><point><x>-49.24991</x><y>-25.50943</y></point></SegmentDescription></segDescription><routeTotals><totalDistance>15.43</totalDistance><totalTime>PT1H1M</totalTime><totalFuelUsed>0</totalFuelUsed><totaltollFeeCost>0</totaltollFeeCost><totalfuelCost>0</totalfuelCost><totalCost>0</totalCost><taxiFare1>31.27</taxiFare1><taxiFare2>35.9</taxiFare2></routeTotals><routeSummary><RouteSummary><description>origem</description><distance>0</distance><point><x>-49.24115</x><y>-25.40083</y></point></RouteSummary><RouteSummary><description>destino</description><distance>15.43</distance><point><x>-49.24991</x><y>-25.50943</y></point></RouteSummary></routeSummary><roadType><twoLaneHighway>5.27</twoLaneHighway><secondLaneUnderConstruction>0</secondLaneUnderConstruction><oneLaneRoadway>10.159999999999998</oneLaneRoadway><pavingWorkInProgress>0</pavingWorkInProgress><dirtRoad>0</dirtRoad><roadwayInPoorConditions>0</roadwayInPoorConditions><ferry>0</ferry></roadType></getRouteResult></getRouteResponse></soap:Body></soap:Envelope>'

    if (1):
    #if response.status == 200:
        
        #TODO: Needs cached geocode here
    
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
        
        if type == 'geofence':
            ls = LineString(multiline)

        
        else:
            json = simplejson.dumps(route)
            return HttpResponse(json, mimetype='application/json')
        
    return 'ae'

def Maploader(request):
    
    ticket = "awFhbDzHd0vJaWVAzwkLyC9gf0LhbM9CyxSLyCH8aTphbIOidIZHdWOLyCtq"
    
    url = "webservices.apontador.com.br"
    
    xml = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><getMap xmlns="http://webservices.maplink2.com.br"><routeId>string</routeId><extent><XMin>-49.2962338995702</XMin><YMin>-25.4429948584803</YMin><XMax>-43.2075</XMax><YMax>-22.902778</YMax></extent><mo><scaleBar>true</scaleBar><mapSize><width>600</width><height>600</height></mapSize><showPoint>false</showPoint><icon><Icon><iconType>int</iconType><iconID>int</iconID><point xsi:nil="true" /></Icon><Icon><iconType>int</iconType><iconID>int</iconID><point xsi:nil="true" /></Icon></icon></mo><token>'+ticket+'</token></getMap></soap:Body></soap:Envelope>'
    conn = httplib.HTTPConnection(url,timeout=5)
    headers = {"Content-type":"text/xml; charset=\"UTF-8\"","Host":"teste.webservices.apontador.com.br"}
    conn.request("POST", "/webservices/v3/MapRender/MapRender.asmx", xml, headers)
    response = conn.getresponse()
    conteudo = response.read()
    conn.close()
    
    
    return 'ae'

def Geocode(street,number,city,state):

    ticket = "awFhbDzHd0vJaWVAzwkLyC9gf0LhbM9CyxSLyCH8aTphbIOidIZHdWOLyCtq"
    
    url = "webservices.apontador.com.br"
    
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
        json = simplejson.dumps(result)
        return HttpResponse(json, mimetype='application/json')
    
    return 'ae'

def ReverseGeocode(lat,lng):
    #first,tries to search in the database the lat lng pair
    try:
        c = CachedGeocode.objects.get(Q(lng=lng) & Q(lat=lat))
        
        #return a list with first element being the full address, the second the city and the third the administrative area.
        return [unicode(c.full_address),unicode(c.street)+" "+unicode(c.number)+", "+unicode(c.administrative_area),unicode(c.city),unicode(c.state),unicode(c.postal_code)]
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
    result = Geocoder.reverse_geocode(lat,lng)
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
        
    
