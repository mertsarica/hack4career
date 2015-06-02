# -*- coding: cp1254 -*-
# Twitter Crawler v1.0 - Crawls and stores all tweets of target twitter account
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
# This tool is provided for educational purposes only, use at your own risk

import urllib, urllib2
import re
import os
import sys
import time
from cookielib import CookieJar

cj = CookieJar()

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
	opener = urllib2.build_opener(proxy_support, urllib2.HTTPCookieProcessor(cj))
else:
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	
# install it
urllib2.install_opener(opener)

os.system("cls")

def crawl_tweets(username):
        filename = "tweets.txt"
        line = ""
        tweets = 0
        
        if os.path.exists(filename):
            cmd = "del " + filename
            os.system(cmd)

        i = 1
        m = 0
        print "[+] Running...\n"
                
        FILE = open(filename,"a+")
        FILE.writelines("Tweet|Time\n")
        FILE.close()
        
	while i > 0:
                url = "https://twitter.com/" + username.strip() + "?page=" + str(i) + "&twttr=true"
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                f = opener.open(url)            
		response = f.read().decode("utf-8")

		if response.find("This person has protected their tweets ") >= 0:
                        print "This person has protected their tweets. :("
                        sys.exit(1)
        
                print "[+] Crawled " + str(i) + ". page"
                retup = re.findall('(<span class="entry-content">)(.+)(</span>)', response)
                if len(retup) > 0:
                    retup2 = re.findall('(time:\')(.+)(\'}">)', response)
                    for element in retup:
                        line = element[1] + " | " + str(retup2[m][1]) + "\n"
                        unikod = unicode(line)
                        unibayt = unicode.encode(unikod, "utf-8")
                        FILE = open(filename, "a+") 
                        FILE.write(unibayt)
                        FILE.close()
                        m = m + 1
                    m = 0
                    tweets = tweets + len(retup)
                else:
                    break
                
                i = i + 1
	print "\n[+] %d tweets crawled and stored in tweets.txt successfully :)" % tweets
	    
if __name__ == '__main__': 	
	print "==========================================="
	print u"Twitter Crawler [http://www.mertsarica.com]"
	print "==========================================="
	if len(sys.argv) < 2:
		print "Usage: python twitter_crawler.py [twitter account]\n"
		sys.exit(1)
	
	try:
            crawl_tweets(sys.argv[1])
        except KeyboardInterrupt:	
            print "[+] Bye..."                                
