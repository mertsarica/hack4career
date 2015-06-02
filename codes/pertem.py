# -*- coding: utf-8 -*-
# Yedek Subay Sınıflandırma Sonuçları Gözlemcisi v1.0
#
# Bu program belirtilen doneme ait yedek subay sinav sonuclarinin
# TSK web sitesinde yayinlanmasi durumunda belirtilen
# e-posta adresine e-posta gondererek sizi bilgilendirmektedir.
# Not: Gmail e-posta adresi kullanmanız gerekmektedir.
#
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
          
import re
import urllib, urllib2, urlparse
import time
import datetime
import sys
import os
import smtplib
from email.MIMEText import MIMEText

# Dönem bilgisi - Döneme göre değiştirilmesi gerekmektedir!
donem = "339"

# E-posta bilgisi - Girilmesi zorunludur!
GMAIL_LOGIN = 'mert.sarica@gmail.com'
GMAIL_PASSWORD = ''

# Statik değişkenler - Lütfen değiştirmeyiniz!
url = "http://pertem.kkk.tsk.tr/yedeksubay/AdayNoArama.aspx"
waittime = 1*60

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

def send_email(subject, message, from_addr=GMAIL_LOGIN, to_addr=GMAIL_LOGIN):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.ehlo()
    server.login(GMAIL_LOGIN,GMAIL_PASSWORD)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.close()

def sonuclar():
            
    try:
            f = opener.open(url)
    except:
            print "[+] Hata: Internet'e bağlı olduğunuzu ve/veya proxy ayarlarınızın doğru olduğunu kontrol edin!"
            sys.exit(1)
                    
    response = f.read()
    
    if response.find(donem) > 0:
        print u"Sınav sonuçları açıklanmıştır, hayırlı tezkereler :)"
        msg = "Sınav sonuçları açıklanmıştır - http://pertem.kkk.tsk.tr/yedeksubay/AdayNoArama.aspx\n" + "-"*126 + "\nhttp://www.mertsarica.com"
        send_email('Hayırlı Tezkereler :)', msg)

        sys.exit(1)

if __name__ == '__main__':
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
            os.system("clear")
    elif sys.platform == 'win32':
            os.system("cls")
    else:
            os.system("cls")
    print "=========================================================================="
    print u"Yedek Subay Sınıflandırma Sonuçları Gözlemcisi [http://www.mertsarica.com]"
    print "=========================================================================="
    try:
        while(1):
            if sys.platform == 'linux-i386' or sys.platform == 'linux2':
                    os.system("clear")
            elif sys.platform == 'win32':
                   os.system("cls")
            else:
                   os.system("cls")
                    
            print "=========================================================================="
            print u"Yedek Subay Sınıflandırma Sonuçları Gözlemcisi [http://www.mertsarica.com]"
            print "=========================================================================="
            sonuclar()
            print u"Sınav sonuçları henüz açıklanmamış, 1 dakika sonra tekrar kontrol edilecektir..."
            time.sleep(waittime)
    except KeyboardInterrupt:	
        print "Bye..."
