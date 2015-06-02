# -*- coding: utf-8 -*-
# VirusTotal Reporter v1.0
# Description: It parses antivirus results from the output of VirusTotal Mass Uploader tool.
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com

import os
import time
import locale
import httplib, mimetypes
import urllib
import urllib2
import simplejson
import sys
import hashlib
import datetime
import re

debug = 0
# Define your VirusTotal API key!
vt_api_key = ""

reportfile = "vt_report.txt"
logfile = "vt_av_report.txt"

def blank_report(fname, txt):
	if fname.find(".txt") < 0:
		fname = fname + ".txt"
	file = open(fname, "w")
	txt = str("")
	file.write(txt)
	file.close()
	
def report(fname, txt):
	if fname.find(".txt") < 0:
		fname = fname + ".txt"
	now = datetime.datetime.now()
	time = now.strftime("%d-%m-%Y %H:%M")
	file = open(fname, "a")
	txt = str(txt.encode("cp1254") + "\n")
	file.write(txt)
	file.close()
	
def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")
	
def banner():
	cls()
	print "===================================================="
	print u"VirusTotal Reporter v1.0 [http://www.mertsarica.com]"
	print "===================================================="	

def usage():
	print "Usage: You should copy all malicious files to malwares folder and then run this program. It will submit or resubmit all files to VirusTotal]\n"

def vs_result(fname, txt):
	blank_report(fname, "")
	regex = re.compile(r'("scans": {")(.*?)(": {"detected": )(true|false)(,)', re.MULTILINE|re.IGNORECASE|re.DOTALL)

	if (regex):
		matches = [m.groups() for m in regex.finditer(txt)]

		for m in matches:
			av = m[1] + "=" + m[3]
			if debug:
				print "Antivirus result:", av
			report(fname, av)
			
	regex = re.compile(r'([0-9]"}, ")(.*?)(": {"detected": )(true|false)(,)', re.MULTILINE|re.IGNORECASE|re.DOTALL)

	if (regex):
		matches = [m.groups() for m in regex.finditer(txt)]

		for m in matches:
			av = m[1] + "=" + m[3]
			if debug:
				print "Antivirus result:", av
			report(fname, av)
	
def vt_check_report(fname, sha256):
	url = "https://www.virustotal.com/vtapi/v2/file/report"
	parameters = {"resource": sha256, "apikey": vt_api_key}
	data = urllib.urlencode(parameters)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	json = response.read()
	print "[*] Downloading VirusTotal report for", fname 
	if debug:
		print "Response:", json
	vs_result(fname, json)
	if fname.find(".txt") < 0:
		print "[*] Created VirusTotal report:", fname + ".txt"
	else:
		print "[*] Created VirusTotal report:", fname 
	
def open_report_file():
	try:
		FILE  = open (reportfile,"r" )   
		entries = FILE.readlines()
		FILE.close()
	except IOError:
		print "[+] Can not find report file:", reportfile
		sys.exit(1)
	return entries
		
def main():
	entries = open_report_file()
	for entry in entries:
		vt_check_report(entry.split("|")[1], entry.split("|")[3])
		time.sleep(15)
		
if __name__ == "__main__":
	banner()
	if vt_api_key is "":
		print "You should edit this file and define your VirusTotal API key!"
		sys.exit(1)
	main()
	
	