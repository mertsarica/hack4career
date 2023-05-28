# IP2Geo Tool v2.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.hack4career.com

import os
import sys
import ipinfo

# Type your IPinfo access token below
access_token = ""
debug = 0

def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")

def do_whois():
	try:
		filename = "ip.txt"
		FILE  = open (filename,"r" )
		ips = FILE.readlines()
		FILE.close()
		filename = "location.txt"
		FILE  = open (filename,"w" )
		FILE.close()
	except IOError:
		print ("[+] ip.txt file not found! \n[+] Please put IP addresses into ip.txt and re-run the program\n")
		sys.exit(1)

	for ip in ips:
		handler = ipinfo.getHandler(access_token)
		try:
			details = handler.getDetails(ip.strip())
			print(ip.strip(), details.country, details.city)
			line = ip.strip()+":"+details.country+":"+details.city + "\n"
			filename = "location.txt"
			FILE = open(filename,"a+")
			FILE.writelines(line)
			FILE.close()
		except:
			continue

if __name__ == '__main__':
	cls()
	print ("===========================================")
	print (u"IP2Geo Tool v2 [https://www.hack4career.com]")
	print ("===========================================")
	if len(sys.argv) < 1:
		print ("Usage: python ip2geo_v2.py\n")
		sys.exit(1)

	try:
		do_whois()
	except KeyboardInterrupt:
		print ("[+] Bye...")
