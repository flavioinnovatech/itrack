import sys 
import socket
import select
import json
import os



from datetime import datetime
from xmldictconfig import XmlDictConfig
from xml.etree import cElementTree as ElementTree

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from itrack.command.models import CPRSession

import threading

import time as mTimer

# >> ==================================================== +---------------------------+-\
# >> ==================================================== | SOME FUNCTION DEFINITIONS |  >
# >> ==================================================== +---------------------------+-/


# Constants
TCP_IP = settings.EXTRACTOR_IP          # the server IP address
TCP_PORT = 5000			                # the server port
PROCESSOR_IP = settings.PROCESSOR_IP
PROCESSOR_PORT = settings.PROCESSOR_PORT

BUFFER_SIZE = 20000		# the maximum buffer size (in chars) for a TCP packet
USERNAME = "extractor"		# the user that will log on CPR
PASSWORD = "extractor"		# the password for this user 

# Messages that will be sent to CPR: the ACK and the first auth message
authentication_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"1\" /><Data User=\""+USERNAME+"\" Password=\""+PASSWORD+"\" /></Package>"

ack_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"98\" Reason=\"0\" Save=\"FALSE\"/><Data /></Package>"
nack_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"98\" Reason=\"1\" Save=\"FALSE\"/><Data /></Package>"

# Checks if the packet sent was successful. If not,print on screen the meaning of the reason specified.
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


class ReaderBuffer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def setdata(self,s):
        self.socket = s
        self.msgs = []
        self.haskey = False
        self.key = ""
        self.connect = True
        self.catch = False
        self.wb = None
        self.gcount = 0
    def setWriterBuffer(self,wb):
        self.wb = wb
    def hasKey(self):
        return self.hasKey
    def getKey(self):
        return self.key
    def connected(self):
        return self.connected
    def run(self):

        while True:
            print "RECEPTOR >> " + str(mTimer.clock())
            self.catch = True
            if not self.connected:
                continue
            try:
                mbuffer = self.socket.recv(BUFFER_SIZE)
            except:
                continue
            pos = []
            notexit = True
            start = 0

            while notexit:
                pos1 = -1
                pos2 = -1
                try:
                    pos1 = mbuffer.index("<?xml",start)
                except:
                    notexit = False
                try:
                    pos2 = mbuffer.index("</Package>",start)
                except:
                    notexit = False
                if pos1 != -1 and pos2 != -1:
                    pos.append((pos1,pos2))
                    start = pos2 + 1
                else:
                    notexit = False
            while len(pos) > 0:
                self.gcount += 1
                tpos = pos.pop()
                nbuffer = mbuffer[ tpos[0] : tpos[1]+10 ]
                print "RECEPTOR [" + str(self.gcount) + "] >> " + nbuffer
                xml = None
                try:    
                    xml =  ElementTree.fromstring(nbuffer.strip(""))
                except:
                    if self.wb != None:
                        self.wb.send("nack")
                    continue
                if xml == None:
                    continue
                xmldict = XmlDictConfig(xml)
                self.msgs.append(xmldict)
                formatted_output = {}
                if xmldict['Header']['Id'] == '101':
                    if xmldict['Header']['Reason'] == '0':
                        self.key = xmldict['Data']['SecurityKey']
                        self.haskey = True
                elif xmldict['Header']['Id'] == '198':
                    formatted_output['Type'] = 'Tracking'
                    formatted_output['Identification'] = {}
                    formatted_output['Identification']['EquipType'] = productName(xmldict['TCA']['ProductId'])
                    formatted_output['Identification']['Serial'] = xmldict['TCA']['SerialNumber']
                    formatted_output['Identification']['Date'] = xmldict['Event']['EventDateTime']
                    formatted_output['Input'] = xmldict['Input']
                    formatted_output['LinearInput'] = xmldict['LinearInput']
                    formatted_output['Output'] = xmldict['Output']
                    formatted_output['GPS'] = xmldict['GPS']
                elif xmldict['Header']['Id'] == '106': 
                    formatted_output['Type'] = 'Command'
                    formatted_output['Identification'] = {}
                    formatted_output['Identification']['EquipType'] = xmldict['Data']['ProductId']
                    formatted_output['Identification']['Serial'] = xmldict['Data']['Serial']
                    formatted_output['Identification']['Date'] = xmldict['Header']['TimeStamp']
                    formatted_output['Status'] = xmldict['Data']['Status']
                elif xmldict['Header']['Id'] == '702':
                    formatted_output['Type'] = 'CarMeter'
                    formatted_output['Identification'] = {}
                    formatted_output['Identification']['EquipType'] = productName(xmldict['TCA']['ProductId'])
                    formatted_output['Identification']['Serial'] = xmldict['TCA']['SerialNumber']
                    formatted_output['Identification']['Date'] = xmldict['Datagram']['MsgDateTime']
                    formatted_output['Identification']['NetId'] = xmldict['Frame']['NetId']
                    formatted_output['Identification']['Address'] = xmldict['Frame']['Address']
                    formatted_output['Data'] = {}
                    formatted_output['Data']['Value'] = xmldict['Frame']['Message']
                elif xmldict['Header']['Id'] == '199':
                    self.connected = False
                else :
                    print "### " + xmldict['Header']['Id']
                    self.catch = False
                if self.catch and formatted_output.has_key('Type') and formatted_output['Type']!="":
                    print "#TO PROCESSOR"
                    processor_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    processor_client.connect((PROCESSOR_IP, PROCESSOR_PORT))
                    processor_client.send(json.dumps(formatted_output))
                    processor_client.close()
                self.socket.send(ack_msg)
                print ack_msg

        
