# -*- coding: cp1254 -*-
# Whois Description Tool v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
# This tool is provided for educational purposes only, use at your own risk

import urllib, urllib2
import re
import os
import sys
import time

proxy_info = {
'user' : '', # proxy username
'pass' : '', # proxy password
'host' : "", # proxy host (leave it empty if no proxy is in use)
'port' : 8080 # proxy port
}
        
# build a new opener that uses a proxy requiring authorization
proxy_support = urllib2.ProxyHandler({"http" : \
"http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxy_info})
		
if proxy_info['host'] != "":
	opener = urllib2.build_opener(proxy_support, urllib2.HTTPCookieProcessor())
else:
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	
# install it
urllib2.install_opener(opener)

os.system("cls")

def do_whois():
	try:
                filename = "ip.txt"
		FILE  = open (filename,"r" )   
		ips = FILE.readlines()
		FILE.close()
                # filename = "desc.txt"
		# FILE  = open (filename,"w" )   
		# FILE.close()		
	except IOError:
		print "[+] ip.txt file not found! \n[+] Please put IP addresses into ip.txt and re-run the program\n"
		sys.exit(1)
	
	for ip in ips:
                time.sleep(2) # We dont want to flood remote server.
		url = "http://www.whois.com.tr/?q="+ip.strip()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                f = opener.open(url)
		response = f.read()
		if response.find("rkiye") < 0:
                    continue
                    
                url = "http://www.whois.com.tr/?q="+ip.strip()+"&type=jx"

		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                f = opener.open(url)
		response = f.read()

                re1='(descr:)'	# Word 1
                re2='(.*?)'	# Word 2
                re3='(\\\\n)'	# Tag 2

                rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
                m = rg.search(response)
                if m:
                    word2=m.group(2)

                    print "IP: "+ip.strip()+" Desc: "+word2.lstrip()
                            
                    # line = ip.strip()+":"+word2.lstrip() + "\n"
                    # filename = "desc.txt"
                    # FILE = open(filename,"a+")
                    # FILE.writelines(line)
                    # FILE.close()
		    continue

                re1='(OrgName:)'# Word 1
                re2='(.*?)'	# Word 2
                re3='(\\\\n)'	# Tag 2		
                rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
                m = rg.search(response)
                if m:
                    word2=m.group(2)

                    print "IP: "+ip.strip()+" Desc: "+word2.lstrip()
        
                    # line = ip.strip()+":"+word2.lstrip() + "\n"
                    # filename = "desc.txt"
                    # FILE = open(filename,"a+")
                    # FILE.writelines(line)
                    # FILE.close()
			
if __name__ == '__main__': 	
	print "==========================================="
	print u"Whois Desc Tool [http://www.mertsarica.com]"
	print "==========================================="
	if len(sys.argv) < 1:
		print "Usage: python whois_desc.py\n"
		sys.exit(1)
	
	try:
            do_whois()
        except KeyboardInterrupt:	
            print "[+] Bye..."                                
