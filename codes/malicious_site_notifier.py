# -*- coding: utf-8 -*-
# ZararlÄ± URL Duyuru istemcisi
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
# Consumer key: 
# Consumer secret: 
# Access Token key: 
# Access Token secret: 
          
import feedparser
import re
import urllib, urllib2, urlparse
import time
import datetime
import sys
import os
import oauth
import socket
import twitter

default_timeout = 30

socket.setdefaulttimeout(default_timeout)

reload(sys)
sys.setdefaultencoding('iso-8859-9')

debug = 0
updated = 0
score = 0
virus = ""
url = ""
published = 0
waittime = 24*60*60

proxy_info = {
'user' : '',
'pass' : '',
'host' : "",
'port' : 8080 # or 8080 or whatever
}

# build a new opener that uses a proxy requiring authorization
proxy_support = urllib2.ProxyHandler({"http" : \
"http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxy_info})

if proxy_info['host'] != "":
	opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
else:
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	
# install it
urllib2.install_opener(opener)

def log(txt):
    now = datetime.datetime.now()
    time = now.strftime("%d-%m-%Y %H:%M")
    file = open("/logs.txt", "a")
    txt = str(time + ":" + txt.encode("cp1254") + "\n")
    file.write(txt)
    file.close()

def tweet(txt):
    if debug:
	print "Tweet:", txt
    api = twitter.Api(consumer_key='key',
                      consumer_secret='key',
                      access_token_key='key',
                      access_token_secret='key')
    if debug:
    	print "Twitter:", twitter
    user_timeline = api.PostUpdate(txt.encode("utf-8"))
    if debug:
    	print "Timeline:", user_timeline

def direct_message(user, txt):         
    consumer_key = "key"
    consumer_secret = "key"

    now = datetime.datetime.now()
    time = now.strftime("%d-%m-%Y %H:%M")

    log = ""
    file = open("/tweets.txt", "a")
    log = str(time + ":" + user + ":" + txt + "\n")
    file.write(log)
    file.close()
    
    twitter = OAuthApi(consumer_key, consumer_secret)

    # Do a test API call using our new credentials
    twitter = OAuthApi(consumer_key, consumer_secret, 'key', 'key')
    txt = "d " + user + " " + txt
    user_timeline = twitter.UpdateStatus(status=txt.encode("utf-8"))
    
def get_score(txt):
    global score
    
    re1='(vt_score)'	# Variable Name 1
    re2='.*?'	# Non-greedy match on filler
    re3='(\\d+)'	# Integer Number 1
    re4='(\\/)'	# Any Single Character 1
    re5='(\\d+)'	# Integer Number 2
    
    rg = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)
    m = rg.search(txt)
    if m:
        var1=m.group(1)
        int1=m.group(2)
        c1=m.group(3)
        int2=m.group(4)
        if debug:
            print "("+var1+")"+"("+int1+")"+"("+c1+")"+"("+int2+")"+"\n"
        if int(int2)/4 < int(int1):
            score = 1
        else:
            score = 0
            
def get_virusname(txt):
    global virus
		
    re1='(virusname)'	# Word 1
    re2='.*?'	# Non-greedy match on filler
    re3='((?:[a-z][a-z0-9_./]*))'	# Variable Name 1
    re4='.*?'	# Non-greedy match on filler
    re5='(<)'	# Any Single Character 1
    
    rg = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)
    m = rg.search(txt)
    if m:
        word1=m.group(1)
        var1=m.group(2)
        c1=m.group(3)
        if debug:
            print "("+word1+")"+"("+var1+")"+"("+c1+")"+"\n"
        virus = var1
    else:
        virus = ""

def malwares():
    entry = 0.0
   
    try:
        FILE  = open ("/malwares.txt","r" )   
        entry = FILE.read()
        FILE.close()
    except IOError:
        pass
        print "[+] viruses.txt file not found but do not worry I will create it right now :)\n"

    m = 1
    
    while m > 0:
            url = "http://malc0de.com/database/index.php?search=TR&CC=on&page=" + str(m)
            response = opener.open(url)
	    
            html = response.read()
	    if debug:
            	print url
	    	print html


            retup = re.findall(r"(<td>)([0-9]{4})(-)([0-9]{2})(-)([0-9]{2})(</td>)", html)
            date = []
            url = []
            i = 0

	    if debug:
            	print retup   
            if len(retup) > 0:
                    for element in retup[::-1]:
                        date.append(element[5] + "." + element[3] + "." + element[1])
                        ldate = element[5] + element[3] + element[1]
                        i = i + 1

                    retup = re.findall(r"(<td>)([a-zA-Z0-9\.-]*)(/)([ a-zA-ZÅžÅŸÄžÄŸÃœÃ¼Ã–Ã¶Ã‡Ã§IÄ±ö0-9\.\/\-\_\=\&\?\>\<\~\"\;]*)(</td>)", html)
                    for element in retup[::-1]:
                            url.append(element[1]+element[2]+element[3])

                    i = 0
		    if debug:
                    	print url
                    if len(date) == len(url):
			    if debug:
                            	print "i", i
				print "date", date
				print "url", url
                            while i < len(date):
                                    a = datetime.datetime(int(date[i][6:10]), int(date[i][3:5]), int(date[i][0:2]), 0, 0, 0, 0)
                                    b = datetime.datetime(1982, 2, 13, 0, 0, 0, 0)
                                    if entry:
                                            b = datetime.datetime(int(entry[4:9]), int(entry[2:4]), int(entry[0:2]), 0, 0, 0, 0)
                                    if a > b:
                                            print "[Zararlý Site] - http://" + url[i].replace("<br/>", "") + " - " + date[i]
                                            msg = "[Zararlý Site] - http://" + url[i].replace("<br/>", "") + " - " + date[i]
                			    try:
                        			tweet(msg)
                			    except Exception,e:                         
                        			print str(e)
                        			pass
                                            log(msg)
                                            time.sleep(3)
                                    i = i + 1
                    else:                
                            print "Uzunluk hatasý!"
                            sys.exit(0)
            m = m - 1

    file = open("/malwares.txt", "w")
    txt = str(ldate)
    file.write(txt)
    file.close()

