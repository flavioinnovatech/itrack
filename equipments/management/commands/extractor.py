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

from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from itrack.equipments.models import Equipment, Tracking, TrackingData,CustomField
from itrack.alerts.models import Alert,Popup
from itrack.vehicles.models import Vehicle
from itrack.accounts.models import UserProfile
from comparison import AlertComparison




def SendSMS(to,msg):

    respostas = { "000" : "000 - Mensagem enviada com sucesso!", 
	    "010" : "010 - Mensagem sem conteudo.",
	    "011" : "011 - Mensagem invalida.",
	    "012" : "012 - Destinatario vazio.",
	    "013" : "013 - Destinatario invalido.", 
	    "014" : "014 - Destinatario vazio",
	    "080" : "080 - ID ja usado.",
	    "900" : "900 - Erro de autenticacao na conta.",
	    "990" : "990 - Creditos insuficientes.",
	    "999" : "999 - Erro desconhecido."
    }

    account = 'infotrack'
    code = '8OcDN8nVzx'

    if len(str(to)) <= 10:
        to = '55'+ str(to)
    else:
        to = str(to)
    #to = '551481189826'
    #to = 'xx1234567890'

    # Prepara a mensagem com URL Encode
    msgUrl = urlencode({'msg':msg})

    # Tenta abrir a URL indicada
    url  = "http://system.human.com.br/GatewayIntegration/msgSms.do?dispatch=send&account=" + account + "&code=" + code + "&to=" + to + "&" + msgUrl
    conexao = urllib.urlopen(url)
    conteudo = conexao.read()
    conexao.close()

    codigo = conteudo[0:3]

    # Retorna resposta para o usuario
    try:
	    return respostas[codigo]
    except:
	    return conteudo



class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})


TCP_IP = '187.115.25.240' 	# the server IP address
TCP_PORT = 5000			# the server port
BUFFER_SIZE = 20000		# the maximum buffer size (in chars) for a TCP packet
USERNAME = "extractor"		# the user that will log on CPR
PASSWORD = "extractor"		# the password for this user 


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




