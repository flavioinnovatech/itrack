
import datetime
import socket   
import subprocess   

class XmlTag(object):
   def __init__(self,tagname):
      self.tagName = tagname
      self.mlist = []
      self.preval = ""
      self.posval = ""
   def begin(self):
      return "\n<" + self.tagName + ">"
   def content(self):
      ret = ""
      if len(self.mlist) > 0:
       for i in self.mlist:
          ret += i.mount()
      return ret
   def end(self):
      return "</" + self.tagName + ">"
   def mount(self):
      return self.begin() + self.preval + self.content() + self.posval + self.end()   
   def tagkv(self, key, val) :
      item = XmlTag(key)
      item.preval = val
      self.append(item)      
   def append(self,tag):
      self.mlist.append(tag)
class Param(XmlTag):
   def __init__(self,id,val):
      super(Param,self).__init__("PARAMETER")
      self.tagkv("ID",id)
      self.tagkv("VALUE",val)
class Params(XmlTag):
   def __init__(self):
      super(Params,self).__init__("PARAMETERS")
   def add(self, id, val):
      self.append(Param(id,val))
class Cmd(XmlTag):
   def __init__(self,protocol="",serial="",idcmd="",type="",attempts="",timeout=""):
      super(Cmd,self).__init__("COMMAND")
      self.protocol = protocol
      self.serial = serial
      self.idcmd = idcmd
      self.type = type
      self.attempts = attempts
      self.timeout = timeout
      self.params = Params()
   def load(self):
      self.mlist = []
      self.tagkv("PROTOCOL",self.protocol)
      self.tagkv("SERIAL",self.serial)
      self.tagkv("ID_COMMAND",self.idcmd)
      self.tagkv("TYPE",self.type)
      self.tagkv("ATTEMPTS",self.attempts)
      self.tagkv("COMMAND_TIMEOUT",self.timeout)
      self.append(self.params)