class WriterBuffer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def setdata(self,s,key):
        self.socket = s
        self.msgs = []
        self.smsgs = []
        self.key = key
        self.init = True
    def hasKey(self):
        return self.haskey
    def setKey(self,key):
        self.key = key
        self.haskey = True


    def run(self):
        while True:
            if self.init:
                seckey_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"2\" /><Data SessionId=\""+self.key+"\" /></Package>"
                print seckey_msg
                self.socket.send(seckey_msg)
                mbuffer = self.socket.recv(BUFFER_SIZE)
                print "TRANSMISSOR >> " + mbuffer.strip("")
                self.init = False
            else:
                if len(self.smsgs) > 0:
                    print "# POP"
                    msg2send = self.smsgs.pop()
                    self.socket.send(msg2send)
                    print "SENT >> " + msg2send
                    
    def send(self,msg):
        print "# PUSH"
        if(msg=="nack"):
            nmsg = nack_msg
        else:
            nmsg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package>" + msg + "</Package>"
        self.smsgs.append(nmsg)

class Quanta(object):
    def __init__(self):
        self.key = ""
        self.read_s = 0
        self.write_s = 0
        self.rb = 0
        self.wb = 0
    def connect(self):
        self.read_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.read_s.connect((TCP_IP, TCP_PORT))
        self.read_s.settimeout(3)
        self.read_s.send(authentication_msg)
        print authentication_msg
        rb = ReaderBuffer()
        rb.setdata(self.read_s)
        rb.start()
        while True:
            if rb.haskey:
                break
        self.write_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.write_s.connect((TCP_IP, TCP_PORT))
        self.write_s.settimeout(3) #
#        self.write_s = self.read_s
        wb = WriterBuffer()
        wb.setdata(self.write_s,rb.getKey())
        wb.start()
        self.rb = rb
        self.wb = wb
    def send(self,cmd):
        if not self.rb.connected:
            self.connect()
        if cmd == "1":
            msg = "<Header Version=\"1.00\" Id=\"41\" /><Data Account=\"2\" ProductId=\"41\" Serial=\"000017E8\" Priority=\"3\" NetId=\"E7\" Address=\"00\" Format=\"HEX\" Value=\"0100000001\"/>"
            self.wb.send(msg)
        elif cmd == "2":
            msg = "<Header Version=\"1.00\" Id=\"41\" /><Data Account=\"2\" ProductId=\"41\" Serial=\"000017E8\" Priority=\"3\" NetId=\"E7\" Address=\"00\" Format=\"HEX\" Value=\"0200000002\"/>"
            self.wb.send(msg)
        elif cmd == "3":
            msg = "<Header Version=\"1.00\" Id=\"41\" /><Data Account=\"2\" ProductId=\"41\" Serial=\"000017E8\" Priority=\"3\" NetId=\"E7\" Address=\"00\" Format=\"HEX\" Value=\"0300000003\"/>"
            self.wb.send(msg)
        elif cmd == "4":
            msg = "<Header Version=\"1.00\" Id=\"41\" /><Data Account=\"2\" ProductId=\"41\" Serial=\"000017E8\" Priority=\"3\" NetId=\"E7\" Address=\"00\" Format=\"HEX\" Value=\"0400000004\"/>"
            self.wb.send(msg)
        elif cmd == "5":
            msg = "<Header Version=\"1.00\" Id=\"41\" /><Data Account=\"2\" ProductId=\"41\" Serial=\"000017E8\" Priority=\"3\" NetId=\"E7\" Address=\"00\" Format=\"HEX\" Value=\"0500000005\"/>"
            self.wb.send(msg)
        elif cmd == "A":
            msg = "<Header Version=\"1.00\" Id=\"41\" /><Data Account=\"2\" ProductId=\"41\" Serial=\"000017E8\" Priority=\"3\" NetId=\"E7\" Address=\"00\" Format=\"HEX\" Value=\"0A0000000A\"/>"
            self.wb.send(msg)
        elif cmd == "B":
            msg = "<Header Version=\"1.00\" Id=\"41\" /><Data Account=\"2\" ProductId=\"41\" Serial=\"000017E8\" Priority=\"3\" NetId=\"E7\" Address=\"00\" Format=\"HEX\" Value=\"0B0000000B\"/>"
            self.wb.send(msg)
        elif cmd == "C":
            msg = "<Header Version=\"1.00\" Id=\"41\" /><Data Account=\"2\" ProductId=\"41\" Serial=\"000017E8\" Priority=\"3\" NetId=\"E7\" Address=\"00\" Format=\"HEX\" Value=\"0C000001010E\"/>"
            self.wb.send(msg)

    def disconnect(self):
        turnoff = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"99\" SessionId=\""+self.key+"\" /></Package>"
        print turnoff
        self.read_s.send(turnoff)
        try:
            data = self.read_s.recv(BUFFER_SIZE)
            print data
            xml = ElementTree.fromstring(data[:len(data)-1])
            if reasonMsg(xml.find("Header").get("Reason"))==1 and xml.find("Header").get("Id") == "199" :
                return True
            return False
        except:
            return False
