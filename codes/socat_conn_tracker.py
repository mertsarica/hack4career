# -*- coding: cp1254 -*-
# SOCAT Connection Tracker v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
# This tool is provided for educational purposes only, use at your own risk

import re
import os
import sys
import time
import datetime

debug = 0

def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")

def track(fname):
	filename =  fname
	
	with open(filename, 'r+') as f:
		ipaddress = ""
		conntime = ""
		for line in f:
			re1='((?:2|1)\\d{3}(?:-|\\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))(?:T|\\s)(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9]))'	# Time Stamp 1
			re2='.*?'	# Non-greedy match on filler
			re3='(accepting connection from)'	# Word 1
			re4='.*?'	# Non-greedy match on filler
			re5='((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])'	# IPv4 IP Address 1

			rg = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)
			m = rg.search(line)
			if m:
				if debug:
					print "Line:", line
				timestamp1=m.group(1)
				word1=m.group(2)
				ipaddress1=m.group(3)
				ipaddress = ipaddress1
				# print "Connection from:", ipaddress1# + "\n"
				# print "Connection Time:", timestamp1
				conntime = timestamp1
				ctime = datetime.datetime.strptime(timestamp1, "%Y/%m/%d %H:%M:%S")
				
			txt = f.next()
			re1='.*?'	# Non-greedy match on filler
			re2='(forked off child process)'	# Word 1
			re3='.*?'	# Non-greedy match on filler
			re4='(\\d+)'	# Any Single Digit 1

			rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
			m = rg.search(txt)
			
			if m:
				if debug:
					print "Txt:", txt
				word1=m.group(1)
				d1=m.group(2)
				if debug:
					print "Connection ID:", d1
				
				m = f
				for nline in m:
					re0='((?:2|1)\\d{3}(?:-|\\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))(?:T|\\s)(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9]))'
					re1='.*?'	# Non-greedy match on filler
					re2='(socat)'	# Word 1
					re3='(\\[)'	# Square Braces 1
					re4= d1	# Non-greedy match on filler
					re5='(\\] N exiting with status 0)'	# Word 2

					rg = re.compile(re0+re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)
					m = rg.search(nline)
					if m:
						word1=m.group(1)
						sbraces1=m.group(2)
						word2=m.group(3)
						# print "Connection from:", ipaddress# + "\n"
						# print "Disconnection Time:", word1
						# print "Connection Time:", timestamp1
						dtime = datetime.datetime.strptime(word1, "%Y/%m/%d %H:%M:%S")
						diff = dtime - ctime
						if diff.seconds >= 120:
							print "Connection from:", ipaddress
							print "Connection Time:", conntime
							print "Disconnection Time:", word1
							print "Connection duration:", diff.seconds/60, "minutes\n"
						# else:
						# 	print "Connection duration:", diff.seconds, "seconds\n"
						break

					re0='((?:2|1)\\d{3}(?:-|\\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))(?:T|\\s)(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9]))'
					re1='.*?'	# Non-greedy match on filler
					re2='(socat)'	# Word 1
					re3='(\\[)'	# Square Braces 1
					re4= d1	# Non-greedy match on filler
					re5='(\\] N exit\\(1\\))'	# Word 2

					rg = re.compile(re0+re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)
					m = rg.search(nline)
					if m:
						word1=m.group(1)
						sbraces1=m.group(2)
						word2=m.group(3)
						# print "Disconnection Time:", word1
						dtime = datetime.datetime.strptime(word1, "%Y/%m/%d %H:%M:%S")
						diff = dtime - ctime
						if diff.seconds >= 120:
							print "Connection from:", ipaddress
							print "Connection Time:", conntime
							print "Disconnection Time:", word1
							print "Connection duration:", diff.seconds/60, "minutes\n"
						# else:
						#	print "Connection duration:", diff.seconds, "seconds\n"
						break
						
			
if __name__ == '__main__': 	
	cls()
	print "====================================================="
	print u"SOCAT Connection Tracker [https://www.mertsarica.com]"
	print "====================================================="
	if len(sys.argv) < 2:
		print "Usage: python socat_conn_tracker.py <log file>\n"
		sys.exit(1)
	
	try:
		track(sys.argv[1])
	except KeyboardInterrupt:	
		print "[+] Bye..."                                

