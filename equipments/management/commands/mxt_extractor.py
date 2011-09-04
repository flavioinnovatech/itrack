import os
import json
import Queue
import threading
from xml.etree import cElementTree as ElementTree
import time
import socket

# globals and constants
clientPool = Queue.Queue (0)
PROCESSOR_IP = "192.168.1.197"
PROCESSOR_PORT = 9000

#thread class to process each .xml found
class ClientThread(threading.Thread):
   def run ( self ):
      # Have our thread serve "forever":
      while True:

         # Get a client out of the queue
         client = clientPool.get()

         # Check if we actually have an actual client in the client variable:
         if client != None:
            positions = ElementTree.parse(client).findall('POSITION')
            for position in positions:

                formatted_output = {}

                #identification
                formatted_output['Type'] = 'Tracking'
                formatted_output['Identification'] = {}
                formatted_output['Identification']['EquipType'] = (
                            productName(position.find('FIRMWARE/PROTOCOL')).text
                            )
                formatted_output['Identification']['Serial'] = (
                            position.find('FIRMWARE/SERIAL').text)
                formatted_output['Identification']['Date'] = (
                            position.find('GPS/DATE').text)

                #helper elements
                hardware_state = position.find('HARDWARE_MONITOR')
                gps = position.find('GPS')
                
                #GPS
                formatted_output['GPS'] = {}
                formatted_output['GPS']['Lat'] = gps.find('LATITUDE').text
                formatted_output['GPS']['Long'] = gps.find('LONGITUDE').text
                formatted_output['GPS']['Speed'] = gps.find('SPEED').text
                
                #Linear Inputs            
                formatted_output['LinearInput'] = {}
                formatted_output['LinearInput']['Hodometer'] = (
                            gps.find('HODOMETER').text )
                formatted_output['LinearInput']['Temp1'] = (
                            hardware_state.find('TEMPERATURE').text)
                formatted_output['LinearInput']['RPM'] = (
                            hardware_state.find('RPM').text)
                formatted_output['LinearInput']['PowerSupply'] = (
                            hardware_state.find('POWER_SUPPLY').text)
                formatted_output['LinearInput']['Hourmeter'] = (
                            hardware_state.find('HOURMETER').text)
                #MEGA HACK: the maxtrack trackers dont have any velocimeter ind-
                #           icator, then we are going to cheat by duplicating 
                #           the info from the GPS speed.
                formatted_output['LinearInput']['Speed'] = (
                            formatted_output['GPS']['Speed'])
                
                #inputs
                inputs = hardware_state.find('INPUTS')
                formatted_output['Input'] = {}
                formatted_output['Input']['Ignition'] = (
                                inputs.find('IGNITION').text)
                formatted_output['Input']['Panic'] = inputs.find('PANIC').text
                for i in xrange(1,9):
                    formatted_output['Input']['Input'+str(i)]= (
                                    inputs.find('INPUT'+str(i))).text
                
                #outputs
                outputs = hardware_state.find('OUTPUTS')
                formatted_output['Output'] = {}
                for i in xrange(1,9):
                    formatted_output['Output']['Output'+str(i)]= (
                                    outputs.find('OUTPUT'+str(i))).text

                print "Sending one MXT tracking table to the data processor on",
                print str(PROCESSOR_IP)+":"+str(PROCESSOR_PORT)
                
                processor_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                processor_client.connect((PROCESSOR_IP, PROCESSOR_PORT))
                processor_client.send(json.dumps(formatted_output))
            os.remove(client)

#
#
#
#processor_client.close()


# Product name conversion function: returns one internal identification, 
# shared with the other brand trackers, based on the TCA id
# Here's the table of conversion:

#   Product name                Product Brand ID    Internal ID
#   --------------------------  ----------------    -----------
#   TCA / TETROS BABY V1.0          50                  0
#   TCA Light V2 com PIC - GSM      54                  1
#   TCA Light V1 com PIC - GSM      55                  2
#   TCA Master V1 com PIC - GSM     56                  3
#   TCA Baby V1 com PIC - CDMA      60                  4
#   TETROS BABY V2.0                40                  5
#   TETROS MIDI                     41                  6
#   TETROS MAXI                     42                  7
#   TETROS MINI                     43                  8
#   TETROS PLUS                     22                  9

def productName(identification):
    if identification == "50":
        return "0"
    elif identification == "54":
        return "1"
    elif identification == "55":
        return "2"
    elif identification == "56":
        return "3"
    elif identification == "60":
        return "4"
    elif identification == "40":
        return "5"
    elif identification == "41":
        return "6"
    elif identification == "42":
        return "7"
    elif identification == "43":
        return "8"
    elif identification == "22":
        return "9"

    return identification

# =======> +----------------+
# =======> | MAIN PROCEDURE |
# =======> +----------------+
for x in xrange(5):
    ClientThread().start()

while True:
    for dirname, dirnames, filenames in os.walk('/Maxtrack_Gateway/xml_data'):
        for filename in filenames[0:5]:
            xmlfile = os.path.join(dirname, filename)
            clientPool.put(xmlfile)
    time.sleep(5)

