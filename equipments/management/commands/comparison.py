from itrack.geofence.models import Geofence
from django.contrib.gis.geos import Point


def AlertComparison(command,alert,customfield,value):
    
    # command.stdout.write(">>>> ")
    # command.stdout.write(str(alert.trigger.custom_field))
    # command.stdout.write(" sera comparado com ")
    # command.stdout.write(str(customfield))
    # command.stdout.write("\n")
    
    if(alert.trigger.custom_field == customfield):
      
        if customfield.type == 'Input':
          
            # command.stdout.write(">>>>>> ")
            # command.stdout.write(str(value))
            # command.stdout.write("\n")
          
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

def GeofenceComparison(request):
  
  return False
