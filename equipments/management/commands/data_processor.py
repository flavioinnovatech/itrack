# -*- coding:utf-8 -*-
import sys 
import socket
import select
import json
import Queue
import threading

from datetime import datetime
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from itrack.equipments.models import Equipment, Tracking, TrackingData,
                                     CustomField,EquipmentType
from itrack.alerts.models import Alert,Popup
from itrack.vehicles.models import Vehicle

#some globals and constants
#--------------------------
PROCESSOR_PORT = settings.PROCESSOR_PORT
clientPool = Queue.Queue (0)
equipTypeDict = {}

# >> ====================================== +-------------------------------+-\
# >> ====================================== | THREAD TO PROCESS THE DATA    |  >
# >> ====================================== +-------------------------------+-/

class ClientThread(threading.Thread):
   def run ( self ):
      # Have our thread serve "forever":
      while True:

         # Get a client out of the queue
         client = clientPool.get()

         # Check if we actually have an actual client in the client variable:
         if client != None:

            print 'Received connection:', client[1][0]
            inbox =  client[0].recv(1024)
            
            datadict = json.loads(inbox)
            
            # BIG BAD TODO:
            '''
                   (    )            +--------------------------------------+
                  ((((()))           |  CONVERTER O EXTRACTOR AQUI DENTRO   |
                  |o\ /o)|           |  DO PROCESSOR, É SÓ EXECUTAR TODOS   |
                  ( (  _')          <   OS PASSOS JÁ FEITOS LÁ, E DAR UMA   |
                   (._.  /\__        |  ARRUMADA NO CÓDIGO DE RECONHECIM-   |
                  ,\___,/ '  ')      |  ENTO DE EQUIPAMENTO.                |
    '.,_,,       (  .- .   .    )    +--------------------------------------+
     \   \\     ( '        )(    )
      \   \\    \.  _.__ ____( .  |
       \  /\\   .(   .'  /\  '.  )
        \(  \\.-' ( /    \/    \)
         '  ()) _'.-|/\/\/\/\/\|
             '\\ .( |\/\/\/\/\/|
               '((  \    /\    /
               ((((  '.__\/__.')
                ((,) /   ((()   )
                 "..-,  (()("   /
                  _//.   ((() ."
          _____ //,/" ___ ((( ', ___
                           ((  )
                            / /
                          _/,/'
                        /,/,"
            '''
            
            # tries to pick the equipment and the date of the tracking table
            try:
                #first, check if the equipment exists
                e = Equipment.objects.get(
                    Q(serial=datadict['Identification']['Serial'])&
                    Q(type=datadict['Identification']['EquipType'])
                    )
                try:
                    #second, if the vehicle exists, for that given equipment, 
                    #
                    v = Vehicle.objects.get(equipment=e)
                    sys = lowestDepth(e.system.all())
                except ObjectDoesNotExist:
                    # TODO: does nothing if gets here
                    pass
            except ObjectDoesNotExist:
                #TODO: create equipment under the root system
                pass
            
            searchdate = datetime.strptime(xmldict['Event']['EventDateTime'], 
                        "%Y/%m/%d %H:%M:%S")
            
            time.sleep(1)
            client[0].close()
            print 'Closed connection:', client[1][0]

# >> ====================================== +-------------------------------+-\
# >> ====================================== | MAIN COMMAND PROCEDURE        |  >
# >> ====================================== +-------------------------------+-/

class Command(BaseCommand):
    def handle(self, *args, **options):
    
        #TODO: get from the database all the equipment types
        
        #types = EquipmentType.objects.all()
        cfs = CustomField.objects.select_related().all()
        for cf in cfs:
            for etype in cf.equipmenttype_set.all():
                equipTypeDict.setdefault(int(etype.product_id), []).append(cf)
        
        # Start two threads:
        for x in xrange(2):
            ClientThread().start()

        # Set up the server:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', PROCESSOR_PORT))
        server.listen(5)
        print "Server listening. The recognized equipment types are:"
        print EquipTypeDict
        # Have the server serve "forever":
        while True:
            clientPool.put(server.accept())
