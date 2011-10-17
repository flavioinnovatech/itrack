# -*- coding: utf-8 -*-
# Create your views here.
import csv,codecs, StringIO
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import simpleSplit

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from itrack.reports.forms import ReportForm
from itrack.equipments.models import CustomFieldName, Tracking, TrackingData
from itrack.system.models import System
from itrack.vehicles.models import Vehicle
from itrack.system.tools import lowestDepth,findParents,findChild,serializeChild,findChildInstance
from itrack.pygeocoder import Geocoder

import math


class UnicodeWriter(object):
   
    def __init__(self, f, dialect=csv.excel_tab, encoding="utf-16", **kwds):
        # Redirect output to a queue
        self.queue = StringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoding = encoding
    
    def writerow(self, row):
        # Modified from original: now using unicode(s) to deal with e.g. ints
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = data.encode(self.encoding)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)
    
    def writerowxml(self, row) :
        # Modified from original: now using unicode(s) to deal with e.g. ints
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = data.encode(self.encoding)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

API_KEY = 'ABQIAAAAOV9qRRxejMi2WeW2TanAKhTefegWErZP_EhBh-or-xYREOhaRBSYXJPqI_-2MwMOsGwqcYel72Q_Qw'

VEHICLE_CHOICES = (("license_plate","Placa"),("date",u"Data"),("type",u"Tipo de veículo"),("address",u"Endereço"),("system",u"Sistema"),("color",u"Cor"),("year",u"Ano"),("model",u"Modelo"),("manufacturer",u"Fabricante"),("chassi",u"Chassi"))


def geoDistance(lat1,lon1,lat2,lon2):

    dla1 = math.floor(lat1)
    mla1 = math.floor(((lat1)-dla1)*60)
    sla1 = math.floor( ( ((lat1-dla1)*60) - mla1 )*60 )
    
    print(str(dla1) + ":" + str(mla1) + ":" + str(sla1))
    
    
    dlo1 = math.floor(lon1)
    mlo1 = math.floor(((lon1)-dlo1)*60)
    slo1 = math.floor( ( ((lon1-dlo1)*60) - mlo1 )*60 )
    
    print(str(dlo1) + ":" + str(mlo1) + ":" + str(slo1))
    
    dla2 = math.floor(lat2)
    mla2 = math.floor(((lat2)-dla2)*60)
    sla2 = math.floor( ( ((lat2-dla2)*60) - mla2 )*60 )
    
    print(str(dla2) + ":" + str(mla2) + ":" + str(sla2))
    
    dlo2 = math.floor(lon2)
    mlo2 = math.floor(((lon2)-dlo2)*60)
    slo2 = math.floor( ( ((lon2-dlo2)*60) - mlo2 )*60 )
    
    print(str(dlo2) + ":" + str(mlo2) + ":" + str(slo2))
    
    
    
    lat1 = dla1 + mla1/60 + sla1/3600
    lon1 = dlo1 + mlo1/60 + slo1/3600
    lat2 = dla2 + mla2/60 + sla2/3600
    lon2 = dlo2 + mlo2/60 + slo2/3600
    
    
    #padronizado
    
    rad_lat1 = (lat1)*math.pi/180
    rad_lon1 = (lon1)*math.pi/180
    
    rad_lat2 = (lat2)*math.pi/180
    rad_lon2 = (lon2)*math.pi/180
     
     
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)*math.sin(dlat/2)+math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)*math.sin(dlon/2)
    
    # verify this
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    
    d = 6371 *c # (Raio da terra) * c
    return d
    
def firstRowTitles(item):
    pos = [x[0] for x in VEHICLE_CHOICES].index(item)
    return VEHICLE_CHOICES[pos][1]


def checkready(request):
    return HttpResponse("<?xml version=\"1.0\" encoding=\"utf-8\"?><status>"+request.session.get('download','wait')+"</status>", mimetype='text/xml')
@csrf_exempt
def report(request,offset):
    request.session['download'] = 'wait'
    no_information = 0
    
    if request.method != 'POST':
        form = ReportForm(int(offset))
    else:

        try:
            
            if request.POST.has_key("vehicle_other"):
                #print("# TESTE 001 ");
                v = Vehicle.objects.get(license_plate=request.POST["vehicle"])
                request.POST["vehicle"] = str(v.id)
        except ObjectDoesNotExist:
            #print("# TESTE 004 ");
            pass
        form = ReportForm(int(offset),request.POST)    
        #print("# TESTE 005 ");

        if form.is_valid():
            #print("# TESTE 006 ");
            system = request.session["system"]
            s = System.objects.get(pk=system)
            parents = findParents(s,[s])
            parents = serializeChild(findChild(system),[])
            print parents
            d1 = datetime.now()
            #TODO: A business logic pra cá ficou assim:
            #TODO: criar campo indicando se o veículo foi deletado no model do veículo, e sumir com os veículos apagados
            #TODO: apenas por esse campo. Aqui vamos ter a busca sem checar esse campo, assim o sistema pode consultar infos
            #TODO: antigas sobre os veículos que ele não mais usa. Além disso, sistemas apagados só podem ter suas
            #TODO: informações vistas pelo sistema root. Não esquecer de checar qual sistema está vendo a informação, e pegar
            #TODO: trackings apenas para o sistema logado.            
            try:
