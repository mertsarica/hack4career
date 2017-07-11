# JavaScript Crawler v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com

import mechanize
import re
import os
import time
import sys
import pprint
import datetime
from urlparse import urlparse
from pymongo import MongoClient
import ssl
import socket
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

debug = 0
socket.setdefaulttimeout(3)

# How many days to sleep until recrawling
sleepday = "10"

# Would you like to detect internal js files ?
intjs = 0

logfile = "js.txt"

client = MongoClient()
db = client['javascript']
# collection = db['malsites']

def log(txt):             
    try:
            now = datetime.datetime.now()
            time = now.strftime("%d-%m-%Y %H:%M:%S")                
            file = open(logfile, "a")
            txt = str(time + "|" + txt.encode("cp1254") + "\n")
            # txt = str(txt.encode("cp1254") + "\n")
            file.write(txt)
            file.close()
    except Exception, e:
	    if debug:
	    	log("|log() error: " + str(e))
            pass

def insert_database(tag, domain, url):
    post = {"domain": domain,
            "tag": tag,
            "url": url,
	    "date": datetime.datetime.utcnow()}
    posts = db.posts
    try:
        post_id = posts.insert_one(post).inserted_id
	if debug:
        	print "[+] Added to database", url
    except Exception, e:
	print "[*] Database error", str(e)
	if debug:
		log("|insert_database() error: " + str(e))
	pass

def cls():
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
        os.system("clear")
    elif sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("cls")

def find_script(txt, domain):
    soup = BeautifulSoup(txt, "lxml")
    all_scripts = soup.find_all("script")
    for script in all_scripts:
    	try:
		scr = script.get("src")
		if scr[0] == "/" and scr[1] == "/":
			scr = "https:" + scr
		if (scr.find("http://") < 0 and scr.find("https://") < 0) and intjs:
			if scr[0] == "/":
				scr = domain + scr
			else:
				scr = domain + "/" + scr
                if (scr.find("http://") < 0 and scr.find("https://") < 0) and not intjs:
                        continue
		# print scr
    		if scr.find(".js") >= 0:
			print "[+] Script src tag:", scr
        		# print script.get("src")
			log(domain + "|Script src tag:" + scr)
			# insert_database("script", domain, scr)
        except Exception, e:
#		log("|find_script() error: " + str(e))
#		print "Error"
        	continue

def find_iframe(txt, domain):
    soup = BeautifulSoup(txt, "lxml")
    all_scripts = soup.find_all("iframe")
    for script in all_scripts:
        try:
                scr = script.get("src")
                if scr[0] == "/" and scr[1] == "/":
                        scr = "https:" + scr
                if (scr.find("http://") < 0 and scr.find("https://") < 0) and intjs:
                        if scr[0] == "/":
                                scr = domain + scr
                        else:
                                scr = domain + "/" + scr
                if (scr.find("http://") < 0 and scr.find("https://") < 0) and not intjs:
                        continue
                # print scr
#                if scr.find(".js") >= 0:
                print "[+] Iframe src tag:", scr
                # print script.get("src")
                log(domain + "|Iframe src tag:" + scr)
                # insert_database("script", domain, scr)
        except Exception, e:
#		log("|find_iframe() error: " + str(e))
#               print "Error"
                continue


def banner():
    cls()
    print "===================================================="
    print u"JavaScript Crawler v1.0 [https://www.mertsarica.com]"
    print "===================================================="

def check():
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    # cj = cookielib.LWPCookieJar()
    # br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')]
    br.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ENUSMSNIP)')]

    try:
        FILE  = open ("domains.txt","r" )
        hosts = FILE.readlines()
        FILE.close()
    except IOError:
        print "[+] domains.txt not found!\n"
        sys.exit(1)

    for host in hosts:
	try:
		print "[*] Connecting to:", host.strip()
        	br.open(host.strip(), timeout=1.0)
        	response = br.response()
		find_script(response.read(), host.strip())
        	find_iframe(response.read(), host.strip())
		# sys.exit(1)
        except Exception, e:
		if debug:
			log("|Connection error: " + str(e))
                print "[*] Connection error:", str(e)
                pass

def main():
    banner()
    while (1==1):
        try:
            print "[+] Crawling..."
            check()
            print "[+] Sleeping %s day..." % (sleepday)
            time.sleep(int(sleepday)*24*60*60)
        except KeyboardInterrupt:
             # banner()
             print "[+] Bye..."
             sys.exit(1)
        except Exception as e:
             print "[+] Error: ", str(e)
	     log("|log() error: " + str(e))
             # print "[+] Connection error, sleeping 5 minutes..."
             # time.sleep(300)
             # main()
	     sys.exit(1)

if __name__ == '__main__': 
    main()

