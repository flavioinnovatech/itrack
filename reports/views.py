# -*- coding: utf-8 -*-
# Create your views here.
import csv,codecs, cStringIO

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.http import HttpResponse
from django.utils.encoding import smart_str

from itrack.reports.forms import ReportForm
from itrack.equipments.models import CustomFieldName, Tracking, TrackingData
from itrack.system.models import System
from itrack.vehicles.models import Vehicle
from itrack.system.tools import lowestDepth
from itrack.pygeocoder import Geocoder


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
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
    
    if request.method != 'POST':
        form = ReportForm(int(offset))
    else:
        form = ReportForm(int(offset),request.POST)
        
        if form.is_valid():
            trackings = Tracking.objects.filter(Q(eventdate__gte=form.cleaned_data['period_start']) & Q(eventdate__lte=form.cleaned_data['period_end']))
            
            #initializing the resources that are going to be used to mount the table
            table_content = []
            list_table = []
            vehicle = Vehicle.objects.get(license_plate=form.cleaned_data["vehicle"])
            display_fields = map(lambda x: x.custom_field,form.cleaned_data["fields"])

            title_row = map(lambda x: firstRowTitles(str(x)), form.cleaned_data['vehicle_fields']) + map(lambda x: unicode(x),display_fields)

            #main loop for each tracking found
            for tracking in trackings:
                item = {}
                output_list = []
                tdata = TrackingData.objects.filter(tracking=tracking)
                
                #data for vehicle fields
                for data in form.cleaned_data['vehicle_fields']:
                    if data != "address" and data != "date" and data !="system":
                        item[data] = vehicle.__dict__[data]
                        output_list.append(vehicle.__dict__[data])
                    elif data == "date":
                        item["date"] = str(tracking.eventdate)
                        output_list.append(str(tracking.eventdate))
                    elif data == "system":
                        item["system"] = lowestDepth(vehicle.equipment.system.all()).name
                        output_list.append(lowestDepth(vehicle.equipment.system.all()).name)
                    elif data == "address":
                        lat = ''
                        lng = ''
                        for j in tdata:

                            #getting the lat and long 
                            if j.type.tag == 'Lat':
                                lat = float(j.value)
                                #output_list.append(j.value)
                            elif j.type.tag == 'Long':
                               lng = float(j.value)
                                #output_list.append(j.value)
                        
                        #if there's a lattitude and longitude to process    
                        if not lat == '' and not lng == '':
                            
                            result = Geocoder.reverse_geocode(lat,lng)
                            addr = unicode(result[0])
                        else:
                            addr = u'Não disponível'
                        
                        item['address'] = addr
                        output_list.append(addr)
                
                #data of the custom fields (inputs and outputs)        
                for x in display_fields:
                    item[x.tag] = "OFF"
                    topush = "OFF"
                    for y in tdata:
                        if y.type == x:
                            item[x.tag] = y.value
                            topush = "ON"
                    output_list.append(topush)

                list_table.append(output_list)
                table_content.append(item)
            
            if request.POST['type'] == 'CSV':
                response = HttpResponse(mimetype='text/csv')
                response['Content-Disposition'] = 'attachment; filename=report.csv'
                writer = UnicodeWriter(response)
                writer.writerow(title_row)
                print "aqui!"
                for line in list_table:
                    writer.writerow(line)
                    
                return response
    return render_to_response("reports/templates/form.html",locals(),context_instance=RequestContext(request),)
