# -*- coding: utf-8 -*-
# Cinemaximum Sinema Bileti Gözlemcisi
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
import subprocess
subprocess.check_output('chcp 1254'.split(), shell=True)

reload(sys)
sys.setdefaultencoding('iso-8859-9')

# keyword = "page-sessions__title error"
keyword = "sessions-display__no-session"
title = "Batman vs Superman"
mailto = "Alıcı e-posta adresi"
# mailto = "mert.sarica@gmail.com"

GMAIL_LOGIN = 'Gönderen e-posta adresi'
GMAIL_PASSWORD = 'E-posta şifresi'

# url = "https://cinemaximum.com.tr/biletleme/~step~session~tarih~18-12-2015~sinema~palladium~film~star-wars-guc-uyaniyor"
url = "https://www.cinemaximum.com.tr/biletleme/~step~session~tarih~27-03-2016~sinema~palladium~film~batman-v-superman-adaletin-safagi"
waittime = 30*60

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

def send_email(subject, message, from_addr=GMAIL_LOGIN, to_addr=mailto):
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
    global title
        
    try:
            f = opener.open(url)
    except:
            print u"[+] Hata: Internet'e bağlı olduğunuzu ve/veya proxy ayarlarınızın doğru olduğunu kontrol edin!"
            sys.exit(1)

    response = f.read()
    
    if response.find(keyword) < 0:
        print title + u" Sinema Bileti Satışa Çıkmıştır!"
        title = title + " Sinema Bileti Satışa Çıkmıştır!"
        msg = title + "\n" + "\nSinema biletini satın almak için ziyaret etmeniz gereken web adresi: " + url
        try:
            send_email(title, msg)
        except:
            print u"[+] Hata: E-posta bilgilerinizin doğru olduğunu kontrol edin!"
            sys.exit(1)
        sys.exit(1)

if __name__ == '__main__':
    try:
        while(1):
            if sys.platform == 'linux-i386' or sys.platform == 'linux2':
                    os.system("clear")
            elif sys.platform == 'win32':
                   os.system("cls")
            else:
                   os.system("cls")
                    
            print "================================================================"
            print u"Cinemaximum Sinema Bileti Gözlemcisi [http://www.mertsarica.com]"
            print "================================================================"
            sonuclar()
            print title + u" sinema bileti henüz satışa çıkmamış, 30 dakika sonra tekrar kontrol edilecektir..."
            time.sleep(waittime)
    except KeyboardInterrupt:	
        print "Bye..."
