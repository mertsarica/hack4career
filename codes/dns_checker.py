# -*- coding: utf-8 -*-
# DNS Checker
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
          
import socket
import time
import datetime
import sys
import os
import winsound
import subprocess

debug = 0
waittime = 60*60

def dns_lookup(address):
    subprocess.call("ipconfig /flushdns", stdout=False, stderr=False)
    query = socket.getaddrinfo(address, 80)
    query = ".".join([str(x) for x in query])
    query = query.split("'")[3]
    print address, "-", query
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    if os.path.isfile("history.txt"):
        FILE  = open ("history.txt","r" )   
        entries = FILE.readlines()
        FILE.close()
        lastentry = entries[-1].split("|")[1]

        if debug:
            print query.strip, lastentry
            print address.strip().lower(), entries[-1].split("|")[0].strip().lower()

        if (address.strip().lower() == entries[-1].split("|")[0].strip().lower()):
            if query.strip() != lastentry.strip():
                print "DNS Change Detected! (Old: %s - New: %s)\n" %(lastentry.strip(), query)
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                    
        line = address + "|" + query + "|" + date + "\n"
        FILE = open("history.txt", "a")
        FILE.writelines(line)
        FILE.close()
    else:
        line = address + "|" + query + "|" + date + "\n"
        FILE = open("history.txt", "w")
        FILE.writelines(line)
        FILE.close()

if __name__ == '__main__':
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
            os.system("clear")
    elif sys.platform == 'win32':
            os.system("cls")
    else:
            os.system("cls")
    print "======================================="
    print u"DNS Checker [http://www.mertsarica.com]"
    print "======================================="

    if debug:
        print len(sys.argv)
        
    if len(sys.argv) < 2:
        print "Usage: python dns_checker.py <domain name> [check interval]"
        print "\nRequired arguments:"
        print "<domain name>"
        print "\nOptional arguments:"
        print "[check interval (in minutes)]    Ex: 5 (make dns resolution in every 5 minutes)"
        sys.exit(1)

    if len(sys.argv) > 2:
        waittime = int(sys.argv[2])*60

    try:
        while(1):
            dns_lookup(sys.argv[1])
            time.sleep(waittime)
    except KeyboardInterrupt:	
        print "Bye..."