#                form.cleaned_data["vehicle"]
                vehicle = Vehicle.objects.get(pk=int(request.POST["vehicle"]))
            except:
                #print("# TESTE 013 ")
                if request.POST['type'] == 'HTML':
                    no_information = 1
                    request.session['download'] = 'done'
                    message = "Veiculo não encontrado."
                    return render_to_response("reports/templates/htmlreporterror.html",locals(),context_instance=RequestContext(request),)                    
                else:
                    no_information = 1
                    request.session['download'] = 'done'
                    return render_to_response("reports/templates/form.html",locals(),context_instance=RequestContext(request),)
            #print("# TESTE 014 ");            
            if s.parent == None:
                #print("# TESTE 015 ")
                equip_system = s.name
                trackings = Tracking.objects.filter(
                    Q(eventdate__gte=form.cleaned_data['period_start'])  
                    &Q(eventdate__lte=form.cleaned_data['period_end'])
                    &(
                        Q(trackingdata__type__type = 'Vehicle')
                        &Q(trackingdata__value = vehicle.id)
                    )
                )
                #print("# TESTE 016 ")
            else:
                #print("# TESTE 017 ")
                equip_system = lowestDepth(vehicle.equipment.system.all()).name
                #print vehicle.id
                trackings = Tracking.objects.filter(
                    Q(eventdate__gte=form.cleaned_data['period_start'])  
                    &Q(eventdate__lte=form.cleaned_data['period_end'])
                    &(
                        Q(trackingdata__type__type = 'Vehicle')
                        &Q(trackingdata__value = vehicle.id)
                     )   
                ).filter( #extra filter for the system
                    Q(trackingdata__type__type = 'System')
                    &Q(trackingdata__value__in = parents)
                )
            
            if trackings.count() == 0:
                #print("# TESTE 018 ")
                if request.POST['type'] == 'HTML':
                    no_information = 1
                    message = "Não foram encontrados dados para a busca realizada."
                    request.session['download'] = 'done'
                    return render_to_response("reports/templates/htmlreporterror.html",locals(),context_instance=RequestContext(request),)                    
                else:
                    no_information = 1
                    request.session['download'] = 'done'
                    return render_to_response("reports/templates/form.html",locals(),context_instance=RequestContext(request),)
            #print("# TESTE 019 ")

            request.session['download'] = 'started'
            datas = TrackingData.objects.select_related('tracking').filter(Q(tracking__in=trackings))

            #print("# TESTE 020 ")
            tdata_dict = {}
            for tdata in datas:
                tdata_dict.setdefault(tdata.tracking.eventdate, []).append(tdata)
            
            d2 = datetime.now()
            #print tdata_dict
            
            #initializing the resources that are going to be used to mount the table
            table_content = []
            list_table = []
            

                
            try:
                #print(form.cleaned_data["vehicle_fields"])
                #print(request.POST.getlist("vehicle_fields"))
                #print(form.cleaned_data["fields"])
                #print(request.POST.getlist("fields"))
                #custom fields
                display_fields = map(lambda x: x.custom_field,
                    form.cleaned_data["fields"])
                
                #custom fields names
                display_fields2 = map(lambda x: x, 
                    form.cleaned_data["fields"])
                
            except Exception as err:
                #print(err.args)
                pass
                
            try:
                tmp_x = map(lambda x: unicode(x),display_fields)
                title_row = map(lambda x: firstRowTitles(str(x)), 
                    form.cleaned_data['vehicle_fields']) +  tmp_x
                    
            except Exception as err:
                #print(err.args)
                pass
                
            if request.POST['type'] == 'CSV':
                #print("# TESTE 022 ")
                #main loop for each tracking found
                for title_col in title_row:
                    print("HTML* :" + unicode(title_col).encode("utf-8"))
                response = HttpResponse(mimetype='text/csv')
                response['Content-Disposition'] = 'attachment; filename=report.csv'
                response.set_cookie("fileDownloadToken", request.POST['token'])    
                count = 0
                mount2 = ""
                #print("# TESTE 023 ")
                try:
                    for title_col in title_row:
                        mount2 += "\t" if count > 0 else ""
                        mount2 += unicode(title_col).encode("UTF-16")[2:]
                        count += 1
                except Exception as err:
                    print(err.args)
                #print("# TESTE 024 ")
                mount2 += "\r\n"
                response.write(mount2)
                #print(mount2)
                
                for date, tdata in tdata_dict.items():
                    #print("# TESTE 025 ")
                    item = {}
                    output_list = []
                    mount = ""
                    try:
                        addrs = [x.value for x in sorted(tdata,key=lambda d: d.type.name) if x.type.type == 'Geocode']
                        addrs = unicode(addrs[2]+" - "+addrs[1]+", "+addrs[3]+" - "+addrs[0]).encode("UTF-16")[2:]
                    except:
                        try:
                            addrs = str(addrs[2]+" - "+addrs[1]+", "+addrs[3]+" - "+addrs[0]).encode("UTF-16")[2:]
                        except:
                            addrs = ""
                    #print("# TESTE 026 ")
                    count = 0
                    for data in form.cleaned_data['vehicle_fields']:
                        #print("# TESTE 027 ")
                        #print(data)
                        try:
                            if data != "address" and data != "date" and data !="system":
                                try:
                                    tmp = ""
                                    tmp += "\t" if count > 0 else ""
                                    count += 1
                                    tmp += unicode(vehicle.__dict__[unicode(data)]).encode("UTF-16")[2:]
                                    mount += tmp
                                except Exception as err:
                                    #print(err.args)
                                    pass
                            elif data == "date":
                                mount += "\t" if count > 0 else ""
                                mount += str(date)
                                count += 1
                            elif data == "system":
                                mount += "\t" if count > 0 else ""
                                mount += str(equip_system)
                                count += 1
                            elif data == "address":
                                mount += "\t" if count > 0 else ""
                                mount += str(addrs)
                                count += 1
                        except Exception as err:
                            #print(err.args)
                            raise err
                    
                    for x in display_fields:
                        #print("# TESTE 028 ")
                        topush = "OFF"
                        for y in tdata:
                            if y.type == x:
                                topush = "ON"
                        mount += "\t" if count > 0 else ""
                        mount += str(topush)
                        count += 1
                    mount += "\r\n"
                    response.write(mount)
                    #print("# TESTE 029 ")
                    #print(mount)
                #print("# TESTE 030 ")
                request.session['download'] = 'done'
                return response

                
            elif request.POST['type'] == 'HTML':
                for title_col in title_row:
                    print("HTML* :" + unicode(title_col).encode("utf-8"))
                    
                request.session['download'] = 'done'
                response = HttpResponse(mimetype='text/xml')
                response.set_cookie("fileDownloadToken", request.POST['token'])    
                response.write("<?xml version=\"1.0\" encoding=\"utf-8\"?><?xml-stylesheet type=\"text/xsl\" href=\"/media/xslt/report.xsl\"?><document>")

                str_placa = ""
                str_tipo = ""
                str_cor = ""
                str_ano = ""
                str_modelo = ""
                str_marca = ""
                str_chassi = ""
                count = 0
                for data in form.cleaned_data['vehicle_fields']:
                    if data != "address" and data != "date" and data !="system":
                        if count == 0 : #placa
                            str_placa = unicode(vehicle.__dict__[data]).encode("UTF-8")
                        elif count == 1: # tipo
                            str_tipo = unicode(vehicle.__dict__[data]).encode("UTF-8")
                        elif count == 2: # cor
                            str_cor = unicode(vehicle.__dict__[data]).encode("UTF-8")
                        elif count == 3: # ano
                            str_ano = unicode(vehicle.__dict__[data]).encode("UTF-8")
                        elif count == 4: # modelo
                            str_modelo = unicode(vehicle.__dict__[data]).encode("UTF-8")
                        elif count == 5: # marca
                            str_marca = unicode(vehicle.__dict__[data]).encode("UTF-8")
                        elif count == 6: #chassi
                            str_chassi = unicode(vehicle.__dict__[data]).encode("UTF-8")
                        mount = ""
                        count += 1
                        
                mount2 = ""              
                mount2 += "<info>"
                if request.POST.has_key("title"):
                    title_raw = request.POST["title"]
                    title = translate_table_xstl(title_raw)
                    mount2 += "<title>"+unicode(title).encode("UTF-8","ignore")+"</title>"
                if request.POST.has_key("period_start"):
                    mount2 += "<datestart>"+unicode(request.POST["period_start"]).encode("UTF-8","ignore")+"</datestart>"
                if request.POST.has_key("period_end"):
                    mount2 += "<dateend>"+unicode(request.POST["period_end"]).encode("UTF-8","ignore")+"</dateend>"                    
                mount2 += "<datenow>" + str(datetime.now())[:19] + "</datenow>"
                mount2 += "<licenseplate>" + str_placa + "</licenseplate>"
                mount2 += "<type>" + str_tipo + "</type>"
                mount2 += "<color>" + str_cor + "</color>"  
                mount2 += "<year>" + str_ano + "</year>" 
                mount2 += "<model>" + str_modelo + "</model>" 
                mount2 += "<brand>" + str_marca + "</brand>" 
                mount2 += "<bodyframe>" + str_chassi + "</bodyframe>"
                mount2 += "</info>"
                mount2 += "<head>"          
                
                #field_list = {}
                #customnames = CustomFieldName.objects.select_related(depth=1).filter(Q(system=system)&Q(custom_field__system=system)).distinct()
                '''
                for name in customnames:
                    field_list.setdefault(name.custom_field.id,name.name)
                    
                for j in data_list:
                    if j.type.tag == 'Lat': pass
                    elif j.type.tag == 'Long': pass
                    elif field_list.has_key(j.type.id):
                        key = smart_str(field_list[j.type.id], encoding='utf-8', strings_only=False, errors='strict')
                        val = j.value
                '''
                
                for title_col in title_row:
                    print("HTML :" + unicode(title_col).encode("utf-8"))
                    if title_col == "Placa" or title_col == u"Tipo de veículo" or title_col == "Ano" or title_col == "Cor" or title_col=="Modelo" or title_col == "Fabricante" or title_col == "Chassi" or title_col == "Sistema" : continue
                    title_col2 = translate_table_xstl(title_col)
                    mount2 += "<coltitle>" + unicode(title_col2).encode("utf-8") + "</coltitle>"
                mount2 += "</head>"
                response.write(mount2)
                tdata_dk = tdata_dict.keys()
                tdata_dk.sort()
                for date in tdata_dk:
                    tdata = tdata_dict[date]
                    item = {}
                    output_list = []
                    mount = ""
                    try:
                        addrs1 = [x.value for x in sorted(tdata,key=lambda d: d.type.name) if x.type.type == 'Geocode']
                        #addrs = unicode(addrs[2]).encode("UTF-8")+" - "+unicode(addrs[1]).encode("UTF-8")+", "+unicode(addrs[3]).encode("UTF-8")+" - "+unicode(addrs[0]).encode("UTF-8")
                        tmp1 = unicode(addrs1[2])
                        tmp2 = unicode(addrs1[1])
                        tmp3 = unicode(addrs1[3])
                        tmp4 = unicode(addrs1[0])
                        addrs = ""
                        if tmp1 != u"" and tmp1 != u"Sem Nome":
                            addrs += tmp1
                            if tmp2 != u"" and tmp2 != u"Sem Nome":
                                addrs += " - "
                        addrs += tmp2
                        if tmp1 != u"" and tmp2 != u"":
                            addrs += ", "
                        addrs += tmp3
                        if tmp3 != u"":
                            addrs += " - "
                        addrs += tmp4
                        addrs = unicode(addrs).encode("utf-8")
                        #print("1#" +str(addrs))                                        
                    except:
                        try:
                            addrs = str(addrs[2]+" - "+addrs[1]+", "+addrs[3]+" - "+addrs[0]).encode("UTF-8")
                            #print("2#" +str(addrs))                                        
                        except Exception as err:
                            #print(err.args)
                            addrs = ""
                    for data in form.cleaned_data['vehicle_fields']:
                        if data == "license_plate" or data == "type" or data == "year" or data == "color" or data == "model" or data == "manufacturer" or data == "chassi" or data == "system": continue
                        if data != "address" and data != "date" and data !="system":
                            mount += "<field>" + unicode(vehicle.__dict__[data]).encode("UTF-8") + "</field>"
                        elif data == "date":
                            mount += "<field>" + unicode(date).encode("UTF-8") + "</field>"
                        elif data == "system":
                            mount += "<field>" + unicode(equip_system).encode("UTF-8") + "</field>"
                        elif data == "address":
                            mount += "<field>" + addrs + "</field>"
                    for x in display_fields:
                        topush = "<field>" + "OFF" + "</field>"
                        for y in tdata:
                            if y.type == x:
                                item[x.tag] = y.value
                                #print(unicode(y.type.name) +  " :: " + unicode(y.value))
                                if unicode(y.type.name) == u"Velocidade Tacógrafo" or unicode(y.type.name) == u"Voltagem de Alimentação" or unicode(y.type.name) == u"Odômetro" or unicode(y.type.name) == u"Velocidade GPS" or unicode(y.type.name) == u"RPM":
                                    val_data = 0.00
                                    if unicode(y.value) == u"OFF":
                                        val_data = 0.00
                                    else:
                                        val_data = float(y.value)
                                    topush = "<field>" + "{0:.2f}".format(val_data) + "</field>"
                                else:
                                    if unicode(y.value)==u"0":
                                        topush = "<field>OFF</field>"    
                                    elif unicode(y.value)==u"1":
                                        topush = "<field>ON</field>"    
                                    else:
                                        topush = "<field>" + y.value + "</field>"
                                
                        mount += str(topush)
                    response.write("<row>"+mount+"</row>")
                response.write("</document>")
                return response
            elif request.POST['type'] == 'PDF':
                request.session['download'] = 'done'
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=relatorio.pdf'
                try:
                    doc = canvas.Canvas(response)

                    field_list = {}
                    customnames = CustomFieldName.objects.select_related(depth=1).filter(Q(system=system)&Q(custom_field__system=system)).distinct()
                    tdata_dk = tdata_dict.keys()
                    tdata_dk.sort()

                    
                    page_count = 0
                    str_placa = ""
                    str_tipo = ""
                    str_cor = ""
                    str_ano = ""
                    str_modelo = ""
                    str_marca = ""
                    str_chassi = ""
                    
                    mount = ""
                    lWidth, lHeight = A4
                    doc.setPageSize((lHeight, lWidth))
                    
                    count = 0
                    for data in form.cleaned_data['vehicle_fields']:
                        if data != "address" and data != "date" and data !="system":
                            if count == 0 : #placa
                                str_placa = unicode(vehicle.__dict__[data]).encode("UTF-8")
                            elif count == 1: # tipo
                                str_tipo = unicode(vehicle.__dict__[data]).encode("UTF-8")
                            elif count == 2: # cor
                                str_cor = unicode(vehicle.__dict__[data]).encode("UTF-8")
                            elif count == 3: # ano
                                str_ano = unicode(vehicle.__dict__[data]).encode("UTF-8")
                            elif count == 4: # modelo
                                str_modelo = unicode(vehicle.__dict__[data]).encode("UTF-8")
                            elif count == 5: # marca
                                str_marca = unicode(vehicle.__dict__[data]).encode("UTF-8")
                            elif count == 6: #chassi
                                str_chassi = unicode(vehicle.__dict__[data]).encode("UTF-8")
                            mount = ""
                            count += 1
                    
                    placa_first = True
                    size = 29

                    totalpages = len(tdata_dk)/(size+1)
                    if totalpages == 0 : totalpages = 1
                    else : totalpages += 1
                    #for date, tdata in tdata_dict.items():
                    left = 20
                    logow = 175
                    logoh = 42
                    top = 300
                    geodist_started = False
                    geodist_total = 0
                    geodist_last_lat = 0
                    geodist_last_lon = 0
                    if len(display_fields) >= 18:
                        space_A = 20
                    else:
                        if len(display_fields) <= 0 :
                            space_A = 360
                        else:
                            space_A = 360 / (len(display_fields))
                    try:
                    
                        page = 1
                        start = 0
                        top = 596
                        end = size - 1

                        
                            # y tracking data
                            #cfns1 = CustomFieldName.objects.select_related(depth=1).filter(pk__in=cfns,custom_field=y.type)
                            #print(str(cfns1) + " % " + str(type(cfns1)))
                        
                        while True:
                            if start >= len(tdata_dk) : break
                            if end >= len(tdata_dk) :
                                end = len(tdata_dk)-1
                            if start == end: break
                            
                            doc.drawInlineImage("/root/itrack/static/media/static/img/logo_wbg.png",left,top - logoh - left,logow,logoh)
                            count = 0
                            doc.setFont("Helvetica",14)
                            #dados do veiculos

                            if request.POST.has_key("title"):
                                doc.drawString(left+logow+40,top-30,request.POST["title"])
                            doc.setFont("Helvetica",10)
                            try:
                                if request.POST.has_key("period_start"):
                                    doc.drawString(left+logow+50,top-45,"A partir : " + request.POST["period_start"])
                            except Exception as err:
                                print(err.args)
                            try:
                                if request.POST.has_key("period_end"):
                                    doc.drawString(left+logow+50,top-57,u"Até : " + unicode(request.POST["period_end"]))
                            except Exception as err:
                                print(err.args)
                            doc.drawString(left+logow+50,top-69,"Emitido em : " + str(datetime.now())[:19])
                               
                            #doc.rect(200,770,380,55,fill=0)
                            doc.setFont("Helvetica",11)
                            doc.drawString(logow + 290,top-30 ,"Dados do veículo:")
                            doc.setFont("Helvetica",10)
                            doc.drawString(logow + 295,top-45,"Placa:")
                            doc.drawString(logow + 395,top-45,"Cor:")
                            doc.drawString(logow + 495,top-45,"Ano:")
                            doc.drawString(logow + 295,top-57,"Tipo:")
                            doc.drawString(logow + 365,top-57,"Modelo:")
                            doc.drawString(logow + 515,top-57,"Fabricante:")
                            doc.drawString(logow + 295,top-69,"Chassi:")
                            doc.drawString(logow + 325,top-45,str_placa)
                            doc.drawString(logow + 420,top-45,str_cor)
                            doc.drawString(logow + 520,top-45,str_ano)
                            doc.drawString(logow + 320,top-57,str_tipo)
                            doc.drawString(logow + 403,top-57,str_modelo)
                            doc.drawString(logow + 568,top-57,str_marca)
                            doc.drawString(logow + 333,top-69,str_chassi)

                            
                            '''
                            id = request.GET.get('id', '')
                            try:
                                if id == '':  = Vehicle.objects.get(system = system)
                                else:  = Vehicle.objects.get(pk = int(id))
                            except: pass
                            count = 0;
                            ets = equipments.equipment.type
                            cfs = [x for x in Vehicle.objects.get(pk=int(id)).equipment.type.custom_field.filter(type="Output")]
                            cfns = CustomFieldName.objects.filter(custom_field__in=cfs,system=request.session['system'],custom_field__availablefields__system=request.session['system'])
                            for cfn in cfns:
                                #cfn.pk
                                #cfn.name.encode("UTF-8")
                                pass
                            '''
                                
                            doc.drawString(20,top-50-logoh,"Data")
                            doc.drawString(125,top-50-logoh,"Endereço")
                            tcount = 0
                            '''
                            for title_col in title_row:
                                if title_col!="Placa" and title_col != "Cor" and title_col != "Modelo" and title_col != "Data" and title_col != "Ano" and title_col != "Fabricante" and title_col != "Chassi" and title_col != "Sistema"  and unicode(title_col) != u"Tipo de veículo" and unicode(title_col) != u"Endereço":
                                    doc.drawString(500 +100*tcount,top-50-logoh,title_col)
                                    tcount += 1
                                    if tcount > 4 : break
                            '''        
                            
                            doc.line(0,top-logoh-55,842,top-logoh-55)
                            doc.rect(logow+280,top-75,370,60,fill=0)
                            tcount = 0
                            doc.setFont("Helvetica",8)
                            printed = []
                            scount = 0
                            
                            for title_col in title_row:
                                #print("PDF :" + unicode(title_col).encode("utf-8"))
                                if unicode(title_col) == u"Endereço" or title_col == "Data" or title_col == "Placa" or title_col == u"Tipo de veículo" or title_col == "Ano" or title_col == "Cor" or title_col=="Modelo" or title_col == "Fabricante" or title_col == "Chassi" or title_col == "Sistema" : continue
                                #print("OK@@")
                                K = simpleSplit(unicode(title_col).encode("utf-8"),doc._fontname,doc._fontsize,space_A-5)
                                if len(K) > 1 :
                                    doc.drawString(left+470+space_A*tcount,top-50-logoh,"[" + str(scount+1) + "]")
                                    scount += 1
                                else:
                                    doc.drawString(left+470+space_A*tcount,top-50-logoh,unicode(title_col).encode("utf-8"))
                                    printed.append(unicode(title_col))
                                tcount += 1
                                if tcount > 15 : break
                            str_dfs = ""
                            tcount = 0
                            for title_col in title_row:
                                if unicode(title_col) == u"Endereço" or title_col == "Data" or title_col == "Placa" or title_col == u"Tipo de veículo" or title_col == "Ano" or title_col == "Cor" or title_col=="Modelo" or title_col == "Fabricante" or title_col == "Chassi" or title_col == "Sistema" : continue
                                if unicode(title_col) not in printed:
                                    str_dfs += "[" + str(tcount+1) + "] " + title_col  + " "
                                    tcount += 1
                                    if tcount>15 : break

                            tmp_y = left
                            tmp_x = left
                            str_dfs += " * estimativa"
                            L = simpleSplit(str_dfs,doc._fontname,doc._fontsize,730)
                            if(len(L)>=1):
                                tmp_y += (len(L)-1)*11
                            doc.line(0,tmp_y+10,842,tmp_y+10)
                            for t in L:
                                doc.drawString(tmp_x,tmp_y,t)
                                tmp_y -= doc._leading
                            
                            doc.drawString(760,left,"Pagina " + str(page) + " de " + str(totalpages))
                            page += 1
                            FirstOnPage = True
                            for date in tdata_dk[start:end]:
                            
                                #print("OK")
                                tdata = tdata_dict[date]
                                geodist_state = 0
                                geodist_cur_lat = 0
                                geodist_cur_lon = 0
                                for y in tdata:
                                    if y.type.name == "Longitude":
                                        print(unicode(y.type.name) +  " :: " + unicode(y.value))
                                        geodist_cur_lon = y.value
                                        geodist_state += 1
                                    elif y.type.name == "Latitude":
                                        print(unicode(y.type.name) +  " :: " + unicode(y.value))
                                        geodist_cur_lat = y.value
                                        geodist_state += 1000
                                if geodist_started:
                                    print("before:" + str(geodist_total))
                                    if ((geodist_state / 1000) >= 1) and ((geodist_state - math.floor(geodist_state/1000)) >= 1):
                                        try:
                                            geodist_total += geoDistance(float(geodist_last_lat),float(geodist_last_lon),float(geodist_cur_lat),float(geodist_cur_lon))
                                            geodist_last_lat = geodist_cur_lat
                                            geodist_last_lon = geodist_cur_lon
                                        except Exception as err:
                                            raise err
                                    print("after:" + str(geodist_total))
                                else:
                                    if ((geodist_state / 1000) >= 1) and ((geodist_state - math.floor(geodist_state/1000)) >= 1):
                                        geodist_started = True
                                        geodist_last_lat = geodist_cur_lat
                                        geodist_last_lon = geodist_cur_lon

                                if placa_first:
                                    placa_first = False
                                try:
                                    addrs1 = [x.value for x in sorted(tdata,key=lambda d: d.type.name) if x.type.type == 'Geocode']
                                    addrs = ""
                                    
                                    tmp1 = unicode(addrs1[2]).encode("UTF-8")
                                    tmp2 = unicode(addrs1[1]).encode("UTF-8")
                                    tmp3 = unicode(addrs1[3]).encode("UTF-8")
                                    tmp4 = unicode(addrs1[0]).encode("UTF-8")
                                    addrs = ""
                                    if tmp1 != u"" and tmp1 != u"Sem Nome":
                                        addrs += tmp1
                                        if tmp2 != u"" and tmp2 != u"Sem Nome":
                                            addrs += " - "
                                    addrs += tmp2
                                    if tmp1 != u"" and tmp2 != u"":
                                        addrs += ", "
                                    addrs += tmp3
                                    if tmp3 != u"":
                                        addrs += " - "
                                    addrs += tmp4
                                    
                                except:
                                    try:
                                        addrs = str(addrs[2]+" - "+addrs[1]+", "+addrs[3]+" - "+addrs[0]).encode("UTF-8")
                                        #print("2#" +str(addrs))                                        
                                    except Exception as err:
                                        #print(err.args)
                                        addrs = ""
                                str_date = ""
                                for data in form.cleaned_data['vehicle_fields']:
                                    if data == "license_plate" or data == "type" or data == "year" or data == "color" or data == "model" or data == "manufacturer" or data == "chassi" or data == "system": continue
                                    elif data == "date":
                                        str_date = unicode(date).encode("UTF-8")
                                        pass
                                    elif data != "address" and data != "date" and data !="system":
                                        #mount += "<field>" + unicode(vehicle.__dict__[data]).encode("UTF-8") + "</field>"
                                        pass
                                doc.setFont("Helvetica",10)
                                doc.drawString(left+100,top - 70 - logoh -16*count,addrs)
                                doc.drawString(left,top - 70 - logoh -16*count,str_date)
                                #doc.line(21,680-16*count,575,680-16*count)
                                tcount = 0
                                dfcount = 0
                                try:
                                    for x in display_fields:
                                        check = False
                                        try:
                                            for y in tdata_dict[date]:
                                                # y tracking data
                                                # tracking data is instance of custom field
                                                if y.type == x:

                                                    if unicode(y.type.name) == u"Velocidade Tacógrafo" or unicode(y.type.name) == u"Voltagem de Alimentação" or unicode(y.type.name) == u"Odômetro" or unicode(y.type.name) == u"Velocidade GPS" or unicode(y.type.name) == u"RPM":
                                                        val_data = 0.00
                                                        if unicode(y.value) == u"OFF":
                                                            val_data = 0.00
                                                        else:
                                                            val_data = float(y.value)
                                                        doc.drawString(left+470+space_A*dfcount,top - 70 - logoh -16*count,"{0:.2f}".format(val_data))                                                      
                                                    else:
                                                        #print(unicode(y.type.name) +  " :: " + unicode(y.value))
                                                        if unicode(y.value) == u"OFF":
                                                            doc.drawString(left+470+space_A*dfcount,top - 70 - logoh -16*count,"O")
                                                        elif unicode(y.value) == u"ON":
                                                            doc.drawString(left+470+space_A*dfcount,top - 70 - logoh -16*count,"X")
                                                        elif unicode(y.value) == u"1":
                                                            doc.drawString(left+470+space_A*dfcount,top - 70 - logoh -16*count,"X")    
                                                        elif unicode(y.value) == u"0":
                                                            doc.drawString(left+470+space_A*dfcount,top - 70 - logoh -16*count,"O")
                                                        else:
                                                            doc.drawString(left+470+space_A*dfcount,top - 70 - logoh -16*count,unicode(y.value).encode("utf-8"))
                                                    check = True
                                                    break
                                        except Exception as err:
                                            print(err.args)
                                        if not check:
                                            doc.drawString(left+470 + space_A*dfcount,top - 70 - logoh -16*count,"O")    
                                        dfcount += 1
                                        if dfcount>15 : break
                                except Exception as err:
                                    print(err.args)
                                count += 1
                                if count >= size:
                                    break
                            fdist = "%(dist).3f" % {"dist":geodist_total}
                            fdist = fdist.replace(".",",")
                            doc.drawString(left+logow+50,top-81,"Dist. Percorrida*: "+unicode(fdist).encode("utf-8")+" km")
                            
                            doc.showPage()
                            start += size
                            end += size
                    except Exception as err:
                        print(err.args)
                    
                    
                    
                    doc.save()
                except Exception as err:
                    print(err.args)
                return response
            if request.POST['type'] == 'HTML':
                response = HttpResponse(mimetype='text/html')
                writer = UnicodeWriter(response)
                writer.writerow(title_row)
                for line in list_table:
                    writer.writerow(line)
                return response
        else:
            if request.POST['type'] == 'HTML':
                no_information = 1
                message = "Por favor escolha o veiculo cadastrado, um intervalo de datas e os campos que deseja exibir."
                message2 = "Feche esta tela e tente novamente."
                request.session['download'] = 'done'
                return render_to_response("reports/templates/htmlreporterror.html",locals(),context_instance=RequestContext(request),)                    
            else:
                no_information = 2

    request.session['download'] = 'done'
    
    return render_to_response("reports/templates/form.html",locals(),context_instance=RequestContext(request),)
    
