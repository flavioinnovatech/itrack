#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys 
import socket
import os
import sys 
import select 
import string
from urllib import urlencode
import urllib
import time
from datetime import datetime
from xml.etree import cElementTree as ElementTree
#from xml.etree.ElementTree import ParseError

from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import lower,title
from django.contrib.gis.geos import Point
from django.conf import settings

from itrack.equipments.models import Equipment, Tracking, TrackingData,CustomField
from itrack.alerts.models import Alert,Popup
from itrack.vehicles.models import Vehicle
from itrack.accounts.models import UserProfile
from itrack.command.models import CPRSession
from itrack.command.models import Command as ItrackCommand
from itrack.system.tools import lowestDepth

from comparison import AlertComparison,GeofenceComparison, AlertSender
from geocoding import ReverseGeocode
from xmldictconfig import XmlDictConfig


#TCP_IP = '192.168.1.119'
TCP_IP = settings.EXTRACTOR_IP   # the server IP address
TCP_PORT = 5000			# the server port
BUFFER_SIZE = 20000		# the maximum buffer size (in chars) for a TCP packet
USERNAME = "extractor"		# the user that will log on CPR
PASSWORD = "extractor"		# the password for this user 

# >> ==================================================== +---------------------------+-\
# >> ==================================================== | SOME FUNCTION DEFINITIONS |  >
# >> ==================================================== +---------------------------+-/

# Messages that will be sent to CPR: the ACK and the first auth message
authentication_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"1\" /><Data User=\""+USERNAME+"\" Password=\""+PASSWORD+"\" /></Package>"

ack_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"98\" Reason=\"0\" Save=\"FALSE\"/><Data /></Package>"

#Checks if the packet sent was successful. If not,print on screen the meaning of the reason specified.
def reasonMsg(msg):
    if msg == "0":
        return 1
    
    elif msg == "1":
        print "Error: Invalid username or password."
    elif msg == "2":
        print "Error: Session already open."
    elif msg == "3":
        print "Error: Invalid session code."
    elif msg == "4":
        print "Error: Invalid parameters."
    elif msg == "5":
        print "Error: Temporary registry created on memory."
    elif msg == "6":
        print "Error: Invalid datagram received."
    elif msg == "98":
        print "Error: User does not have permission to execute this action."
    elif msg == "99":
        print "Error: General failure. Could not execute the action"
    
    return 0

#Authentication function. Receives the connected TCP socket and starts the communication with the server
#   parameters:   s : the connected socket
#   return: the security key for the started session
def authentication(s):
    
    s.send(authentication_msg)
    try:
        data = s.recv(BUFFER_SIZE)
        
        xml = ElementTree.fromstring(data[:len(data)-1])
        msg_reason = xml.find("Header").get("Reason")
        
        if reasonMsg(msg_reason):
            sec_key = xml.find("Data").get("SecurityKey")
        else:
            exit(int(msg_reason))
        return sec_key
    except:
        exit(1)

# >> ==================================================== +-------------------------------+-\
# >> ==================================================== | MAIN COMMAND PROCEDURE        |  >
# >> ==================================================== +-------------------------------+-/

class Command(BaseCommand):
    args = 'no args'
    help = 'Extract info from CPR'

# >> ==================================================== +-------------------------------+-\
# >> ==================================================== | CONNECTION AND AUTHENTICATION |  >
# >> ==================================================== +-------------------------------+-/

    
    def handle(self, *args, **options):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))

        #s.connect((TCP_IP, TCP_PORT))
        #sending the auth message, receiving the response and sending an ack message
        key = authentication(s)
        CPRSession.objects.all().delete()
        cprkey = CPRSession(key=key,time=datetime.now())
        cprkey.save()
        #mounting the XML response to server
        seckey_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"2\" /><Data SessionId=\""+key+"\" /></Package>"
        close_msg =  "<?xml version=\"1.0\" encoding=\"ASCII\"?>\n<Package>\n  <Header Version=\"1.0\" Id=\"99\" />\n  <Data SessionId=\""+key+"\" />\n</Package>"

        #sending the response to the server, and awaiting the outbox message
        s.send(ack_msg)
        s.send(seckey_msg)
        data = s.recv(BUFFER_SIZE)
        s.send(ack_msg)

        #listening all information given by CPR.

