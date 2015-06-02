# IP2Geo Tool v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com

import urllib, urllib2
import re
import os
import sys

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
                filename = "location.txt"
		FILE  = open (filename,"w" )   
		FILE.close()		
	except IOError:
		print "[+] ip.txt file not found! \n[+] Please put IP addresses into ip.txt and re-run the program\n"
		sys.exit(1)
	
	for ip in ips:
                # print ip
		url = "http://www.ipgeo.com/tools/cmd/country.php"
                parameters = {'ip' : str(ip), 'Submit' : 'Lookup'}                                                                        
                headers =  {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2'} 
                data = urllib.urlencode(parameters)
                req = urllib2.Request(url, data, headers)
                req.add_header('Referer', 'http://www.ipgeo.com/tools/country.php')
                response = urllib2.urlopen(req)
		html = response.read()
		# print html

                re1='(Country: )'	# Word 1
                re2='(<b>)'	# Non-greedy match on filler
                re3='(.*)'	# Word 2
                re4='(<\\/b>)'	# Tag 2

                rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
                m = rg.search(html)
                if m:
                    word2=m.group(3)
                    if len(ip) < 12:
                            print "IP: "+ip.strip()+"\t\tLocation: "+word2.strip()
                    else:
                            print "IP: "+ip.strip()+"\tLocation: "+word2.strip()
                            
                    line = ip.strip()+":"+word2.strip() + "\n"
                    filename = "location.txt"
                    FILE = open(filename,"a+")
		    FILE.writelines(line)
		    FILE.close()
			
if __name__ == '__main__': 	
	print "======================================="
	print u"IP2Geo Tool [http://www.mertsarica.com]"
	print "======================================="
	if len(sys.argv) < 1:
		print "Usage: python ip2geo.py\n"
		sys.exit(1)
	
	try:
            do_whois()
        except KeyboardInterrupt:	
            print "[+] Bye..."                                