class Command(BaseCommand):
    args = 'no args'
    help = 'Extract info from CPR'
    
    def handle(self, *args, **options):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))

        #s.connect((TCP_IP, TCP_PORT))
        #sending the auth message, receiving the response and sending an ack message
        key = authentication(s)
        #mounting the XML response to server
        seckey_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"2\" /><Data SessionId=\""+key+"\" /></Package>"
        close_msg =  "<?xml version=\"1.0\" encoding=\"ASCII\"?>\n<Package>\n  <Header Version=\"1.0\" Id=\"99\" />\n  <Data SessionId=\""+key+"\" />\n</Package>"

        #sending the response to the server, and awaiting the outbox message
        s.send(ack_msg)
        s.send(seckey_msg)
        data = s.recv(BUFFER_SIZE)
        s.send(ack_msg)

        #listening all information given by CPR.

        while 1:
            if ([s],[],[]) == select.select([s],[],[],0):
                outbox = s.recv(BUFFER_SIZE)
                s.send(ack_msg)
                try:
                  xml =  ElementTree.fromstring(outbox.strip(""))
                  xmldict = XmlDictConfig(xml)
                  try:
                      e = Equipment.objects.get(serial=xmldict['TCA']['SerialNumber'])
                      searchdate = datetime.strptime(xmldict['Event']['EventDateTime'], "%Y/%m/%d %H:%M:%S")
                      try:
                          t = Tracking.objects.get(Q(equipment=e) & Q(eventdate=searchdate))
                    
                      except ObjectDoesNotExist:
                          t = Tracking(equipment=e, eventdate=searchdate, msgtype=xmldict['Datagram']['MsgType'])
                          t.save()
                          for k_type,d_type in xmldict.items():
                              if type(d_type).__name__ == 'dict':
                                  for k_tag,d_tag in d_type.items():
                                      try:
                                          c = CustomField.objects.get(Q(type=k_type)&Q(tag=k_tag))
                                          tdata = TrackingData(tracking=t,type=c,value=d_tag)
                                          tdata.save()
                                      except ObjectDoesNotExist:
                                          pass
                          self.stdout.write('>> The tracking table sent on '+str(searchdate)+' for the equipment '+ xmldict['TCA']['SerialNumber'] +' has been saved successfully.\n')
                        
      #      Here is the main alert handler. First, queries the database looking if there's some alert that matches the 
      # received tracking. After that, for each alert in the result of the query, alert in each way available.
                        
                          #get the vehicle object
                          vehicle = Vehicle.objects.get(equipment = e)
                          
                          if vehicle.last_alert_date is not None:                            
                              total_seconds = (searchdate - vehicle.last_alert_date).days * 24 * 60 * 60 + (searchdate - vehicle.last_alert_date).seconds
                              self.stdout.write(str(total_seconds)+'\n')
                              self.stdout.write(str(vehicle.threshold_time*60)+'\n')
                            
                              #checks if there's enough time between the last alert sent and a possibly new one
                              if total_seconds > vehicle.threshold_time*60:
                                  self.stdout.write('>> Alert threshold reached.\n')
                                  vehicle.last_alert_date = searchdate
                                  vehicle.save()
                                
                                  alerts = Alert.objects.filter(Q(vehicle=vehicle) & Q(time_end__gte=searchdate) & Q(time_start__lte=searchdate) & Q(active=True))
                                  
                                  
                                  #iterates over the inputs and checks if it is needed to send the alert
                                  for k_type,d_type in dict(xmldict['Input'].items() + xmldict['LinearInput'].items()).items():       
                                              self.stdout.write(str(k_type)+'\n')
                                              try:
                                                  c = CustomField.objects.get(Q(tag=k_type)& ~Q(type='GPS'))

                                                  #function that returns true if the alert shall be sent, and false if not.
                                                  for alert in alerts:
                                                      if AlertComparison(self,alert,c,d_type):         
                                                          self.stdout.write('entrou no Alert Comparison')
                                                          
                                                          if alert.receive_email:
                                                            for destinatary in alert.destinataries.values():
                                                              send_mail(str(alert), str(alert), "infotrack@infotrack.com.br", [destinatary['email']], fail_silently=False, auth_user=None, auth_password=None, connection=None)
                                                            
                                                          if alert.receive_sms:
                                                              for destinatary in alert.destinataries.values():
                                                                
                                                                  self.stdout.write(str(destinatary['username']) + '-> ')
                                                                  cellphone = UserProfile.objects.get(profile__id = destinatary['id']).cellphone                                               
                                                                  self.stdout.write(str(cellphone))
                                                                  self.stdout.write(SendSMS(cellphone,'[INFOTRACK] O alerta: "'+str(alert)+u'" foi disparado pelo veiculo '+str(vehicle)+'.')+'\n')                                                

                                                          if alert.receive_popup:
                                                              for destinatary in alert.destinataries.all():
                                                                  popup = Popup(alert=alert,user=destinatary,vehicle=vehicle,date=searchdate)
                                                                  popup.save()             
                                              except ObjectDoesNotExist:
                                                  self.stdout.write('Erro no Custom Field\n')
                                                  pass
                          else:
                              vehicle.last_alert_date = searchdate
                              vehicle.save()
                            
                               
                        
                          #self.stdout.write(str(searchdate)+'\n')
                          #self.stdout.write(str(a_set[1]["time_start"])+' >> '+str(a_set[1]["time_start"] < searchdate) +'\n')
                          #self.stdout.write(str(a_set[1]["time_end"])+' >> '+str(a_set[1]["time_end"] > searchdate) +'\n')
                        
                        
                        
                
                  except ObjectDoesNotExist:
                      pass
                  except KeyError:
                      pass
                except:
                  pass
