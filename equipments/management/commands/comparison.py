



def AlertComparison(command,alert,customfield,value):
    if(alert.trigger.custom_field == customfield):
        if customfield.type == 'Input':
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
