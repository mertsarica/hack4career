# -*- coding: cp1254 -*-
# Suspicious JavaScript Hunter v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.mertsarica.com

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
# from urlparse import urlparse
from scrapy.utils.httpobj import urlparse
import time
import os
import sys
import urllib, urllib2
import datetime
import re
import yara

urls = []
debug = 0
logfile = "logs.txt"

# Terminates itself after crawled x JavaScript links
max_crawl_limit = 15
crawl_counter = 0

# You may download yara rules from https://github.com/Yara-Rules/rules
# Extracted main yara rule file
yararules = "C:\\Users\\Mert\\Desktop\\Yara\\rules-master\\rules-master\\index.yar"
rules = yara.compile(yararules)

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

	print "=============================================================="
	print u"Suspicious JavaScript Hunter v1.0 [https://www.mertsarica.com]"
	print "=============================================================="

class RedSpider(CrawlSpider):
	name = 'RedSpider'
	start_urls = []
	AUTOTHROTTLE_ENABLED = "True"

	def __init__(self, url=None, *args, **kwargs):
		super(RedSpider, self).__init__(*args, **kwargs)
		# self.allowed_domains = [url]
		# self.start_urls = ["http://" + url]
		input = kwargs.get('urls', '').split(',') or []
		self.allowed_domains = input
		self.start_urls = ["http://" + input[0]]
		
	rules = (
		Rule(LinkExtractor(unique=True), callback='parse_item', follow=True),
	)

	banner()
	print "[*] Crawling..."
		
	def parse_item(self, response):
		txt = ""
		link = ""
		sdata = ""

		scripts = response.xpath('//script[@src]').extract()
		crawledLinks = []

		for sdata in scripts:		
			if debug:
				print "Script Tag: ", sdata

			try:
				if sdata.find(".js") < 0:
					continue

				re1='src="'	# Word 1
				re2='((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))'	# HTTP URL 1
				re3='"'

				rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
				m = rg.search(sdata)
				if m:
					httpurl1=m.group(1)
					link = httpurl1 
					if debug:
						print "[*] JavaScript URL detected (regex):", link
						
				else:

					if sdata.find("//") >= 0:
						continue
						
					re1='src='	# Word 1
					re2='(".*?")'	# HTTP URL 1

					rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
					m = rg.search(sdata)
					if m:
						httpurl1=m.group(1)
						if debug:
							print "[*] JavaScript URL detected (regex):", httpurl1

						if not httpurl1.startswith( "/" ):
							httpurl1 = "/" + httpurl1
						
						link = "".join(self.start_urls) + httpurl1.replace("\"", "")
			except Exception as e:
				if debug:
					print str(e)
				continue
			
			if link not in urls and len(link) >= 1:
				urls.append(link)

				if debug:
					print "[*] JavaScript URL:", link

				yield scrapy.Request(link, callback=self.parse_body)

	def parse_body(self, response):		
		global crawl_counter
		try:
			crawl_counter += 1
			if crawl_counter > max_crawl_limit:
				os._exit(0)
			matches = rules.match(data=response.body)
			if matches:
				for match in matches:
					print "[+] URL:", response.request.url, "Matched YARA Rule:", match
					if debug:
						print "[*] Matched body response:", response.body.decode("utf-8")
					txt = "URL: " + response.request.url + " Matched YARA Rule: " + str(match)
					log(txt)
		except Exception as e:
#			if debug:
			print str(e)