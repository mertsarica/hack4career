# -*- coding: utf-8 -*-
# Türk Dil Kurumu Sözlük Üreticisi
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
# 
# egrep -e "^[a-z]+[^\n]$" *.html | cut -d " " -f 1 | sort | uniq -i | cut -d ":" -f 2 > sozluk.txt

import sys
import os
import urllib, urllib2, urlparse
import time
import re
import codecs

debug = 0
i = 0
error = 0

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
	opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
else:
	opener = urllib2.build_opener(urllib2.HTTPHandler)

# install it
urllib2.install_opener(opener)

if sys.platform == 'linux-i386' or sys.platform == 'linux2':
        os.system("clear")
elif sys.platform == 'win32':
        os.system("cls")
else:
        os.system("cls")

def kelime_topla(kelime, sayfa):
    global error

    kelime = kelime.strip()
    if sayfa:
        url = "http://www.tdkterim.gov.tr/bts/?kategori=verilst&ayn=tam&kelime=" + urllib.quote(kelime.encode('iso-8859-9')) + "%&sayfa=" + sayfa
        print "http://www.tdkterim.gov.tr/bts/?kategori=verilst&ayn=tam&kelime=" + kelime + "%&sayfa=" + sayfa
    else:
        url = "http://www.tdkterim.gov.tr/bts/?kategori=verilst&ayn=tam&kelime=" + urllib.quote(kelime.encode('iso-8859-9')) + "%"
        print "http://www.tdkterim.gov.tr/bts/?kategori=verilst&ayn=tam&kelime=" + kelime + "%"

    # if debug:
    # print url

    try:
            f = opener.open(url)
    except Exception, (message):
            error = error + 1
            if error == 3:
                    print "[+] Error: Check your internet connection or proxy configuration"
                    sys.exit(1)
            else:
                    kelime_topla(kelime, sayfa)
    error = 0                       
    response = f.read()

    if sayfa:
        fname = kelime.strip() + sayfa + ".html"
    else:
        fname = kelime.strip() + ".html"
        
    FILE= open(fname,"w")
    FILE.write(response)
    FILE.close()

    if debug:
            print response
            
    while response.find("SONRAK") > 0:

        txt=response

        re1='((?:[a-z][a-z]+))'	# Word 1
        re2='.*?'	# Non-greedy match on filler
        re3='(sayfa=)'	# Word 2
        re4='(\\d+)'	# Integer Number 1
        re5='(">SONRAK)'	# Word 3

        rg = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)
        m = rg.search(txt)
        if m:
            c1=m.group(3)
            time.sleep(5)
            if c1 == sayfa:
                    kelime_olustur("")
            else:
                    kelime_topla(kelime, c1)
                    
def kelime_olustur(resume):
    harfler = ["a", "b", "c", u"ç", "d", "e", "f", "g", u"ğ", "h", u"ı", "i", "j", "k", "l", "m", "n", "o", u"ö", "p", "r", "s", u"ş", "t", "u", u"ü", "v", "y", "z"]
    global i
    
    if resume:
            if debug:
                    print resume
            i = harfler.index(resume[0])
            resume = ""

    while i < len(harfler):
        harf = harfler[i]
        i = i + 1
        if debug:
            print u"%s" % harf

        # harf = unicode(harf, "utf-8")
        FILE= codecs.open("resume.ini","w", "utf-8")
        FILE.write(harf)
        FILE.close()

        kelime_topla(harf, 0)

    sys.exit(1)
  
if __name__ == '__main__':
    print "==========================================================="
    print u"TDK Online Dictionary Generator [http://www.mertsarica.com]"
    print "==========================================================="

    resume = ""
    
    try:
            FILE  = codecs.open ("resume.ini","r","utf-8")   
            resume = FILE.readlines()
            resume = "".join(resume)
            FILE.close()
            print "[+] Resuming -> [%s] :)\n" % (resume)
    except IOError:
            print "[+] Resume file not found\n"
		
    try:
            print "[+] Crawling:"
            if resume:
                    kelime_olustur(resume)
            else:
                    kelime_olustur("")
    except KeyboardInterrupt:
            os.system("cls")
            print "==========================================================="
            print u"TDK Online Dictionary Generator [http://www.mertsarica.com]"
            print "==========================================================="		
            print "[+] Bye..."

    sys.exit(1)