# >> ==================================================== +-------------------------------+-\
# >> ==================================================== | MAIN EXTRACTOR LOOP           |  >
# >> ==================================================== +-------------------------------+-/

        
        while 1:
        
            # if there is messages to read in the socket
            if ([s],[],[]) == select.select([s],[],[],0):
            
                # reads and inform the acknowledgement of the message
                inbox = s.recv(BUFFER_SIZE)
                s.send(ack_msg)
                try:

# >> ==================================================== +-------------------------------+-\
# >> ==================================================== | PARSING XML                   |  >
# >> ==================================================== +-------------------------------+-/
                
                  # parse the received xml and turns it into a dict
                  self.stdout.write("================================\n"+inbox+"\n================================\n")
                  xml =  ElementTree.fromstring(inbox.strip(""))
                  xmldict = XmlDictConfig(xml)
                  # checks if it's a tracking table
                  if xmldict['Header']['Id'] == '198':
                      try:
# >> ==================================================== +-------------------------------+-\
# >> ==================================================== | DATABASE LOOKUP               |  >
# >> ==================================================== +-------------------------------+-/
                          
                          # tries to pick the equipment and the date of the tracking table
                          e = Equipment.objects.get(serial=xmldict['TCA']['SerialNumber'])
                          v = Vehicle.objects.get(equipment=e)
                          sys = lowestDepth(e.system.all())
                          searchdate = datetime.strptime(xmldict['Event']['EventDateTime'], "%Y/%m/%d %H:%M:%S")
                          try:
                              # tries to pick the tracking table with the same equipment and eventdate
                              t = Tracking.objects.get(Q(equipment=e) & Q(eventdate=searchdate))
                    
                          except ObjectDoesNotExist:
                              # probably the try statement above will raise this exception, so the script shall create the tracking
                              t = Tracking(equipment=e, eventdate=searchdate, msgtype=xmldict['Datagram']['MsgType'])
                              t.save()
                              
# >> ==================================================== +-------------------------------+-\
# >> ==================================================== | CUSTOMFIELD AND DATA MERGING  |  >
# >> ==================================================== +-------------------------------+-/                              

                              #iterates over the input dicts and saves the information for each matching custom field in the database table
                              for k_type,d_type in xmldict.items():
                                  if type(d_type).__name__ == 'dict':
                                      for k_tag,d_tag in d_type.items():
                                          try:
                                              #find the customfield to put the tracking data under, then create and save it
                                              # TODO: if needed, optimize this database lookup doing one big search out of the for statement
                                              # TODO: and iterate over the list
                                              c = CustomField.objects.get(Q(type=k_type)&Q(tag=k_tag))
                                              tdata = TrackingData(tracking=t,type=c,value=d_tag)
                                              tdata.save()
                                          except ObjectDoesNotExist:
                                              pass
                                              
# >> ================================================= +----------------------------------+-\
# >> ================================================= | GEOCODING AND MORE DATA ADDITION |  >
# >> ================================================= +----------------------------------+-/

                              #reverse geocoding in the background
                              geocodeinfo = ReverseGeocode(str(xmldict['GPS']['Lat']),str(xmldict['GPS']['Long']))
                              
                              #get the custom fields for the right things
                              geocodefields = CustomField.objects.filter(type='Geocode')
                              geodict = {}
                              for field in geocodefields:
                                geodict[field.tag] = field
                              
                              #saving the tracking datas to the tracking
                              TrackingData(tracking=t, type=geodict['Address'],value=geocodeinfo[1]).save()
                              TrackingData(tracking=t, type=geodict['City'],value=geocodeinfo[2]).save()
                              TrackingData(tracking=t, type=geodict['State'],value=geocodeinfo[3]).save()
                              TrackingData(tracking=t, type=geodict['PostalCode'],value=geocodeinfo[4]).save()
                              
                              #saving the vehicle tracking data
                              field = CustomField.objects.get(tag="Vehicle")
                              TrackingData(tracking=t,type=field,value=v.id).save()
                              
                              #saving the system tracking data
                              field = CustomField.objects.get(tag="System")
                              TrackingData(tracking=t,type=field,value=sys.id).save()
                              
                              # print the success message            
                              self.stdout.write('>> The tracking table sent on '+str(searchdate)+' for the equipment '+ xmldict['TCA']['SerialNumber'] +' has been saved successfully.\n')

