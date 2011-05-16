#!/usr/bin/env python
import sys 
import socket
import elementtree.ElementTree as ET
import sys
import select 
import tty 
import termios

TCP_IP = '192.168.0.151'
TCP_PORT = 5000
BUFFER_SIZE = 20000
USERNAME = "extractor"
PASSWORD = "extractor"

authentication_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"1\" /><Data User=\""+USERNAME+"\" Password=\""+PASSWORD+"\" /></Package>"

ack_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"98\" Reason=\"0\" Save=\"FALSE\"/><Data /></Package>"

#helper function that tells if there's any data on stdin to be read
def isData():
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

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
        print authentication_msg
        
        data = s.recv(BUFFER_SIZE)
        print data
        s.send(ack_msg)
        
        xml = ET.fromstring(data[:len(data)-1])
        msg_reason = xml.find("Header").get("Reason")
        
        if reasonMsg(msg_reason):
            sec_key = xml.find("Data").get("SecurityKey")
        else:
            exit(int(msg_reason))
        return sec_key
    except:
        exit(1)
        
        
print " \n\n\t\tWelcome to Infotrack Bridge.\n\n"
print ">> Trying to connect to the server",TCP_IP + ":" + str(TCP_PORT)+"."

#creating and connecting trough the TCP socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(20)
s.connect((TCP_IP, TCP_PORT))
s.send(ack_msg)

#sending the auth message, receiving the response and sending an ack message
print ">> Connection established. Sending authentication protocol."
key = authentication(s)
print "\n>> Authentication successful. Security key:",key


#mounting the XML response to server
seckey_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?>\n<Package>\n  <Header Version=\"1.0\" Id=\"2\" />\n  <Data SessionId=\""+key+"\" />\n</Package>"
close_msg =  "<?xml version=\"1.0\" encoding=\"ASCII\"?>\n<Package>\n  <Header Version=\"1.0\" Id=\"99\" />\n  <Data SessionId=\""+key+"\" />\n</Package>"
print ">> Sending session start message."


#sending the response to the server, and awaiting the outbox message
s.send(seckey_msg)
switch = 0
#
positions = []
while 1:
    try:
        outbox = s.recv(BUFFER_SIZE)
    except:
        s.close()
    else:
        s.send(ack_msg)
        if switch == 0:
            print outbox
            switch = 1
        xml =  ET.fromstring(outbox.strip(""))
        
        elemento = [ xml.find("GPS").get("Lat") , xml.find("GPS").get("Long") ]
        if elemento not in positions:
            positions.append(elemento)
        else:
            print elemento, "already on the list"
            positions.remove(elemento)
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            if isData():
                ch = sys.stdin.read(1)
                
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

        

        
                
        
        

    
