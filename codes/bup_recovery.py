# Mcafee Virusscan Antivirus Quarantined File (BUP) Restore Utility v1.1
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
from itertools import izip, cycle
import os, re, sys
import time

# Global Variables
key = "j"
payload = ""
fname = ""
view = 0
restore = 0

def restore_it(key):
        global fname
        encryptedData = ""
        data = ""

        i = 0
        b = 61440+512
        p = 1
        m = 0
        t = 1

        if len(payload) > 61952:
                while b < len(payload):
                        if i == 0:
                                data = payload[0:61440]
                        if i % 512 == 0:
                                if i == 512:
                                        m = 1
                                else:
                                        m = m + 1
                                if p == 5 or t % 8 == 0:
                                        t = 0
                                        data = data + payload[b+(i/m):b+(i/m)+61440]
                                        b = b+(i/m)+61440
                                else:
                                        data = data + payload[b+(i/m):b+(i/m)+65536]
                                        b = b+(i/m)+65536
                        i = i + 512
                        p = p + 1
                        t = t + 1
        else:
                data = payload


        for (x, y) in izip(data, cycle(key)):
                encryptedData = encryptedData + ''.join(chr(ord(x) ^ ord(y)))

        if encryptedData.find("WasAdded=") >= 0 and encryptedData.find(key*55) >= 0:
                print "Original" + encryptedData[encryptedData.find("Name="):encryptedData.find("WasAdded=")-2]
                fname = encryptedData[encryptedData.find("Name="):encryptedData.find("WasAdded=")]
                fname = fname.rsplit("\\", 1)[1]
                encryptedData = encryptedData[0:encryptedData.find(key*55)]
        elif encryptedData.find(key*55) >= 0:
                encryptedData = encryptedData[0:encryptedData.find(key*55)]

        if encryptedData.find("ile_1]") >= 0:
                encryptedData = encryptedData[0:encryptedData.find("ile_1]")]
        elif encryptedData.find("[File") >= 0:
                encryptedData = encryptedData[0:encryptedData.find("[File")]
        elif encryptedData.find("[Fil") >= 0:
                encryptedData = encryptedData[0:encryptedData.find("[Fil")]
        elif encryptedData.find("le_]") >= 0:
                encryptedData = encryptedData[0:encryptedData.find("le_]")]
        
        if restore:
                e = open(fname.rstrip(), "wb")     
                e.write(encryptedData)
                e.close()

                print "[*] Restored successfully ->", fname.rstrip()

if __name__ == '__main__':
        if sys.platform == 'linux-i386' or sys.platform == 'linux2':
                os.system("clear")
        elif sys.platform == 'win32':
                os.system("cls")
        else:
                os.system("cls")
        
	print "====================================================================="
	print u"Mcafee Virusscan BUP File Restore Utility [http://www.mertsarica.com]"
	print "====================================================================="
	if len(sys.argv) < 3:
		print "Usage: python bup_recovery.py [view/restore] [quarantined file]\n"
		sys.exit(1)

	try:
                if (sys.argv[1].lower() == "restore"):
                        restore = 1
                elif (sys.argv[1].lower() == "view"):
                        view = 1
                else:
                        print "Usage: python bup_recovery.py [view/restore] [quarantined file]\n"
                        sys.exit(1)  

                cfile = sys.argv[2]

                try:
                        m = open(cfile, "rb")
                except IOError:
                        print "[+] BUP file not found\n"
                        sys.exit(1)
                        
                m.seek(2048, os.SEEK_SET)
                payload = m.read(512)
                encryptedData = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(payload, cycle(key)))
                m.close()
                
                if encryptedData.find("OriginalName") >= 0:             
                        m = open(cfile, "rb")
                        m.seek(2048+512, os.SEEK_SET)
                        payload = m.read()
                        print encryptedData[0:encryptedData.find("WasAdd")]
                        fname = encryptedData[encryptedData.find("OriginalName"):encryptedData.find("WasAdd")]
                        fname = fname.rsplit("\\", 1)[1]
                        m.close()
                        if view:
                                sys.exit(1)
                                
                else:
                        m = open(cfile, "rb")
                        m.seek(2048+384, os.SEEK_SET)
                        payload = m.read()
                        print encryptedData[0:encryptedData.find("ObjectType=")]
                        m.close()

                restore_it(key)
        except KeyboardInterrupt:	
            print "[+] Bye..."
