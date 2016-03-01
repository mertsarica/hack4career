# Allatori ZIP Shortener v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com

import zipfile
import sys
import os 
# Define the length of junk char (AAAAAAA...) 
nm = "A"*7280

def shorten(sname, dname):
        try:
                source = zipfile.ZipFile(sname, 'r')
        except:
                print "[*] Can not file the source JAR file"
                sys.exit(1)
        target = zipfile.ZipFile(dname, 'w', zipfile.ZIP_DEFLATED)
        for file in source.filelist:
                target.writestr(file.filename.replace(nm,"A"), source.read(file.filename))
        target.close()
        source.close()
	print "[*] Shortened", sname, "to", dname

def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")

def banner():
        cls()

        print "======================================================="
        print u"Allatori ZIP Shortener v1.0 [http://www.mertsarica.com]"
        print "======================================================="

def usage():
       print "Usage: python allatori_zip_shortener.py <source JAR file> <destination JAR file>\n"

if __name__ == '__main__':
        cls()
	banner()
        
	if len(sys.argv) < 3:
		usage()
		sys.exit(1)
	else:
		shorten(sys.argv[1], sys.argv[2])


