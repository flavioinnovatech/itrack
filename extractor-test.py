import sys 
import socket
import os
from xml.etree import cElementTree as ElementTree

TCP_IP = '192.168.1.119' 	# the server IP address
TCP_PORT = 5000			# the server port
BUFFER_SIZE = 20000		# the maximum buffer size (in chars) for a TCP packet
USERNAME = "extractor"		# the user that will log on CPR
PASSWORD = "extractor"		# the password for this user 

# Messages that will be sent to CPR: the ACK and the first auth message
authentication_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"1\" /><Data User=\""+USERNAME+"\" Password=\""+PASSWORD+"\" /></Package>"

ack_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"98\" Reason=\"0\" Save=\"FALSE\"/><Data /></Package>"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

s.send(authentication_msg)
try:
	data = s.recv(BUFFER_SIZE)
except:
	print "Timeout!"
else:
	xml = ElementTree.fromstring(data[:len(data)-1])
	sec_key = xml.find("Data").get("SecurityKey")


seckey_msg = "<?xml version=\"1.0\" encoding=\"ASCII\" ?>\n<Package>\n  <Header Version=\"1.0\" Id=\"2\" />\n  <Data SessionId=\""+sec_key+"\" />\n</Package>"

print ">> Sending session start message."
print seckey_msg
s.send(seckey_msg)

try: 
	data = s.recv(BUFFER_SIZE)
	print data
except:
	pass

a = sys.stdin.readline()