def viruses():
    global published
    entry = 0
    
    try:
            FILE  = open ("viruses.txt","r" )   
            entry = FILE.read()
            FILE.close()
    except IOError:
            pass
            print "[+] viruses.txt file not found but do not worry I will create it right now :)\n"
            
    d = feedparser.parse("http://support.clean-mx.de/clean-mx/rss?scope=viruses&country=TR&limit=0,50")
    i = len(d['entries']) - 1
    
    while i >= 0:
        if debug:
            print d['entries'][i]['title']       # each entry is a dictionary
        if d['entries'][i]['title'].find("c99shell.com") >= 0:
            i = i - 1
            continue
        if d['entries'][i]['title'].find("tr-shell.org") >= 0:
            i = i - 1
            continue
        if d['entries'][i]['title'].find("sh3llz.org") >= 0:
            i = i - 1
            continue
        published = d['entries'][i].updated_parsed
        date = time.mktime(published)
        published = str(published[2]) + "." + str(published[1]) + "." + str(published[0])
        
        url = d['entries'][i]['title']
        if debug:
            print d['entries'][i]['summary_detail'].value
 	
        get_score(d['entries'][i]['summary_detail'].value)
        if score > 0:
            get_virusname(d['entries'][i]['summary_detail'].value)
            if debug:
                print score, url, virus, published, date, entry
	    
            if date > float(entry):
                msg = "[Zararlý Site] - " + url.strip() + " - " + published

		try:
                	print msg
		except:
			pass

                try:
                	tweet(msg)
                except Exception,e:    
                	print str(e)
                	pass
                log(msg)

                file = open("/viruses.txt", "w")
                file.write(str(date))
                file.close()
                time.sleep(3)

        i = i - 1

def get_feedurl(txt):
    global feedurl

    re1='(url)'	# Word 1
    re2='.*?'	# Non-greedy match on filler
    re3='((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))'	# HTTP URL 1
    re4='.*?'	# Non-greedy match on filler
    re5='(<[^>]+>)'	# Tag 1

    rg = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)
    m = rg.search(txt)
    if m:
            word1=m.group(1)
            httpurl1=m.group(2)
            tag1=m.group(3)
            feedurl = httpurl1.replace("<br", "")
            return feedurl
        
def portals():
    entry = 0
    try:
            FILE  = open ("/portals.txt","r" )   
            entry = FILE.read()
            FILE.close()
    except IOError:
            pass

            
    global published
    d = feedparser.parse("http://support.clean-mx.de/clean-mx/rss?scope=portals&country=TR&limit=0,150")
    i = len(d['entries']) - 1
    while i >= 0:
        url = get_feedurl(d['entries'][i]['summary_detail'].value)
        if debug:
            print d['entries'][i]['title']       # each entry is a dictionary
        if url.find("c99shell.com") >= 0:
            i = i - 1
            continue
        if url.find("tr-shell.org") >= 0:
            i = i - 1
            continue
        if url.find("sh3llz.org") >= 0:
            i = i - 1
            continue
        published = d['entries'][i].updated_parsed
	if debug:
		print "published:", published
        date = time.mktime(published)
	if debug:
		print "date:", date
        published = str(published[2]) + "." + str(published[1]) + "." + str(published[0])
	if debug:
		print "published2:", published
        
        # url = d['entries'][i]['title']
        
        if debug:
            print d['entries'][i]['summary_detail'].value
            print url, published, date, entry

	if debug:
		print "date, float(entry)", date, entry
        if date > float(entry):
	    msg = "[Hacklenmiþ Site] - " + url.encode("ascii", "ignore") + " - " + published
            print msg
            try:                            
                        tweet(msg)                        
            except Exception,e:                            
                        print str(e)                        
                        pass 
            log(msg)

            file = open("/portals.txt", "w")
            file.write(str(date))
            file.close()
            time.sleep(3)
            
        i = i - 1