class Cmds(XmlTag):
   def __init__(self,protocol,serial,timeout):
      self.serial = serial
      self.protocol = str(protocol)
      self.timeout = datetime.datetime.today()+datetime.timedelta(seconds=timeout)
      self.timeoutstr = ""
      self.timeoutstr += str(self.timeout.year) + "-"
      if self.timeout.month < 10:
       self.timeoutstr += "0" + str(self.timeout.month) + "-"
      else:
       self.timeoutstr += str(self.timeout.month) + "-"
      if self.timeout.day < 10:
       self.timeoutstr += "0" + str(self.timeout.day) + " "
      else:
       self.timeoutstr += str(self.timeout.day) + " "
      if self.timeout.hour < 10:
       self.timeoutstr += "0" + str(self.timeout.hour) + ":"
      else:
       self.timeoutstr += str(self.timeout.hour) + ":"
      if self.timeout.minute < 10:
       self.timeoutstr += "0" + str(self.timeout.minute) + ":"
      else:
       self.timeoutstr += str(self.timeout.minute) + ":"
      if self.timeout.second < 10:
       self.timeoutstr += "0" + str(self.timeout.second)
      else:
       self.timeoutstr += str(self.timeout.second)
      
      super(Cmds,self).__init__("COMMANDS")

   def load(self):
      for i in self.mlist:
       i.load()
   def mount(self):
      self.load();
      return super(Cmds,self).mount();
      
      
   def MTCActivateOutput(self):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCActivateOutput",type="0",attempts="3",timeout=self.timeoutstr)
      self.append(ret)
   def MTCDeactivatePanic(self):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCDeactivatePanic",type="1",attempts="3",timeout=self.timeoutstr)
      self.append(ret)
   def MTCOutputControl(self,id,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCOutputControl",type="2",attempts="3",timeout=self.timeoutstr)
      ret.params.add("OUTPUT"+str(id),val)
      self.append(ret)
   def MTCDealayInterval(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCActivateOutput",type="3",attempts="3",timeout=self.timeoutstr)
      ret.params.add("INTERVAL",str(val))
      self.append(ret)
   def MTCInformationConfigRouteReference(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTInformationConfigRouteReference",type="4",attempts="3",timeout=self.timeoutstr)
      ret.params.add("ROUTE_REFERENCE","1" if val else "0")
      self.append(ret)
   def MTCInformationConfigLatitudeLongitude(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCInformationConfigLatitudeLongitude",type="4",attempts="3",timeout=self.timeoutstr)
      ret.params.add("LATITUDE_LONGITUDE","1" if val else "0")
      self.append(ret)
   def MTCInformationConfigVelocityDirection(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCInformationConfigVelocityDirection",type="4",attempts="3",timeout=self.timeoutstr)
      ret.params.add("VEL_DIR","1" if val else "0")
      self.append(ret)
   def MTCInformationConfigInputOutput(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCInformationConfigInputOutput",type="4",attempts="3",timeout=self.timeoutstr)
      ret.params.add("INPUT_OUTPUT","1" if val else "0")
      self.append(ret)
   def MTCInformationConfigCount(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCInformationConfigCount",type="4",attempts="3",timeout=self.timeoutstr)
      ret.params.add("COUNT","1" if val else "0")
      self.append(ret)
   def MTCInformationConfigTemperature(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCInformationConfigTemperature",type="4",attempts="3",timeout=self.timeoutstr)
      ret.params.add("TEMPERATURE","1" if val else "0")
      self.append(ret)
   def MTCInformationConfigOdometer(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCInformationConfigOdometer",type="4",attempts="3",timeout=self.timeoutstr)
      ret.params.add("ODOMETER","1" if val else "0")
      self.append(ret)
   def MTCInformationConfigHourmeter(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCInformationConfigHourmeter",type="4",attempts="3",timeout=self.timeoutstr)
      ret.params.add("HOURMETER","1" if val else "0")
      self.append(ret)
   def MTCSleepMode(self,val):
      #MTC40 val in hours, MTC500 val in minutes
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCSleepMode",type="5",attempts="3",timeout=self.timeoutstr)
      ret.params.add("SLEEPMODE",str(val))
      self.append(ret)

   def MTCMaxSpeedKnots(self,knots):
      # 1KNOT = 1,852km/h
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCMaximunSpeedKnots",type="6",attempts="3",timeout=self.timeoutstr)
      ret.params.add("MAXIMUNSPEEDKNOTS",str(val))
      self.append(ret)
   def MTCGPSSleepMode(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCGPSDelaySeconds",type="7",attempts="3",timeout=self.timeoutstr)
      ret.params.add("GPSDELAYSECONDS",str(val))
      self.append(ret)
   def MTCTransmitDtmfOnInput(self,id,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCTransmitDtmfOnInput",type="8",attempts="3",timeout=self.timeoutstr)
      ret.params.add("TRANSMIT_ACTIVATE_INPUT","1" if val else "0")
      self.append(ret)
   def MTCTransmitDtmfOnIgnition(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCTransmitDtmfOnIgnition",type="8",attempts="3",timeout=self.timeoutstr)
      ret.params.add("TRANSMIT_IGNITION_CHANGE","1" if val else "0")
      self.append(ret)
   def MTCTransmitGprsOnAny(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCTransmitGprsOnAny",type="8",attempts="3",timeout=self.timeoutstr)
      ret.params.add("TRANSMIT_TIME_TRANSMISSION_WITH_IGNITION_OFF","1" if val else "0")
      self.append(ret)
   def MTCTransmitOnPanic(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCTransmitOnPanic",type="8",attempts="3",timeout=self.timeoutstr)
      ret.params.add("AUDIO_INPUT_ONLY_DURING_PANIC","1" if val else "0")
      self.append(ret)
   def MTCTransmitOnSpeedExcess(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCTransmitOnSpeedExcess",type="8",attempts="3",timeout=self.timeoutstr)
      ret.params.add("TRANSMIT_SPEED_EXCESS","1" if val else "0")
      self.append(ret)
   def MTCTransmitOnVoltagePeak(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCTransmitOnVoltagePeak",type="8",attempts="3",timeout=self.timeoutstr)
      ret.params.add("TRANSMIT_TEMPERATURE_TENSAO_ALERT","1" if val else "0")
      self.append(ret)
   def MTCStandardVoiceNumber(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCStandardVoiceNumber",type="9",attempts="3",timeout=self.timeoutstr)
      ret.params.add("STANDARDVOICENUMBER",str(val))
      self.append(ret)
   def MTCPanicVoiceNumber(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCPanicVoiceNumber",type="10",attempts="3",timeout=self.timeoutstr)
      ret.params.add("PANICVOICENUMBER",str(val))
      self.append(ret)
   def MTCAuxOuputData(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCAuxOutputData",type="12",attempts="3",timeout=self.timeoutstr)
      ret.params.add("MTCAUXOUTPUTDATA",str(val))
      self.append(ret)
   def MTCWayPointActivate(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCWayPointActivate",type="13",attempts="3",timeout=self.timeoutstr)
      ret.params.add("WAYPOINTACTIVATE","1" if val  else "0")
      self.append(ret)
   def MTCConfigModemTransmitUsingSMS(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCConfigModemTransmitUsingSMS",type="14",attempts="3",timeout=self.timeoutstr)
      ret.params.add("TRANSMIT_USING_SMS","1" if val  else "0")
      self.append(ret)
   def MTCConfigModemForceGPS(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCConfigModemForceGPS",type="14",attempts="3",timeout=self.timeoutstr)
      ret.params.add("FORCE_GPS","1" if val  else "0")
      self.append(ret)
   def MTCConfigModemFillBufferBeforeSendSMS(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCConfigModemFillBufferBeforeSendSMS",type="14",attempts="3",timeout=self.timeoutstr)
      ret.params.add("FILL_BUFFER_BEFORE_SEND_SMS","1" if val  else "0")
      self.append(ret)
   def MTCConfigModemVoiceConnectionInput4(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCConfigModemVoiceConnectionInput4",type="14",attempts="3",timeout=self.timeoutstr)
      ret.params.add("VOICE_CONNECTION_INPUT4","1" if val  else "0")
      self.append(ret)
   def MTCConfigModemActiveOutput4OnInvalidPacket(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCConfigModemActiveOutput4OnInvalidPacket",type="14",attempts="3",timeout=self.timeoutstr)
      ret.params.add("ACTIVE_OUTPUT4_ON_INVALID_PACKET","1" if val  else "0")
      self.append(ret)
   def MTCConfigModemTransmitUsingGPRS(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCConfigModemTransmitUsingGPRS",type="14",attempts="3",timeout=self.timeoutstr)
      ret.params.add("TRANSMIT_USING_GPRS","1" if val  else "0")
      self.append(ret)
   def MTCScheduleDial(self,slot,hour,minute,day):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCScheduleDial",type="15",attempts="3",timeout=self.timeoutstr)
      ret.params.add("CLEAR_ALL_SCHEDULE","0")
      ret.params.add("SLOT",str(slot))
      ret.params.add("HOUR",str(hour))
      ret.params.add("MINUTE",str(day))
      self.append(ret)
   def MTCClearScheduleDial(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCClearScheduleDial",type="15",attempts="3",timeout=self.timeoutstr)
      ret.params.add("CLEAR_ALL_SCHEDULE","1" if val else "0")
      ret.params.add("CLEAR_SCHEDULE_GPRS","1" if val else "0")
      self.append(ret)
   def MTCAbsoluteOdometer(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCClearScheduleDial",type="18",attempts="3",timeout=self.timeoutstr)
      ret.params.add("MTCABSOLUTEODOMETERMETERS",str(val))
      self.append(ret)
   def MTCAbsoluteHourmeter(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCAbsoluteHourmeter",type="19",attempts="3",timeout=self.timeoutstr)
      ret.params.add("ABSOLUTEHOURMETERHOURS",str(val))
      self.append(ret)
   def MTCOdometerFactorPulseKm(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCOdometerFactorPulseKm",type="20",attempts="3",timeout=self.timeoutstr)
      ret.params.add("ODOMETERFACTORPULSESKM",str(val))
      self.append(ret)
   def MTCGprsApn(self,val):
      if len(str(val)) < 30:
       ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCGprsApn",type="21",attempts="3",timeout=self.timeoutstr)
       ret.params.add("GPRSAPN",str(val))
       self.append(ret)
   def MTCGprsPort(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCGprsPort",type="22",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("MTCGPRSPORT",str(val))
      self.append(ret)
   def MTCEndTrip(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCEndTrip",type="23",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCGprsSecondaryIP(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCGprsSecondaryIP",type="24",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("GPRSECONDARYIP",str(val))
      self.append(ret)
   def MTCGprsRequestSetup(self): #THIS COMMAND HAS A RESPONSE
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCGprsRequestSetup",type="25",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCGprsMaintananceIP(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCGprsMaintananceIP",type="26",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("GPRSMAINTANANCEIP",str(val))
      self.append(ret)
   def MTCWayPointFilter(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCWayPointFilter",type="27",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("WAYPOINTFILTER",str(val))
      self.append(ret)
   def MTCStopSpeedTimeSeconds(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCStopSpeedTimeSeconds",type="28",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("STOPPEDTIMESECONDS",str(val))
      self.append(ret)
   def MTCRequestPositionFromIndex(self,val1,val2):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCRequestPositionFromIndex",type="31",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("QUANTITY",str(val))
      ret.params.add("INDEX",str(val))
      self.append(ret)
   def MTCEraseDynamicWayPoints(self):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCEraseDynamicWayPoints",type="32",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCRemoveExternalWayPoints(self):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCRemoveExternalWayPoints",type="33",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCDynamicReference(self,name,path):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCDynamicReference",type="29",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("NAME",str(val))
      ret.params.add("PLACE",str(val))
      self.append(ret)    
   def MTCForceMaintananceIP(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCDynamicReference",type="35",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("GPRSMAINTANANCEIP",str(val))
      self.append(ret)
   def MTCForcePrimaryIP(self):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCForcePrimaryIP",type="36",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCSerialOutputData(self,val): #HEX512
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCDynamicReference",type="37",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("SERIALOUTPUTDATA",str(val))
      self.append(ret)
   def MTCVoiceCallback(self,val):#NSTRING(19)
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCVoiceCallback",type="38",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("VOICECALLBACK",str(val))
      self.append(ret)
   def MTCBatchConfig(self,val): #USHORT
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCBatchConfig",type="41",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("BATCHCONFIG",str(val))
      self.append(ret)
   def MTCInternalStaticReference(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCInternalStaticReference",type="49",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("NAME",str(val))
      ret.params.add("PLACE",str(val))
      self.append(ret)
   def MTCCycleTimerOutput(self,port,init,off,on,cyles):#4outputs#
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCInternalStaticReference",type="51",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("OUTPUT_"+str(port)+"_INITIAL_STATE",str(init))
      ret.params.add("OUTPUT_"+str(port)+"_TIME_OFF",str(off))
      ret.params.add("OUTPUT_"+str(port)+"_TIME_ON",str(on))
      ret.params.add("OUTPUT_"+str(port)+"_CYCLES",str(cyles))
      self.append(ret)
   def MTCVoiceTransmissionIntervalMinutes(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCVoiceTransmissionIntervalMinutes",type="52",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("INTERVAL",str(val))
      self.append(ret)
   def MTCSMSNumber(self,val): #NSTRING
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCVoiceTransmissionIntervalMinutes",type="53",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("SMSNUMBER",str(val))
      self.append(ret)
   def MTCStandardVoiceNumber(self,val): #NSTRING
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCStandardVoiceNumber",type="54",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("MTCSTANDARDVOICENUMBER",str(val))
      self.append(ret)
   def MTCDelayInterval2Gprs(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCDelayInterval2Gprs",type="55",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("INTERVAL",str(val))
      self.append(ret)
   def MTCDelayInterval2DTMF(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCDelayInterval2DTMF",type="56",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("INTERVAL",str(val))
      self.append(ret)

   def MTCExternalFileReference(self,name,place):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCExternalFileReference",type="38",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("NAME",str(val))
      ret.params.add("PLACE",str(val))
      self.append(ret)    
   def MTCForceGPS(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCForceGPS",type="39",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("FORCEGPS",str(val))
      self.append(ret)
   def MTCPeripheralCode(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCPeripheralCode",type="42",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("PERIPHERALCODE",str(val))
      self.append(ret)
   def MTCChangeApnUser(self,val): #STRING*
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCChangeApnUser",type="43",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("USERGPRS",str(val))
      self.append(ret)
   def MTCPasswordGprs(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCPasswordGprs",type="44",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("PASSWORDGPRS",str(val))
      self.append(ret)
   def MTCEraseExternalMemory(self):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCEraseExternalMemory",type="45",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCTimeZoneConfig(self):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCTimeZoneConfig",type="46",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("TIMEZONECONFIG",str(val))
      self.append(ret)
   def MTCSetFirmware(self,name,path):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCSetFirmware",type="47",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("NAME",str(name))
      ret.params.add("PLACE",str(path))
      self.append(ret)
   def MTCVoltagePeakLimit(self,val1,val2):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCVoltagePeakLimit",type="57",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("TENSAO",str(val1) + "." + str(val2))
      self.append(ret)
   def MTCAuxPortBaud(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCAuxPortBaud",type="58",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("BAUD",str(val))
      self.append(ret)
   def MTCAuxPortTimeoutSeconds(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCAuxPortTimeoutSeconds",type="59",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("INTERVAL",str(val))
      self.append(ret)
   def MTCGprsPause(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCGprsPause",type="60",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("PAUSE","1" if val else "0")
      self.append(ret)
   def MTCSetOutput(self,port,val): #8 outputs, might have the need to fullfill all the outputs
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCSetOutput",type="63",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("ACTION","1" if val else "0")
      ret.params.add("OUTPUT" + str(port),"1" if val else "0")
      self.append(ret)
   def MTCSleepNow(self):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCSleepNow",type="61",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCForceIgnition(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCForceIgnition",type="64",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("INTERVAL",str(val))
      self.append(ret)
   def MTCRpmFactor(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCRpmFactor",type="65",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("RPM_FACTOR",str(val))
      self.append(ret)
   def MTCConfigParam(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCConfigParam",type="66",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("OUTPUT1_AS_GRADATIVE_BLOCK",str(val))
      ret.params.add("SEND_GPS_STRING_ON_RS232",str(val))
      ret.params.add("SEND_GPS_STRING_ON_RS485",str(val))
      ret.params.add("ANTI_THEFT_ON_INPUT2",str(val))
      ret.params.add("UDP_TRANSMITION",str(val))
      ret.params.add("INTPUT5_AS_RPM_READER",str(val))
      ret.params.add("ADS_IN_RAW_MODE",str(val))
      self.append(ret)
   def MTCConfigParamEx(self):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCConfigParamEx",type="67",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("INPUT5_CONTROLS_BRIDGE",str(val))
      ret.params.add("ACTIVATE_GPRS_USING_INTERNAL_BATTERY",str(val))
      ret.params.add("CONFIG_SD_CARD",str(val))
      ret.params.add("TRANSMIT_SATELITAL_ON_GPRS_FAIL",str(val))
      ret.params.add("USING_TARIFF_SYSTEM",str(val))
      ret.params.add("SET_ODOMETER_ON_INPUT3",str(val))
      self.append(ret)
   def MTCRequestPosition(self):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCRequestPosition",type="68",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCAuxWriteAlert(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCAuxWriteAlert",type="69",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("ACTIVE_SERIAL_ALERT","1" if val else "0")
      self.append(ret)
   def MTCSleepMode2(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCSleepMode2",type="70",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("SLEEPMODE2",str(val))
      self.append(ret)
   def MTCSetDtmfPassword(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCSetDtmfPassword",type="73",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("PASSWORD",str(val))
      self.append(ret)
   def MTCSetPeripheralCode(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCSetPeripheralCode",type="74",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("CODE",str(val))
      self.append(ret)
   def MTCCheckWayPointFiles(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCCheckWayPointFiles",type="75",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCMakeBackup(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCMakeBackup",type="81",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCRestoreBackup(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCRestoreBackup",type="82",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCSetPinNumber(self,val): #4digits
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCSetPinNumber",type="83",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("PINNUMBER",str(val))
      self.append(ret)
   def MTCDisconnectInternalBatt(self,val): #4digits
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCDisconnectInternalBatt",type="86",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCSetInputMask(self,panic,i2,i3,i4,i5): #4digits
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCSetInputMask",type="87",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("PANIC",str(panic))
      ret.params.add("INPUT2",str(i2))
      ret.params.add("INPUT3",str(i3))
      ret.params.add("INPUT4",str(i4))
      ret.params.add("INPUT5",str(i5))            
      self.append(ret)
   def MTCInvertOutput(self,panic,i2,i3,i4):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCInvertOutput",type="88",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("OUTPUT1",str(panic))
      ret.params.add("OUTPUT2",str(i2))
      ret.params.add("OUTPUT3",str(i3))
      ret.params.add("OUTPUT4",str(i4))
      self.append(ret)
   def MTCSatSwitchTimer(self,val):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCSatSwitchTimer",type="89",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("INTERVAL",str(val))
      self.append(ret)
   def MTCSetOutputMask(self,i1,i2,i3,i4):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCSetOutputMask",type="90",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("OUTPUT1",str(i1))
      ret.params.add("OUTPUT2",str(i2))
      ret.params.add("OUTPUT3",str(i3))
      ret.params.add("OUTPUT4",str(i4))
      self.append(ret)
   def MTCPublishInterval(self,val): #MUST TYPE:04 VALUE:0 OR "", OTHERELSE ON IGNITION DEFAULT WAS SET BACK
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCPublishInterval",type="91",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("MTCRECORDINGINTERVALSECONDS2",str(val))
      self.append(ret)
   def MTCChangeApnUserPass(self,apn,user,passw): 
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCChangeApnUserPass",type="94",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("GPRSAPN",str(apn))
      ret.params.add("USERGPRS",str(user))
      ret.params.add("PASSWORDGPRS",str(passw))
      self.append(ret)
   def MTCSetHdopFilter(self,val): 
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCSetHdopFilter",type="95",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("HDOPFILTER",str(val))
      self.append(ret)
   def MTCSetRequestCredit(self,val): 
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCRequestCredit",type="96",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)
   def MTCGprsSetIps(self,prim,sec,port):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCGprsSetIps",type="97",attempts="3",timeout=self.timeoutstr)      
      ret.params.add("GPRSPRIMARYIP",str(prim))
      ret.params.add("GPRSSECONDARYIP",str(sec))
      ret.params.add("GPRSPORT",str(port))
      self.append(ret)
   def MTCTurnOffAlarm(self,prim,sec,port):
      ret = Cmd(protocol=self.protocol,serial=self.serial,idcmd="MTCTurnOffAlarm",type="98",attempts="3",timeout=self.timeoutstr)      
      self.append(ret)

      
def Send(protocol,serial,cmd):
    host = '192.168.1.114'   
    port = 5001   
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    s.connect((host,port))
    x = Cmds(protocol,serial,600)
    if cmd == 0:
      x.MTCSetOutput("1",True)
      x.MTCSetOutput("2",True)
      x.MTCSetOutput("3",True)
      x.MTCSetOutput("4",True)
      x.MTCSetOutput("5",True)
      x.MTCSetOutput("6",True)
      x.MTCSetOutput("7",True)
      x.MTCSetOutput("8",True)
      msg = x.mount()   
      totalsent = 0   
      while totalsent < len(msg):   
         sent = s.send(msg[totalsent:])   
         if sent == 0:
             raise RuntimeError("send error")
         totalsent = totalsent + sent
         
      chunk = s.recv(4096)


