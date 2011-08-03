# -*- coding: utf-8 -*-
# Create your views here.
import csv,codecs, StringIO
from datetime import datetime

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.core.exceptions import ObjectDoesNotExist

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
    
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

API_KEY = 'ABQIAAAAOV9qRRxejMi2WeW2TanAKhTefegWErZP_EhBh-or-xYREOhaRBSYXJPqI_-2MwMOsGwqcYel72Q_Qw'

VEHICLE_CHOICES = (("license_plate","Placa"),("date",u"Data"),("type",u"Tipo de veículo"),("address",u"Endereço"),("system",u"Sistema"),("color",u"Cor"),("year",u"Ano"),("model",u"Modelo"),("manufacturer",u"Fabricante"),("chassi",u"Chassi"))

def firstRowTitles(item):
    pos = [x[0] for x in VEHICLE_CHOICES].index(item)
    return VEHICLE_CHOICES[pos][1]

def report(request,offset):
    
    no_information = 0
    
    if request.method != 'POST':
        form = ReportForm(int(offset))
    else:

        try:
            if request.POST.has_key("vehicle_other"):
                v = Vehicle.objects.get(license_plate=request.POST["vehicle"])
                request.POST["vehicle"] = str(v.id)
        except ObjectDoesNotExist:
            pass        
        form = ReportForm(int(offset),request.POST)    
        
        if form.is_valid():
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
                vehicle = Vehicle.objects.get(pk=form.cleaned_data["vehicle"])
            except:
                no_information = 1
                return render_to_response("reports/templates/form.html",locals(),context_instance=RequestContext(request),)
            if s.parent == None:
                equip_system = s.name
                trackings = Tracking.objects.filter(
                    Q(eventdate__gte=form.cleaned_data['period_start'])  
                    &Q(eventdate__lte=form.cleaned_data['period_end'])
                    &(
                        Q(trackingdata__type__type = 'Vehicle')
                        &Q(trackingdata__value = vehicle.id)
                    )
                )
            else:
                equip_system = lowestDepth(vehicle.equipment.system.all()).name
                print vehicle.id
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
                no_information = 1
                return render_to_response("reports/templates/form.html",locals(),context_instance=RequestContext(request),)
            
            datas = TrackingData.objects.select_related('tracking').filter(Q(tracking__in=trackings)&Q(type__type='Geocode'))

            tdata_dict = {}
            for tdata in datas:
                tdata_dict.setdefault(tdata.tracking.eventdate, []).append(tdata)
            
            d2 = datetime.now()
            #print tdata_dict
            
            #initializing the resources that are going to be used to mount the table
            table_content = []
            list_table = []
            
            display_fields = map(lambda x: x.custom_field,form.cleaned_data["fields"])

            title_row = map(lambda x: firstRowTitles(str(x)), form.cleaned_data['vehicle_fields']) + map(lambda x: unicode(x),display_fields)
            
            
            
            #main loop for each tracking found
            for date, tdata in tdata_dict.items():
                item = {}
                output_list = []
                
                #FUNCTIONAL PROGRAMMING RULEZ THE NATION: mount the list of elements of the address,
                #sorted by the customfields names, or ["CEP","Cidade","Endereço","Estado"]
                addrs = [x.value for x in sorted(tdata,key=lambda d: d.type.name) if x.type.type == 'Geocode']
                addrs = str(addrs[2]+" - "+addrs[1]+", "+addrs[3]+" - "+addrs[0])
                
                #data for vehicle fields
               
                for data in form.cleaned_data['vehicle_fields']:
                    if data != "address" and data != "date" and data !="system":
                        output_list.append(vehicle.__dict__[data])
                    elif data == "date":
                        output_list.append(str(date))
                    elif data == "system":
                        output_list.append(equip_system)
                    elif data == "address":
                        output_list.append(addrs)

                #data of the custom fields (inputs and outputs)
                       
                for x in display_fields:
                    topush = "OFF"
                    for y in tdata:
                        if y.type == x:
                            item[x.tag] = y.value
                            topush = "ON"
                    output_list.append(topush)

                list_table.append(output_list)

            
            
            if request.POST['type'] == 'CSV':
                response = HttpResponse(mimetype='text/csv')
                response['Content-Disposition'] = 'attachment; filename=report.csv'
                
                writer = UnicodeWriter(response)
                writer.writerow(title_row)
                for line in list_table:
                    writer.writerow(line)
                response.set_cookie("fileDownloadToken", request.POST['token'])    
                return response
    return render_to_response("reports/templates/form.html",locals(),context_instance=RequestContext(request),)
