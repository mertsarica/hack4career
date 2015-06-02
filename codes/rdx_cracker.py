# ReDiX Crypter Cracker Tool v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
from itertools import izip, cycle
import os, re, sys

key = ""
keyparam = ""
payload = ""

def xor(key):
	ofile = "cracked_payload.exe"
 
	e = open(ofile, "w")

 	encryptedData = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(payload, cycle(key)))
	e.write(encryptedData) 
	e.close()
        print "[+] XORed payload cracked: cracked_payload.exe"

if __name__ == '__main__':
        if sys.platform == 'linux-i386' or sys.platform == 'linux2':
                os.system("clear")
        elif sys.platform == 'win32':
                os.system("cls")
        else:
                os.system("cls")
        
	print "================================================="
	print u"ReDiX Crypter Cracker [http://www.mertsarica.com]"
	print "================================================="
	if len(sys.argv) < 2:
		print "Usage: python rdx_cracker.py [encrypted file]\n"
		sys.exit(1)

	try:
                cfile = sys.argv[1]

                m = open(cfile, "r")
                m.seek(-128, os.SEEK_END)
                data = m.read()
                m.close()

                re1='(_<>_)'	# Tag 1
                re2='([0-9a-zA-Z\]\[_`\'^\\\\]+)'	# XOR Key
                re3='(_<>_)'	# Tag 2

                rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
                m = rg.search(data)
                if m:
                        word3=m.group(2)
                        key = word3
                        print "[+] XOR key detected: " + key

                        keyparam = "_<>_" + key + "_<>_"
                        
                        m = open(cfile, "rb")
                        data = m.read()

                        begin = data.find("_<>_") - len(data)

                        end = data.find(keyparam) - data.find("_<>_") - 4
                        
                        m.seek(4+begin, os.SEEK_CUR)
                        payload = m.read(end)

                        m.close()
                        
                        xor(key)
        except KeyboardInterrupt:	
            print "[+] Bye..."
