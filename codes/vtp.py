# VirusTotal Proxy v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com

from twisted.protocols import portforward
from twisted.internet import reactor
import getopt, sys
import re
import time
import urllib
import simplejson
from cookielib import CookieJar
import threading
from threading import *
import urlparse
import urllib, urllib2
import os
from datetime import datetime
if sys.platform == 'win32':
	import winsound
	
# Global Variables
lport = 0
dhost = ""
dport = 0
debug = False
screenLock = Semaphore(value=1)
debug = ""
domains = []
alarm_level = 1

# Initialization
reload(sys)
sys.setdefaultencoding('iso-8859-9')
opener = urllib2.build_opener(urllib2.HTTPHandler)
urllib2.install_opener(opener)

def cls():
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
        os.system("clear")
    elif sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("cls")

def ctime():
        if debug:
            print "--> ctime()"
        now = datetime.now()
        right_now = str(now.day) + "-" + str(now.month) + "-" + str(now.year) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
        if debug:
            print "right_now", right_now
            print "<-- ctime()"
        return right_now

def check_url(domain):
	url = "https://www.virustotal.com/en/url/submission/"
	token = ""
	positive = 0
	total = 0
	anurl = ""
	
	time.sleep(15) # We dont want to flood remote server.
		
	post_data_dictionary = {"url" : domain}
	http_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0", "X-CSRFToken":"null", "Referer":"https://www.virustotal.com/en/"}		
	post_data_encoded = urllib.urlencode(post_data_dictionary)
	request_object = urllib2.Request(url, post_data_encoded, http_headers)		
		
	if debug:
		screenLock.acquire()
		print url, domain
		screenLock.release()
		
	f = opener.open(request_object)
	response = f.read()
	
	if debug:
		screenLock.acquire()
		print response
		screenLock.release()

	re1='("positives")'	# Double Quote String 1
	re2='(:)'	# Any Single Character 1
	re3='(.*?)'	# Non-greedy match on filler
	re4='(,)'	# Any Single Character 2

	rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
	m = rg.search(response)
	if m:
		string1=m.group(1)
		c1=m.group(2)
		c2=m.group(3)
		c3=m.group(4)		
		positive = c2
		if debug:
			screenLock.acquire()
			print "Positive: " + positive + "\n"
			screenLock.release()

		re1='("last_analysis_date")'	# Double Quote String 1
		re2='(: ")'	# Any Single Character 1
		re3='(.*?)'	# Non-greedy match on filler
		re4='(",)'	# Any Single Character 2

		rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
		m = rg.search(response)
		if m:
			string1=m.group(1)
			c1=m.group(2)
			c2=m.group(3)
			c3=m.group(4)		
			ladate = c2
			if debug:
				screenLock.acquire()
				print "Last Analysis Date: " + ladate + "\n"
				screenLock.release()
			a = datetime.strptime(ladate.split(" ")[0], "%Y-%m-%d")
			b = "{:%Y-%m-%d}".format(datetime.now())
			b = datetime.strptime(b, "%Y-%m-%d")
			
			re1='("total")'	# Double Quote String 1
			re2='(:)'	# Any Single Character 1
			re3='(.*?)'	# Non-greedy match on filler
			re4='(,)'	# Any Single Character 2

			rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
			m = rg.search(response)
			if m:
				string1=m.group(1)
				c1=m.group(2)
				c2=m.group(3)
				c3=m.group(4)		
				total = c2
				if debug:
					screenLock.acquire()
					print "Total: " + total + "\n"
					screenLock.release()			
					
				re1='("reanalyse_url")'	# Double Quote String 1
				re2='(:)'	# Any Single Character 1
				re3='(.*?)'	# Non-greedy match on filler
				re4='(})'	# Any Single Character 2

				rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
				m = rg.search(response)
				if m:
					string1=m.group(1)
					c1=m.group(2)
					c2=m.group(3)
					c3=m.group(4)		
					anurl = c2
					if a < b:
						opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0')]
						aurl = urlparse.urlparse(url).netloc + anurl.replace("\"", "")
						aurl = aurl.replace(" ", "")
						aurl = "https://" + aurl
						f = opener.open(aurl)
						if debug:
							screenLock.acquire()
							print "Submitting outdated URL:", aurl
							screenLock.release()
						return 1
						
					if debug:
						screenLock.acquire()
						print "Report URL: " + anurl + "\n"
						print "----------------------"
						screenLock.release()
					
					if anurl:
						url = urlparse.urlparse(url).netloc + anurl.replace("\"", "")
						url = url.replace(" ", "")
						url = "https://" + url
						
						if debug:
							screenLock.acquire()
							print url
							screenLock.release()

						opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0')]
						f = opener.open(url)
						response = f.read()

						if debug:
							screenLock.acquire()		
							print response
							screenLock.release()			
						
					ltime = ctime()
						
					if m:
						screenLock.acquire()
						print "Date:", ltime, "Domain:", domain, "Detection Ratio:", positive + " / " + total, "Report URL:", url + "\n"	
						screenLock.release()		
						line = ltime + "|" + domain.strip()+"|"+ positive + " / " + total + "|" + url + "\n"		
						if sys.platform == 'win32':
							if int(positive) >= int(alarm_level):
								winsound.Beep(700,1500)
					
						filename = "vtp.txt"
						FILE = open(filename,"a+")
						FILE.writelines(line)
						FILE.close()

					if debug:
						line = response + "\n"
						filename = "vtp_debug.txt"
						FILE = open(filename,"a+")
						FILE.writelines(line)
						FILE.close()
					
					return 0
	return 1
		
