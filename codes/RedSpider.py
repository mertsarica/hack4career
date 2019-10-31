# -*- coding: cp1254 -*-
# Expired Domain Check v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.mertsarica.com

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from urlparse import urlparse
import time
import os
import sys
import urllib, urllib2
import datetime

domains = []
debug = 0
logfile = "logs.txt"

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

def log(txt):
    try:
            now = datetime.datetime.now()
            time = now.strftime("%d-%m-%Y %H:%M:%S")                
            file = open(logfile, "a")
            txt = str(time + " " + str(txt).encode("cp1254") + "\n")
            file.write(txt)
            file.close()
    except Exception as e:
        print str(e)
        if debug:
            log("|log() error: " + str(e))
            pass
			
def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")

def banner():
	cls()

	print "======================================================"
	print u"Expired Domain Check v1.0 [https://www.mertsarica.com]"
	print "======================================================"

def is_registered(domain):
	url = "https://www.whois.com.tr/process.php"
	post_data_dictionary = {"domain" : domain,
							"tld"    : ""    ,
							"sid"    : "13"}
	http_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36 RS"}
	post_data_encoded = urllib.urlencode(post_data_dictionary)
	request_object = urllib2.Request(url, post_data_encoded, http_headers)
	f = opener.open(request_object)
	response = f.read().decode("utf-8")
	if debug:
		print "[*] Response:", response
	time.sleep(2)
	if domain.find("www.") >= 0:
		domain = domain.split("www.")[1]
	findStr="(" + domain + ")</h1>"
	if response.find("No match for") > 0 and response.find(findStr) > 0:
			return 0
	return 1

class RedSpider(CrawlSpider):
	name = 'RedSpider'
	allowed_domains = ['mertsarica.com']
	start_urls = ['https://www.mertsarica.com']
	AUTOTHROTTLE_ENABLED = "True"
	
	rules = (
		Rule(LinkExtractor(unique=True), callback='parse_item', follow=True),
	)

	banner()
	print "[*] Crawling:", "".join(start_urls)

	def parse_item(self, response):
		txt = ""
		link = ""
		# links = response.css('a[href*=http]::attr(href)').extract()
		links = response.css('a::attr(href)').extract()
		crawledLinks = []
			
		for domain in links:		
			if debug:
				print "URL: ", domain

			try:
				link = domain
				domain = ".".join(urlparse(domain).hostname.split(".")[-2:]) #urlparse(domain).hostname
				if domain.replace(".","").isdigit():
					continue
				if domain.find(".") < 0:
					continue
			except Exception as e:
				if debug:
					print str(e)
				continue
			
			if len(domain) > 0 and domain.find(".tr") < 0 and domain not in domains and domain.find("/") < 0:
				domains.append(domain)

				if debug:
					print "Domain:", domain, "Page:", response.request.url

				try:
					if is_registered(domain):
						print "[-] Domain:", domain, "Expired: NO"
						txt = "Domain: " + domain + " Expired: NO"
						log(txt)
					else:
						print "[+] Domain:", domain, "Expired: YES", "Page:", response.request.url
						txt = "Domain: " + domain + " Expired: YES " + " Page: " + response.request.url
						log(txt)
				except Exception as e:
					if debug:
						print str(e)
					continue