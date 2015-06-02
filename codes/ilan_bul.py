# -*- coding: utf-8 -*-
# İlan Arama Uygulamasi
# 09.03.2010 23:15
# http://www.mertsarica.com

import urllib2
import re
import os
import sys


os.system("cls")

print "============================================================="
print u"\tİlan Arama Uygulaması v1.0"
print "============================================================="
if len(sys.argv) < 2:
	print "\nKullanim: python ilan_bul.py <aranacak kelime>\n"
	sys.exit(1)

keyword = ' '.join(sys.argv[1:])

print "[+] Anahtar kelime: %s\n" % keyword

keyword = keyword.replace(" ", "+")

url = "http://www.secretcv.com/modul/is_ilanlari?f[kelime]=" + keyword + "&gonder=%C4%B0LAN+ARA&f[oge]=1000"

response = urllib2.urlopen(url)
html = response.read()

ilanlar = re.findall(r"(http://www\.secretcv\.com/ilan/\S+\d+\.html)", html)

firmalar = re.findall(r"(title=\"(\S).*? firma)", html)

if len(firmalar) > 0:
        print u"[+] Anahtar kelime ile ilişkili firmalar:"
        i = 0
        m = 0
        for firma in firmalar:
                if (i % 2) == 0:
                        print "\n[*] Firma: %s" % (unicode(str(firma[0][7:len(firma)-8]), 'utf-8'))
                        url = ilanlar[m]
                        response = urllib2.urlopen(url)
                        html = response.read()
                        sistem = re.findall("(debian|pix|surf control|surfcontrol|checkpoint|mcafee|redhat|solaris|" +
                                            "aix|slackware|windows|cisco|trend micro|trendmicro|symantec|norton|apache|iis|" +
                                            "juniper|websphere|panda|kaspersky|microsoft sql|mssql|oracle|sybase|db2|fortigate|" +
                                            "nod32|sophos|snort|iss|ubuntu|vmware|bindview|bind|arcsight|check point|websense|" +
                                            "veritas|netbackup|net backup|suse|centos|mandrake|spam assassin|spamassassin|qmail|" +
                                            "acronis|exchange|squid|postfix|ossec|qmail)"
                                            , html.lower())
                        sistem = list(set(sistem))
                        if len(sistem) > 0:
                                print u"[**] İlan: %s" % url
                                print u"[**] İlanda tespit edilen potansiyel üretici/yazılım bilgileri:"
                                for bilgi in sistem:
                                        print "\t" + bilgi.capitalize()
                                komut = "start " + url
                                os.system(komut)
                i = i + 1
                m = m + 2
else:
       print u"[+] Anahtar kelime ile ilişkili firma bulunamadı..." 

print "\n--------------------------------------------------------------"
print "\t\thttp://www.mertsarica.com"