def translate_table_xstl(str_data):
    str_out = ""
    table_1 = [  192,  193,  194,  195,  196,  199,  200,  201,   202,  203,  204,  205,  206,  207,  210,  211,  212,  213,  214,  217,  218,  219,  220,  224,  225,  226,  227,  228,  231,  232,  233,  234,  235,  236,  237,  238,  239,  242,  243,  244,  245,  246,  249,  250,  251, 252 ]
    table_2 = [ u"À", u"Á", u"Â", u"Â", u"Ä", u"Ç", u"È", u"É",  u"Ê", u"Ë", u"Ì", u"Í", u"Î", u"Ï", u"Ò", u"Ó", u"Ô", u"Ô", u"Ö", u"Ù", u"Ú", u"Û", u"Ü", u"à", u"á", u"â", u"ã", u"ä", u"ç", u"è", u"é", u"ê", u"ë", u"ì", u"í", u"î", u"ï", u"ò", u"ó", u"ô", u"õ", u"ö", u"ù", u"ú", u"û", u"ü" ]
    table_4 = [  "C",  "C",  "C",  "C",  "C",  "C",  "C",  "C",   "C",  "C",  "C",  "C",  "C",  "D",  "D",  "D",  "D",  "D",  "D",  "D",  "D",  "D",  "E",  "E",  "E",  "E",  "E",  "E",  "E",  "E",  "E",  "E",  "E",  "E",  "E",  "E",  "F",  "F",  "F",  "F",  "F",  "F",  "F",  "F", "F" ]
    table_5 = [  "0",  "1",  "2",  "3",  "4",  "7",  "8",  "9",   "A",  "B",  "C",  "D",  "E",  "F",  "2",  "3",  "4",  "5",  "6",  "9",  "A",  "B",  "C",  "0",  "1",  "2",  "3",  "4",  "7",  "8",  "9",  "A",  "B",  "C",  "D",  "E",  "F",  "2",  "3",  "4",  "5",  "6",  "9",  "A", "B", "C" ]
    str_buf = ""
    for x in range(len(str_data)):
        str_buf += str( ord(str_data[x]) ) + " # "
        check = False
        for y in range(len(table_2)):
            #print(dir(table_2[y]))
            if ord(table_2[y]) == ord(str_data[x]):
                str_out += "&#" + str(table_1[y]) + ";"
                check = True
                break
        if not check:
            if ord(str_data[x]) < 128:
                str_out += str_data[x]
            else:
                print(ord(str_data[x]))
                #print("CHAR OUT OF RANGE [" + str(str_data[x]) + "]:[" + ord(str_data[x]) )
                pass
    print(str_buf)
    return str_out
    
def print_pdfpage(x):
    return False