# >> ==================================================== +-------------------------------+-\
# >> ==================================================== | MAIN COMMAND PROCEDURE        |  >
# >> ==================================================== +-------------------------------+-/
class Command(BaseCommand):
    def handle(self, *args, **options):

        q = Quanta()
        q.connect()
        while True:
            cmd = raw_input()
            print "EXECUTING [" + cmd + "]"
            q.send(str(cmd))
        q.disconnect()
        return

        f = open("debug.txt","w")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        
        
        key = authentication(s)
        CPRSession.objects.all().delete()
        cprkey = CPRSession(key=key,time=datetime.now())
        cprkey.save()
        
        #mounting the XML response to server
        seckey_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"2\" /><Data SessionId=\""+key+"\" /></Package>"
        
        s.send(ack_msg)
        s.send(seckey_msg)
        
        self.stdout.write('>> Starting main loop.\n')
        while True:
            # if there is messages to read in the socket

            if ([s],[],[]) == select.select([s],[],[],0):
            
                # reads and inform the acknowledgement of the message
                inbox = s.recv(BUFFER_SIZE)
                print(inbox)

                s.send(ack_msg)
                                
                xml =  ElementTree.fromstring(inbox.strip(""))
                xmldict = XmlDictConfig(xml)
                #mounting the dict to be processed. The format used here should be the same for any other extractor build.
                formatted_output = {}
                
                # the XML is a tracking table
                if xmldict['Header']['Id'] == '198':
                    formatted_output['Type'] = 'Tracking'
                    formatted_output['Identification'] = {}
                    formatted_output['Identification']['EquipType'] = productName(xmldict['TCA']['ProductId'])
                    formatted_output['Identification']['Serial'] = xmldict['TCA']['SerialNumber']
                    formatted_output['Identification']['Date'] = xmldict['Event']['EventDateTime']

                    formatted_output['Input'] = xmldict['Input']
                    formatted_output['LinearInput'] = xmldict['LinearInput']
                    formatted_output['Output'] = xmldict['Output']
                    formatted_output['GPS'] = xmldict['GPS']
                
                #the XML is a command response
                elif xmldict['Header']['Id'] == '106': 
                    formatted_output['Type'] = 'Command'
                    formatted_output['Identification'] = {}
                    formatted_output['Identification']['EquipType'] = xmldict['Data']['ProductId']
                    formatted_output['Identification']['Serial'] = xmldict['Data']['Serial']
                    formatted_output['Identification']['Date'] = xmldict['Header']['TimeStamp']
                    formatted_output['Status'] = xmldict['Data']['Status']
                    
                elif xmldict['Header']['Id'] == '702':
                    formatted_output['Type'] = 'CarMeter'
                    formatted_output['Identification'] = {}
                    formatted_output['Identification']['EquipType'] = productName(xmldict['TCA']['ProductId'])
                    formatted_output['Identification']['Serial'] = xmldict['TCA']['SerialNumber']
                    formatted_output['Identification']['Date'] = xmldict['Datagram']['MsgDateTime']
                    formatted_output['Identification']['NetId'] = xmldict['Frame']['NetId']
                    formatted_output['Identification']['Address'] = xmldict['Frame']['Address']
                    formatted_output['Data'] = {}
                    formatted_output['Data']['Value'] = xmldict['Frame']['Message']
                    carm_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.00\" Id=\"41\" /><Data Account=\"2\" ProductId=\"41\" Serial=\"000017E8\" Priority=\"3\" NetId=\"E7\" Address=\"00\" Format=\"HEX\" Value=\"0300000003\"/></Package>"
                    s.send(carm_msg)
                    
                    
                processor_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                processor_client.connect((PROCESSOR_IP, PROCESSOR_PORT))
                processor_client.send(json.dumps(formatted_output))

                print  json.dumps(formatted_output, indent=4)
                        
                processor_client.close()
                exit(0)
                
                #remove that after debugging
                #exit(0)
