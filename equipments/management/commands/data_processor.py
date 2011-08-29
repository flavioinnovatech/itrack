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

clientPool = Queue.Queue ( 0 )
PROCESSOR_PORT = settings.PROCESSOR_PORT

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
            print inbox
            
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
            time.sleep(1)
            client[0].close()
            print 'Closed connection:', client[1][0]

class Command(BaseCommand):
    def handle(self, *args, **options):
    
        #TODO: get from the database all the equipment types

        # Start two threads:
        for x in xrange ( 2 ):
            ClientThread().start()

        # Set up the server:
        server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        server.bind ( ( '', PROCESSOR_PORT ) )
        server.listen ( 5 )

        # Have the server serve "forever":
        while True:
            clientPool.put ( server.accept() )
