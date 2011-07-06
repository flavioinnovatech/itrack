from itrack.geofence.models import Geofence
from django.contrib.gis.geos import Point


def AlertComparison(command,alert,customfield,value):
    self.stdout.write('aisdasoidhas')
  
    if(alert.trigger.custom_field == customfield):
      
        if customfield.type == 'Input':
            print 'aidaidaidhaisdhashiu'
          
            if value == 'ON': value = True 
            else: value = False
            if value == alert.state:
                return True 
        else:
            if alert.state == False:
	        if int(value) < alert.linear_limit:
		    return True
            else:
	        if int(value) > alert.linear_limit:
		    return True
           
    return False
