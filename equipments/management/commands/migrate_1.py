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


class Command(BaseCommand):
        
    def handle(self, *args, **options):
        global main_stop
        eqs = Equipment.objects.all()
        for e in eqs:
            print(e.name)
            e.lasttrack_data = -1
            e.lasttrack_update = -1
            e.save()
