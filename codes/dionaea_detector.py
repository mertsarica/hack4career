# Dionaea Detector v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.mertsarica.com
from os import getenv
import pymssql
import os
import sys
import subprocess

# Enable TDSDUMP
os.environ['TDSDUMP'] = 'tdsdump.txt'

# Global Variables
user = "Hack4Career\\MertSARICA"
password = "Hack4Career"

def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")
		
def banner():
	cls()

	print "=================================================="
	print u"Dionaea Detector v1.0 [https://www.mertsarica.com]"
	print "=================================================="

def usage():
       print "Usage: python dionaea_detector.py <ip address>\n"

if __name__ == '__main__':
	cls()
	banner()
        
	if len(sys.argv) < 2:
		usage()
		sys.exit(1)
	else:
		try:
			pymssql.connect(sys.argv[1], user, password, login_timeout=1)
		except:
			try:
				filename = "tdsdump.txt"
				FILE  = open (filename,"r" )   
				logs = FILE.readlines()
				FILE.close()	
			except IOError:
				print "[+] tdsdump.txt file not found, terminating! \n"
				sys.exit(1)
			if "".join(logs).find("LOGINACK") >= 0:
				print "[*] Dionaea has been detected on", sys.argv[1]
			else:
				print "[*] Sorry, I have no idea", sys.argv[1]