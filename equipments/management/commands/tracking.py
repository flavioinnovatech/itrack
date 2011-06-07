from equipments.models import Equipment, Tracking, TrackingData,CustomField
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
import time
from datetime import datetime

class Command(BaseCommand):
    args = 'no args'
    help = 'Insert one tracking to the database tables'
    
    table = {   'Comm': {   'GPSType': 'INTERNAL', 'RSSI': '4'},
    'Control': {   'Account': '2',
                   'CPRDateTime': '2011/05/31 21:22:00',
                   'MsgId': '377',
                   'Port': '3000',
                   'Provider': ''},
    'Datagram': {   'MsgDateTime': '2011/05/31 18:14:49', 'MsgType': 'TRACKING'},
    'Event': {   'EventDateTime': '2011/05/31 18:14:48'},
    'GPS': {   'Altitude': '647',
               'AltitudeStatus': 'VALID',
               'CableStatus': 'OK',
               'DateTime': '2011/05/31 18:14:44',
               'Lat': '-22.89531',
               'Long': '-47.06044',
               'NorthAngle': '51.9',
               'PosIsValid': 'TRUE',
               'SatNum': '7',
               'Speed': '0'},
    'Header': {   'Id': '198', 'Reason': '0', 'Version': '1.0'},
    'Input': {   'EDN2': 'ON', 'Ignition': 'ON', 'Panic': 'ON'},
    'LinearInput': {   'Odometer': '0', 'RPM': '0', 'Speed': '0'},
    'Output': None,
    'TCA': {   'ProductId': '41', 'SerialNumber': '000017E8', 'VersionId': '1.5'}}

    def handle(self, *args, **options):
        try:
            e = Equipment.objects.get(serial=self.table['TCA']['SerialNumber'])
            searchdate = datetime.strptime(self.table['Event']['EventDateTime'], "%Y/%m/%d %H:%M:%S")
            try:
                t = Tracking.objects.get(Q(equipment=e) & Q(eventdate=searchdate))
                self.stdout.write(str(t)+'\n')
                
            except:
                t = Tracking(equipment=e, eventdate= searchdate, msgtype=self.table['Datagram']['MsgType'])
                t.save()
                for k_type,d_type in self.table.items():
                    if type(d_type).__name__ == 'dict':
                        for k_tag,d_tag in d_type.items():
                            try:
                                c = CustomField.objects.get(Q(type=k_type)&Q(tag=k_tag))
                                tdata = TrackingData(tracking=t,type=c,value=d_tag)
                                tdata.save()
                            except:
                                pass
                    
            
        except KeyError:
            e = Equipment()
        
            
        