def urlquery():
    global updated
    filename = "/urlquery.txt"
    site = ""
    entries = ""       
    killbill = 0               

    try:
            FILE  = open (filename,"r" )
            entries = FILE.readlines()
            entries = "".join(entries)
            FILE.close()
    except IOError:
            pass
            print "[+] urlquery.txt file not found but do not worry I will create it right now :)\n"

    url = "http://urlquery.net/index.php"
    response = opener.open(url)

    html = response.read()

    if debug:
        print url
        print html

    txt = html


    retup = re.findall("<td><nobr><center>([0-9 :-]*)</center></nobr></td><td align='center'><b>([0-9 :-]*)</b></td><td><a title='([ a-zA-ZÖÇÞÝÐÜöçþiðü0-9\./-_=&\?><~\";:]*)' href='report.php\?id=([0-9]*)'>([ a-zA-ZÖÇÞÝÐÜöçþiðü0-9\./-_=&\?><~\";:]*)</a></td><td style='text-align:center;vertical-align=middle;'><img src='images/flags/tr.png'", html)

    for element in retup:
            print " ".join(element)
            if " ".join(element).find("0 - 0 - 0") >= 0:
                continue
            site = " ".join(element)
            date = site.split(" ")[0].split("-")[2] + "-" + site.split(" ")[0].split("-")[1] + "-" + site.split(" ")[0].split("-")[0] # + " " + site.split(" ")[1]
            lsite = site.split(" ")[5]
            site = site.split(" ")[5]
            site = lsite + " - " + date
            if entries.find(lsite) < 0:
                    if debug:
                            print site

                    msg = "[Zararlý Site] - " + site
                    print "[Zararlý Site] - " + site
                    try:
                        tweet(msg)
                    except Exception,e:
                        print str(e)
                        pass
                    log(msg)

                    if killbill == 0:
                        FILE = open(filename,"w")
                        FILE.writelines(lsite)
                        FILE.close()
                    killbill = 1
            else:
                break


    try:
            FILE  = open ("/urlquery.txt","r" )
            entry = FILE.read()
            FILE.close()
    except IOError:
            pass
            print "[+] urlquery.txt file not found but do not worry I will create it right now :)\n"

def hacked():
    global updated
    filename = "/hacked.txt"
    counter = 30
    i = 1
    site = ""
    killbill = 0
    entries = ""

    try:
            FILE  = open (filename,"r" )   
            entries = FILE.readlines()
            FILE.close()
    except IOError:
            pass
            print "[+] hacked.txt file not found but do not worry I will create it right now :)\n"

    while int(i) < counter:
            url = "http://www.zone-h.org/archive/special=1/page=" + str(i)
            if debug:
                print url
                
            response = opener.open(url)
            html = response.read()
                    
	    retup = re.findall(r"(<td>)([a-zA-Z0-9\/\@\:\=\.\"\-\_\~\+\]\[\(\) ]*)(\.tr|\.tr/([a-zA-Z0-9\/\!\@\:\=\.\"\-\_\~\+\]\[\(\) ]*))", html)
            if len(retup) > 0:
                for element in retup:
                    site = element[1] + element[2] + element[3]
                    if site.find("w.tr") > 0:
                        break
                    if entries:
                        if debug:
                            print entries[0]
                        if site.strip() == entries[0].strip():
                            killbill = 1
                            break

                    if debug:
                            print site
                            
                    msg = "[Hacklenmiþ Site] - " + site #.split("/")[0]
                    print "[Hacklenmiþ Site] - " + site
               	    try:                            
                        tweet(msg)                        
                    except Exception,e:                            
                        print str(e)                        
                        pass 
                    log(msg)
                    
                    if updated == 0:
                        updated = 1
                        FILE = open(filename,"w")
                        FILE.writelines(site)
                        FILE.close()
                        
            i = i + 1
            if killbill == 1:
                break
            time.sleep(3)
                        
    try:
            FILE  = open ("/hacked.txt","r" )   
            entry = FILE.read()
            FILE.close()
    except IOError:
            pass
            print "[+] hacked.txt file not found but do not worry I will create it right now :)\n"
            
if __name__ == '__main__':
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
            os.system("clear")
    elif sys.platform == 'win32':
            os.system("cls")
    else:
            os.system("cls")
    print "==================================================="
    print "Malicious Site Notifier [http://www.mertsarica.com]"
    print "==================================================="
    print "[+] 3 dakika bekleniyor..."
    time.sleep(3)
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
        os.system("clear")
    elif sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("cls")
    print "==================================================="
    print "Malicious Site Notifier [http://www.mertsarica.com]"
    print "==================================================="
    try:
        while(1):
            updated = 0

	    try:
		    print "viruses()"
            	    viruses()
		    print "portals()"
            	    portals()
		    print "hacked()"
                    hacked()
		    # print "malwares()"
                    # malwares()
		    print "urlquery()"
		    urlquery()
            except Exception,e: 
		    print str(e)
                    pass
            time.sleep(waittime)
    except KeyboardInterrupt:	
        print "[+] Bye..."
