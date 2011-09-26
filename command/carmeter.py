


class CprCarMeterRequest(object):
    def __init__(self):
        self.code = 0
        self.equiptype = 0x00
        self.size = 0
        self.position = 1
        self.accesstable = 0
        self.card = [0,0,0,0,0,0]
        self.chk = 0
        pass
    def Register(self,pos,table,card): # card list 6 bytes, pos 1 byte, table 1byte, card 4 bytes
        self.code = 0x0A
        self.size = [0x00,0x06]
        self.position = pos
        self.accesstable = table
        self.card = card
        self.chk = 
        pass
    def Unregister(self):
        self.code = 0x0B
        
        pass
    def Check(self):
        self.code = 0x0C
        
        pass
    def KeepAlive(self):
        self.code = 0x01
        
        pass
    def Program(self):
        self.code = 0x02
        
        pass
    def Read(self):
        self.code = 0x03
            
        pass
    def SignalOutput(self):
        self.code = 0x04
        
        pass
    def Boot(self):
        self.code = 0x05
        
        pass
class CprCarMeterResponse(object):
    def __init__(self):
        pass

