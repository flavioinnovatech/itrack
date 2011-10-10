# -*- coding: utf-8 -*-
# Create your views here.
import csv,codecs, StringIO
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter, A4

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
            datas = TrackingData.objects.select_related('tracking').filter(Q(tracking__in=trackings)&Q(type__type='Geocode')).order_by('tracking__eventdate')

            #print("# TESTE 020 ")
            tdata_dict = {}
            for tdata in datas:
                tdata_dict.setdefault(tdata.tracking.eventdate, []).append(tdata)
            
            d2 = datetime.now()
            #print tdata_dict
            
            #initializing the resources that are going to be used to mount the table
            table_content = []
            list_table = []
            #print("# TESTE 021 ")

            
            try:
                #print(form.cleaned_data["vehicle_fields"])
                #print(request.POST.getlist("vehicle_fields"))
                
                #print(form.cleaned_data["fields"])
                #print(request.POST.getlist("fields"))

                display_fields = map(lambda x: x.custom_field,form.cleaned_data["fields"])
            except Exception as err:
                #print(err.args)
                pass

            try:
                title_row = map(lambda x: firstRowTitles(str(x)), form.cleaned_data['vehicle_fields']) + map(lambda x: unicode(x),display_fields)
            except Exception as err:
                #print(err.args)
                pass
                
            if request.POST['type'] == 'CSV':
                #print("# TESTE 022 ")
                #main loop for each tracking found

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
                                item[x.tag] = y.value
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
                
                '''
                for date, tdata in tdata_dict.items():

                    item = {}
                    output_list = []
                    print("# TESTE 023 ")
                    #FUNCTIONAL PROGRAMMING RULEZ THE NATION: mount the list of elements of the address,
                    #sorted by the customfields names, or ["CEP","Cidade","Endereço","Estado"]
                    addrs = [x.value for x in sorted(tdata,key=lambda d: d.type.name) if x.type.type == 'Geocode']
                    print("# TESTE 024 ")
                    try:
                        print(addrs)
                    except Exception as err:
                        print(str(err.message) + ":" + str(err.args))
                    print("# TESTE 025 ")
                    try:
                        addrs = str(addrs[2]) +" - " + str(addrs[1]) + ", " + str(addrs[3]) + " - " + str(addrs[0])
                    except Exception as err:
                        addrs = ""
                        print(str(err.message) + ":" + str(err.args))
                    
                    print("# TESTE 025X ")
                    #data for vehicle fields
                   
                    for data in form.cleaned_data['vehicle_fields']:
                        print("# TESTE 026 ")
                        if data != "address" and data != "date" and data !="system":
                            output_list.append(vehicle.__dict__[data])
                        elif data == "date":
                            output_list.append(str(date))
                        elif data == "system":
                            output_list.append(equip_system)
                        elif data == "address":
                            output_list.append(addrs)

                    #data of the custom fields (inputs and outputs)
                    print("# TESTE 026 ")
                    for x in display_fields:
                        print("# TESTE 027 ")
                        topush = "OFF"
                        for y in tdata:
                            if y.type == x:
                                item[x.tag] = y.value
                                topush = "ON"
                        output_list.append(topush)
                    list_table.append(output_list)
                print("# TESTE 028 ")
                response = HttpResponse(mimetype='text/csv')
                response['Content-Disposition'] = 'attachment; filename=report.csv'
                response.set_cookie("fileDownloadToken", request.POST['token'])    
                count = 0
                for row in list_table:
                    for col in row: 
                        if count > 0:
                            response.write(",")
                        response.write(col)
                        count += 1
                    response.write("\n")
                request.session['download'] = 'done'
                print("# TESTE 026 ")
                return response
                '''
                
            elif request.POST['type'] == 'HTML':
                request.session['download'] = 'done'
                response = HttpResponse(mimetype='text/xml')
                response.write("<?xml version=\"1.0\" encoding=\"utf-8\"?><?xml-stylesheet type=\"text/xsl\" href=\"/media/xslt/report.xsl\"?><document>")
                mount2 = "<head>"                
                for title_col in title_row:
                    mount2 += "<coltitle>" + unicode(title_col).encode("UTF-8") + "</coltitle>"
                mount2 += "</head>"
                response.write(mount2)
                for date, tdata in tdata_dict.items():
                    item = {}
                    output_list = []
                    mount = ""
                    try:
                        addrs = [x.value for x in sorted(tdata,key=lambda d: d.type.name) if x.type.type == 'Geocode']
                        addrs = unicode(addrs[2]+" - "+addrs[1]+", "+addrs[3]+" - "+addrs[0]).encode("UTF-8")
                        #print("1#" +str(addrs))                                        
                    except:
                        try:
                            addrs = str(addrs[2]+" - "+addrs[1]+", "+addrs[3]+" - "+addrs[0]).encode("UTF-8")
                            #print("2#" +str(addrs))                                        
                        except Exception as err:
                            #print(err.args)
                            addrs = ""
                    for data in form.cleaned_data['vehicle_fields']:
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
                                topush = "<field>" + "ON" + "</field>"
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
                    count = 0
                    mount = ""
                    lWidth, lHeight = A4
                    doc.setPageSize((lHeight, lWidth))
                    
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
                    size = 30
                    totalpages = len(tdata_dk)/size
                    if totalpages == 0 : totalpages = 1
                    #for date, tdata in tdata_dict.items():
                    try:

                        print(tdata_dk)
                        page = 1
                        start = 0
                        end = size - 1
                        while True:
                            if start > len(tdata_dk) : break
                            if end > len(tdata_dk) :
                                end = len(tdata_dk)-1
                            count = 0
                            if start == end: break
                            

                            doc.drawInlineImage("/root/itrack/static/media/static/img/logo_wbg.png",20,778,175,42)
                            count = 0
                            doc.setFont("Helvetica",14)
                            #dados do veiculos
                            doc.drawString(300,495,"Relatório de Rastreamento")
                            #doc.rect(200,770,380,55,fill=0)
                            doc.setFont("Helvetica",10)
                            doc.drawString(20,354,"Dados do veículo:")
                            doc.drawString(40,335,"Placa:")
                            doc.drawString(170,335,"Cor:")
                            doc.drawString(320,335,"Ano:")
                            doc.drawString(470,335,"Tipo:")
                            doc.drawString(40,321,"Modelo:")
                            doc.drawString(170,321,"Fabricante:")
                            doc.drawString(320,321,"Chassi:")
                            doc.drawString(79,335,str_placa)
                            doc.drawString(223,335,str_cor)
                            doc.drawString(360,335,str_ano)
                            doc.drawString(500,335,str_tipo)
                            doc.drawString(79,321,str_modelo)
                            doc.drawString(223,321,str_marca)
                            doc.drawString(360,321,str_chassi)
                            doc.drawString(20,302,"Data")
                            doc.drawString(125,302,"Endereço")
                            doc.line(0,70,300,70)
                            doc.line(0,715,300,715)
                            doc.drawString(270,50,"Pagina " + str(page) + " de " + str(totalpages))
                            page += 1
                            
                            for date in tdata_dk[start:end]:
                                tdata = tdata_dict[date]
                                if placa_first:
                                    placa_first = False
                                try:
                                    addrs = [x.value for x in sorted(tdata,key=lambda d: d.type.name) if x.type.type == 'Geocode']
                                    addrs = unicode(addrs[2]+" - "+addrs[1]+", "+addrs[3]+" - "+addrs[0]).encode("UTF-8")
                                    #print("1#" +str(addrs))                                        
                                except:
                                    try:
                                        addrs = str(addrs[2]+" - "+addrs[1]+", "+addrs[3]+" - "+addrs[0]).encode("UTF-8")
                                        #print("2#" +str(addrs))                                        
                                    except Exception as err:
                                        #print(err.args)
                                        addrs = ""
                                #doc.drawStrig(50,700-16*count,addrs)
                                #doc.setFillColorRGB(0, 0, 0)
                                #doc.setStrokeColorRGB(0,0,0)
                                str_date = ""
                                for data in form.cleaned_data['vehicle_fields']:
                                    if data == "date":
                                        str_date = unicode(date).encode("UTF-8")
                                doc.setFont("Helvetica",10)
                                doc.drawString(125,684-16*count,addrs)
                                doc.drawString(20,684-16*count,str_date)
                                #doc.line(21,680-16*count,575,680-16*count)
                                print(str(date) + " @@ " + str(tdata))
                                count += 1
                                if count > size:
                                    break
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
def print_pdfpage(x):
    return False