def connect_vt(self, data):
	re1='(CONNECT)'	# Word 1
	re2='.*?'	# Non-greedy match on filler
	re3='((?:[a-z][a-z\\.\\d\\-]+)\\.(?:[a-z][a-z\\-]+))(?![\\w\\.])'	# Fully Qualified Domain Name 1
	re4='.*?'	# Non-greedy match on filler
	re5='(\\d+)'	# Integer Number 1
	re6='.*?'	# Non-greedy match on filler
	re7='(HTTP)'	# Word 2
	domain=""
	rg = re.compile(re1+re2+re3+re4+re5+re6+re7,re.IGNORECASE|re.DOTALL)
	m = rg.search(data)
	if m:
		fqdn1=m.group(2)
		int1=m.group(3)		
		if int1 == "443":
			domain = "https://" + fqdn1
			screenLock.acquire()
			print "Connecting to:", domain
			screenLock.release()
		else:
			domain = "http://" + fqdn1
			screenLock.acquire()
			print "Connecting to:", domain
			screenLock.release()
	else:
		re1='(GET|POST ) '	# Word 1
		re2='((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))'	# HTTP URL 1
		re3='( HTTP/)'	# Word 2

		rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
		m = rg.search(data)
		if m:
			httpurl1=m.group(2)
			domain = "http://" + urlparse.urlparse(httpurl1).netloc
			screenLock.acquire()
			print "Connecting to:", domain
			screenLock.release()

	for entry in domains:
		if entry.find(domain) < 0:
			if len(domains) >= 50:
				domains.pop(0)
				domains.append(domain)
				screenLock.acquire()
				print domain
				screenLock.release()
		else:
			return
	
	domains.append(domain)
	
	i = 1
	while (i != 0):
		i = check_url(domain)
	
def log_data(self, data):
	server_file = "log.txt" 
	FILE = open(server_file, "a")
	FILE.write(data)
	FILE.close()

def server_dataReceived(self, data):
	global debug
	
	t = Thread(target=connect_vt, args=(self,data))
	t.start()
	
	if debug:
		log_data(self, data)
		screenLock.acquire()
		print "Client ------> server"
		print "%r" % data
		screenLock.release()
		
	portforward.Proxy.dataReceived(self, data)

portforward.ProxyServer.dataReceived = server_dataReceived
	
def vtproxy():
	reactor.listenTCP(lport, portforward.ProxyFactory(dhost, dport))
	reactor.run()

def banner():
	print "============================================"
	print u"VirusTotal Proxy [http://www.mertsarica.com]"
	print "============================================"	
	print "Usage: python vtp.py -l <bind port> -r <proxy ip> -p <proxy port> -a <alarm level>\n"	
		
def main():
	global debug
	global lport
	global dhost
	global dport
	global alarm_level
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "vl:r:p:a:")
	except getopt.GetoptError:
		banner()
		sys.exit(1)

	try:
		for o, a in opts:
			if o == "-l":
				lport = int(a)
			if o == "-r":
				dhost = a
			if o == "-p":
				dport = int(a)
			if o == "-v":
				debug = True
			if o == "-a":
				alarm_level = int(a)
				
	except:
		banner()
		sys.exit(1)
		
	if lport == 0 or dhost == "" or dport == 0:
		cls()
		banner()
		sys.exit(1)
	else:
		cls()
		print "============================================"
		print u"VirusTotal Proxy [http://www.mertsarica.com]"
		print "============================================"		
		print "[+] Listening on port", lport	
		vtproxy()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print "[+] Bye..."
		sys.exit(1)