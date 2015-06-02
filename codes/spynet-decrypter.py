# Spy-Net v2.6 Config Decrypter v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
import os, re, sys
import binascii


def xor(data):
        data = binascii.unhexlify(data)
        decryptedData = ""
        for i in data:
                decryptedData = decryptedData + (chr(ord(i) ^ 0xbc))
        return decryptedData

if __name__ == '__main__':
        if sys.platform == 'linux-i386' or sys.platform == 'linux2':
                os.system("clear")
        elif sys.platform == 'win32':
                os.system("cls")
        else:
                os.system("cls")
        
	print "========================================================="
	print u"Spy-Net v2.6 Config Decrypter [http://www.mertsarica.com]"
	print "========================================================="
	if len(sys.argv) < 2:
		print "Usage: python spynet-decrypter.py [unpacked server.exe]\n"
		sys.exit(1)

	try:
                cfile = sys.argv[1]

                m = open(cfile, "rb")
                data = m.read()
                m.close()
                data = binascii.hexlify(data)

                regex = "(556e6974496e6a6563744c696272617279000000)(.*?)(232323234023232323)"
                person = re.findall(regex, data)
                print "[*] Spy-Net Server:", xor(person[0][1])

                # print "Parameters:"
                data  = data.split("232323234023232323")
                m = 0
                for i in data:
                        if len(i) >= 1024:
                                continue
                        else:
                                if len(i) == 2:
                                        continue
                                m = m + 1
                                if m == 1:
                                        print "[*] Identification:", xor(i)
                                elif m == 2:
                                        print "[*] Password:", xor(i)
                                        print "[*] Parameters:"
                                else:
                                        print xor(i)
        except KeyboardInterrupt:	
            print "[+] Bye..."