# >> ==================================================== +-------------------------------+-\
# >> ==================================================== | ALERTS AND DATA COMPARISON    |  >
# >> ==================================================== +-------------------------------+-/
                        
      # Here is the main alert handler. First, queries the database looking if there's some alert that matches the 
      # received tracking. After that, for each alert in the result of the query, alert in each way available.
                        
                          #queries the vehicle in the database
                          vehicle = v #(has been done before)
                              
                          #if the last alert sent for the vehicle is not null
                          if vehicle.last_alert_date is not None:
                              #calculate the difference between the last alert and a possibly new one                        
                              total_seconds = (searchdate - vehicle.last_alert_date).days * 24 * 60 * 60 + (searchdate - vehicle.last_alert_date).seconds
                            
                              #check if there's enough time between the last alert sent and a possibly new one
                              if total_seconds > vehicle.threshold_time*60:
                                  self.stdout.write('>> Alert threshold reached.\n')
                                  vehicle.last_alert_date = searchdate
                                  vehicle.save()
                                  
                                  #pick the alert records to check                                  
                                  alerts = Alert.objects.filter(Q(vehicle=vehicle) & Q(time_end__gte=searchdate) & Q(time_start__lte=searchdate) & Q(active=True))                              
                                  
                                  #iterates over the inputs and checks if it is needed to send the alert
                                  for k_type,d_type in dict(xmldict['Input'].items() + xmldict['LinearInput'].items()).items():
                                      
                                      try:
                                          
                                          #dont look for GPS information now (will be done for the geofences)
                                          c = CustomField.objects.get(Q(tag=k_type)& ~Q(type='GPS'))
                                          
                                          #function that returns true if the alert shall be sent, and false if not.
                                          for alert in alerts:
                                              
                                              if AlertComparison(self,alert,c,d_type):         
                                                  #function that sends in the proper ways the alerts
                                                  AlertSender(self,alert,vehicle,searchdate)
                                              else:
                                                  pass
                                                  # self.stdout.write('>> Nao entrou no Alert Comparison.\n')
                                                                     
                                      except ObjectDoesNotExist:
                                          # self.stdout.write('>> Entrou no except "objectdoesnotexist".\n')
                                          #exception thrown for the inputs and linear inputs that didn't match
                                          #any field in the database
                                          pass
                                          
# >> ==================================================== +-------------------------------+-\
# >> ==================================================== | GEOFENCE COMPARISONS          |  >
# >> ==================================================== +-------------------------------+-/

                                  #check if the position is inside (or outside) some geofence alert
                                  geoalerts = alerts.filter(trigger__custom_field__tag='GeoFence')

                                  for alert in geoalerts:
                                    if GeofenceComparison(self,alert,xmldict["GPS"]["Lat"], xmldict["GPS"]["Long"]):
                                        AlertSender(self,alert,vehicle,searchdate)
                          else: #if the vehicle never had thrown alerts, give him a last alert date
                              vehicle.last_alert_date = searchdate
                              vehicle.save()
                
                      #exceptions thrown if the equipment does not exist.
                      # TODO: create the equipments that isn't in the equipments database table
                      except ObjectDoesNotExist:
                          pass
                      except KeyError:
                          pass
                          
                  #if the message is a command status message
                  elif xmldict['Header']['Id'] == '106':
                  # TODO: update the status for the given command
                    print xmldict
                    e = Vehicle.objects.get(equipment__serial=xmldict['Data']['Serial'])
                    c = ItrackCommand.objects.filter(equipment=e)
                    c = c.get(state=u'0')
                    self.stdout.write(str(c)+","+xmldict['Data']['Status']+ "\n")
                    if xmldict['Data']['Status'] == '3': #message was sent to the GPRS network
                        #as we only have one command per time in the command table, change the command status
                        self.stdout.write('here!\n')
                        c.state = u"1"
                        c.time_received = datetime.strptime(xmldict['Header']['TimeStamp'], "%Y/%m/%d %H:%M:%S")                        
                        c.save()
                                    
                                     
                #except ParseError:       
                #TODO : parse the things when two tracking tables comes to the inbox - this case is kind of rare,
                #TODO : but makes the extractor crash when the 'except ParseError' is turned on.
                except:
                  pass
