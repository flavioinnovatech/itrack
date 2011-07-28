# -*- coding: utf-8 -*-

from django.contrib.gis.geos import Point
from django.core.mail import send_mail

from itrack.alerts.models import Popup
from itrack.geofence.models import Geofence
from itrack.accounts.models import UserProfile

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
        elif customfield.type == 'LinearInput':
            if alert.state == False:
                if int(value) < alert.linear_limit:
	                return True
                else:
                    if int(value) > alert.linear_limit:
	                    return True
           
    return False

def GeofenceComparison(command,alert,lat,lng):
    lat = float(lat)
    lng = float(lng)
    return False

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

  
def AlertSender(command,alert,vehicle):
    #if the alert shall be sent by email
    if alert.receive_email:

        for destinatary in alert.destinataries.values():
            send_mail('[INFOTRACK] ' + str(alert), 'Veículo:'+str(vehicle)+'\n'+'Alerta:'+str(alert.alerttext), "infotrack@infotrack.com.br", [destinatary['email']], fail_silently=False, auth_user=None, auth_password=None, connection=None)
            command.stdout.write('>>>> Email de alerta enviado.\n')
               
        #if the alert shall be sent by SMS 
        #TODO: if needed, optimize the get database lookup to one big lookup and iterate over this list
    if alert.receive_sms:
      for destinatary in alert.destinataries.values():
          cellphone = UserProfile.objects.get(profile__id = destinatary['id']).cellphone                                               
          command.stdout.write(SendSMS(cellphone,'[INFOTRACK]\n'+'Veiculo: '+str(vehicle)+'\n'+'Alerta:'+str(alert.alerttext)))
          # self.stdout.write(SendSMS(cellphone,'[INFOTRACK]\n'+'Alerta:'+str(alert.alerttext)))
          command.stdout.write('>>>> SMS de alerta enviado.\n')

    #if the alert shall display a popup on the user screen
    if alert.receive_popup:
      for destinatary in alert.destinataries.all():
          popup = Popup(alert=alert,user=destinatary,vehicle=vehicle,date=searchdate)
          popup.save()
