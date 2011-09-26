from django.core.management.base import BaseCommand, CommandError
from itrack.command.models import CPRSession
import socket


class Command(BaseCommand):
    def handle(self, *args, **options):
    
    TCP_IP = '192.168.1.119'
    TCP_PORT = 5000    
    
    sess = CPRSession.objects.all()[0]
                    
    ack_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"98\" Reason=\"0\" Save=\"FALSE\"/><Data /></Package>"
    
    s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_out.connect((TCP_IP, TCP_PORT))
    
    seckey_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"2\" /><Data SessionId=\""+sess.key+"\" /></Package>"
    
    s_out.send(seckey_msg)
    data2 = s_out.recv(BUFFER_SIZE)
    
    print data2
    
    carmeter_msg = '''
<?xml version="1.0" encoding="ASCII"?>
    <Package>
    <Header Version="1.00" Id="41" />
    <Data
        Account="1"
        ProductId="42"
        Serial="00003A7B"
        Priority="3"
        NetId=”0A”
        Address=”AF”
        Format=”HEX”
        Value=”000114351201729400”
    />
    </Package>
'''
    # 0A 00 01 14 35 12 01 72 94 00 XX
    # 0A 00 00 06 01 0F 06 F1 28 73 2F

    
    s_out.send(blocker_msg)
    data2 = s_out.recv(BUFFER_SIZE)
    s_out.send(ack_msg)
