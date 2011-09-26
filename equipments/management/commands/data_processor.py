# -*- coding:utf-8 -*-
import sys
import os 
import socket
import select
import json
import Queue
import threading
import curses
import codecs


from datetime import datetime
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from itrack.equipments.models import Equipment, Tracking, TrackingData
from itrack.equipments.models import CustomField,EquipmentType
from itrack.alerts.models import Alert,Popup
from itrack.vehicles.models import Vehicle
from itrack.system.tools import lowestDepth
from itrack.system.models import System

from geocoding import ReverseGeocode
from comparison import AlertSender,AlertComparison, GeofenceComparison

#some globals and constants
#--------------------------
PROCESSOR_PORT = settings.PROCESSOR_PORT
PROCESSOR_IP = settings.PROCESSOR_IP

clientPool = Queue.Queue (0)
equipTypeDict = {}
equipTypeIndex = {}
geoDict = {}
systemField = None
vehicleField = None
stdscr = None
main_stop = False
trackings_received = 0
count = 0

# >> ====================================== +-------------------------------+-\
# >> ====================================== | THREAD TO OUTPUT TO THE SCREEN|  >
# >> ====================================== +-------------------------------+-/



class OutputThread(threading.Thread):
    
    trackings_per_second = 0
    global trackings_received
    global main_stop
    
    def calculate(self):
        self.trackings_per_second = trackings_received
        trackings_received = 0
        t = threading.Timer(1.0,self.calculate) 

    def __init__(self):
        super(OutputThread, self).__init__()
        self._stop = threading.Event()
    
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
        
    def run ( self ):
        stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        t = threading.Timer(1.0,self.calculate)
        main_stop = False
        while True:
            if self.stopped():
                curses.nocbreak()
                stdscr.keypad(0)
                curses.echo()
                curses.endwin()
                break
            stdscr.addstr(0, 0, "Infotrack: Data Processor", 
                                curses.A_REVERSE)
            stdscr.addstr(0,40,str(self.trackings_per_second))
            curr_y = 5
            curr_x = 5
            #stdscr.addstr(1,5, str(threading.enumerate()))
            stdscr.addstr(2,5,'+------------------+---------------------------------------------------------------+',
                    curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(3,5,'| Thread name      | Thread status                                                 |',
                    curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(4,5,'+------------------+---------------------------------------------------------------+',
                    curses.color_pair(1) | curses.A_BOLD)

            for th in threading.enumerate():
                if isinstance(th,ClientThread):
                    stdscr.addstr(curr_y,curr_x,"| ",
                                curses.color_pair(1) | curses.A_BOLD)
                    stdscr.addstr(th.getName().ljust(13,' '),curses.color_pair(0))
                    stdscr.addstr("\t| ", curses.color_pair(1) | curses.A_BOLD)
                    stdscr.addstr(th.getStatus().ljust(55,' '),curses.color_pair(0))
                    stdscr.addstr("\t| ", curses.color_pair(1) | curses.A_BOLD)
                    curr_y+=1
            stdscr.addstr(curr_y,5,'+------------------+---------------------------------------------------------------+',
                    curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(curr_y+1,5, "Messages in the pool: "+
                            str(clientPool.qsize()).rjust(2,' ')+
                            "\t\t\t\t\tNumber of threads: "+
                            str(threading.active_count()-2)+"\t\t", curses.A_BOLD)
            
            for i in range(10):
                stdscr.addstr(curr_y+2+i,5,''.rjust(84,' ')) 
                       
            stdscr.refresh()
            if ([sys.stdin],[],[]) == select.select([sys.stdin],[],[],0):
                stdscr.refresh()
                jnk = sys.stdin.read(1)
                stdscr.addstr(0,0,jnk)
                if jnk=='x':
                    main_stop = True
                    
                    for th in threading.enumerate():
                        
                        if isinstance(th,ClientThread):
                            th.stop()
                            stdscr.clear()
                elif jnk == 'n':
                    ClientThread().start()
                elif jnk == 'k':
                     for th in threading.enumerate():
                        if isinstance(th,ClientThread):
                            th.stop()
                            break
                
            
# >> ====================================== +-------------------------------+-\
# >> ====================================== | THREAD TO PROCESS THE DATA    |  >
# >> ====================================== +-------------------------------+-/

class ClientThread(threading.Thread):
    
    global trackings_received
    #these functions before run() allows the thread to be stopped.
   
    def __init__(self):
        super(ClientThread, self).__init__()
        self._stop = threading.Event()
        self._status = "Waiting to process data."
        self._laststatus = ""
    def stop(self):
        self._stop.set()
        self._status = "Stopping thread."

    def stopped(self):
        return self._stop.isSet()
   
    def getStatus(self):
        return self._status
       
    def setLastPrint(self):
        self._laststatus = self._status
    def needPrint(self):
        return self._laststatus == self._status

    def setStatus(self,st):
        self._status = st
        
    def run(self):
      # Have our thread serve "forever":
      
      #System and Vehicle custom fields

      systemField = CustomField.objects.get(tag="System")
      vehicleField = CustomField.objects.get(tag="Vehicle")
      root_system = System.objects.get(parent=None)
      while True:
         
         if ((self.stopped() and clientPool.qsize() == 0) or
            (self.stopped() and threading.active_count() > 2)):
            self.setStatus("Thread stopped.")
            break
            
         
         # Get a client out of the queue
         try:
            client = clientPool.get(True,1)
         except Queue.Empty:
            client = None
         # Check if we actually have an actual client in the client variable:
         if client != None:

            self.setStatus('Processing data from '+client[1][0])
            inbox =  client[0].recv(8192)
    #            file = codecs.open("./")
            datadict = json.loads(inbox)
            if datadict['Type'] == 'MTC State Tracking':
                serial_data = datadict['serial']
                sendstate_data = datadict['sendstate']
                date_data = datadict['date']
                e = Equipment.objects.get(Q(serial=serial_data))
                searchdate = datetime.strptime( date_data, "%Y-%m-%d %H:%M:%S")
                t = Tracking(equipment=e, eventdate=searchdate,  msgtype="TRACKING")
                t.save()
                TrackingData(tracking=t,type=CustomField.objects.get(id=67), value=sendstate_data).save()
                
            elif datadict['Type'] == 'Tracking':
            # tries to pick the equipment and the date of the tracking table
                try:
                    #first, check if the equipment exists
                    type_id = datadict['Identification']['EquipType']
                    e = Equipment.objects.get(
                        Q(serial=datadict['Identification']['Serial'])
                    )
                    try:
                        #second, if the vehicle exists, for that equipment, 
                        # insert the tracking head on the tracking table
                        vehicle = Vehicle.objects.get(equipment=e)
                        sys = lowestDepth(e.system.all())
                        
                        try:
                            searchdate = datetime.strptime( 
                                datadict['Identification']['Date'],
                                "%Y/%m/%d %H:%M:%S")
                            
                        except ValueError:
                            searchdate = datetime.strptime( 
                                datadict['Identification']['Date'],
                                "%Y-%m-%d %H:%M:%S")
                        
                        self.setStatus('Tracking at: '+str(searchdate)+' from equip: '+ str(e))
                                
                        #create the tracking
                        t = Tracking(
                            equipment=e, 
                            eventdate=searchdate, 
                            msgtype="TRACKING")
                        t.save()
                        
                        # mounting the list of data received
                        io = {}
                        io['Input'] = datadict['Input'].copy()
                        io['LinearInput'] = datadict['LinearInput'].copy()
                        io['Output'] = datadict['Output'].copy()
                        print datadict['Output']
                        io['GPS'] = datadict['GPS'].copy()
                        
                        for x0 in xrange(1,8):
                            ttype = 53 + x0
                            TrackingData(tracking=t,type=CustomField.objects.get(id=ttype), value=io['Output']['Output' + str(x0)]).save()

                        #filtering that list, leaving only the registered
                        #custom fields for the equipment type
                        io_filtered = {}
                        for cf in equipTypeDict[int(type_id)]:
                            for k,v in io.items():
                                if not io_filtered.has_key(k):
                                    #pre-populating to avoid KeyError
                                    #io_filtered[k] = {}
                                    pass
                                if (cf.tag in v.keys() and
                                              cf.type == k):
                                    #mounting the dict, associating the custom
                                    #field with the value in the tracking
                                    io_filtered[cf] = v[cf.tag]                                            
                            
                        #inserting the tracking datas under the tracking head
                        
                        for k_cf,v in io_filtered.items():                                
                            TrackingData(
                                    tracking=t,
                                    type=k_cf,
                                    value=v
                            ).save()

                        
                        cflist = [x[0] for x in io_filtered.items()]
                        
                        for cf in equipTypeDict[int(type_id)]:
                            if cf not in cflist:
                                TrackingData(
                                    tracking=t,
                                    type=cf,
                                    value="OFF"
                                ).save()
                            
                            
                        try:
                            #reverse geocoding in the background
                            geocodeinfo = ReverseGeocode(
                                        float(datadict['GPS']['Lat']),
                                        float(datadict['GPS']['Long'])
                                      )
                            #saving the acquired geocode information
                        
                            TrackingData(   tracking=t, 
                                        type=geoDict['Address'],
                                        value=geocodeinfo[1]
                                    ).save()
                            TrackingData(   tracking=t, 
                                        type=geoDict['City'],
                                        value=geocodeinfo[2]
                                    ).save()
                            TrackingData(   tracking=t, 
                                        type=geoDict['State'],
                                        value=geocodeinfo[3]
                                    ).save()
                            TrackingData(   tracking=t, 
                                        type=geoDict['PostalCode'],
                                        value=geocodeinfo[4]
                                    ).save()
                                    
                            self.setStatus('Reverse geocode finished. ')
                            # and adding extra vehicle and system custom fields
                            TrackingData(   tracking=t,
                                        type=vehicleField,
                                        value=vehicle.id).save()
                                        
                            TrackingData(   tracking=t,
                                        type=systemField,value=sys.id).save()
                                                                                     
                        
                            #queries the vehicle in the database
                        
                            #if the last alert sent for the vehicle is not null
                        except:
                            pass
                        if vehicle.last_alert_date is not None:
                          total_seconds = (
                                (searchdate - vehicle.last_alert_date).days *
                                24 * 60 * 60 + 
                                (searchdate - vehicle.last_alert_date).seconds
                                )
                                
                          # check if there's enough time between the last alert 
                          # sent and a possibly new one
                          if total_seconds > vehicle.threshold_time*60:
                            vehicle.last_alert_date = searchdate
                            vehicle.save()
                            #pick the alert records to check                                  
                            alerts = Alert.objects.filter(
                                Q(vehicle=vehicle) & 
                                Q(time_end__gte=searchdate) & 
                                Q(time_start__lte=searchdate) & 
                                Q(active=True)
                                )                              
                            geoalerts = alerts.filter(
                                trigger__custom_field__tag='GeoFence'
                            )
                            # iterates over the inputs and checks if it 
                            # is needed to send the alert
                            for k,v in io_filtered.items():
                                if k.type in ['Input','LinearInput']:
                                    for alert in alerts:
                                        if AlertComparison(self,alert,k,v):
                                            self.setStatus('Found alert to send.')
                                            AlertSender(self,alert,vehicle,
                                                        searchdate,geocodeinfo)
                            
                            #checking the geofence alerts
                            for alert in geoalerts:
                                if GeofenceComparison( self,alert,
                                            io["GPS"]["Lat"], 
                                            io["GPS"]["Long"]
                                            ):
                                    self.setStatus('Found geofence alert to send.')
                                    AlertSender(self,alert,vehicle,searchdate)
                            
                            trackings_received += 1
                          else: 
                              # if the vehicle never had thrown alerts, 
                              # give him a last alert date
                              vehicle.last_alert_date = searchdate
                              vehicle.save()
                              
                        self.setStatus("Waiting to process data.")
                                    
                    except ObjectDoesNotExist:
                        self.setStatus("Equipment without vehicle. Dropping received data.")
                        pass
                except ObjectDoesNotExist:
                    self.setStatus('Equipment not found on the database.'+
                        'Creating and inserting under the root system')
                    
                    try:
                        eq = Equipment(
                            name = datadict['Identification']['Serial'],
                            serial = datadict['Identification']['Serial'],
                            type = equipTypeIndex[type_id],
                            available = True
                        )
                    
                        eq.save()
                        eq.system.add(root_system)
                    except IntegrityError:
                        pass

                except KeyError:
                    self.setStatus('Equip Type "'+str(type_id) + '" not '+
                    'recognized. Dropping recived data.')
                          
            elif datadict['Type'] == 'Command':
                pass
            
            client[0].close()
            
         else:
            self.setStatus("Waiting to process data.")
            
            

# >> ====================================== +-------------------------------+-\
# >> ====================================== | MAIN COMMAND PROCEDURE        |  >
# >> ====================================== +-------------------------------+-/

class Command(BaseCommand):
        
    def handle(self, *args, **options):
        global main_stop
        # Custom fields per equip type dict
        cfs = CustomField.objects.select_related(depth=2).all()
        for cf in cfs:
            for etype in cf.equipmenttype_set.all():
                equipTypeDict.setdefault(int(etype.product_id), []).append(cf)
        
        # Geocoding custom fields   
        geocodefields = CustomField.objects.filter(type='Geocode')
        
        for field in geocodefields:
            geoDict[field.tag] = field
        
        
        # Index for the equipments
        etypes = EquipmentType.objects.all()
        for equiptype in etypes:
            equipTypeIndex[str(equiptype.product_id)] = equiptype
        
        # Start ten threads:
        for x in xrange(10):
            ClientThread().start()
        
        
        # Set up the server:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', PROCESSOR_PORT))
        server.listen(5)
        print "Server listening. The recognized equipment types are:"
        print equipTypeDict
        print main_stop
        OutputThread().start()
        # Have the server serve "forever":
        while True:
            try:    
                clientPool.put(server.accept(),False)
            except KeyboardInterrupt:
                if threading.active_count() <= 2:
                    for th in threading.enumerate():
                        if isinstance(th,OutputThread) or isinstance(th,ClientThread):
                            th.stop()
                    time.sleep(1)
                    exit(0)
